from . import var
from . import plot
import matplotlib.pyplot as plt
import sympl as sym
import climt as clm
import logging, os, importlib, shutil
import numpy as np

log = logging.getLogger(__name__)


def copy_state(state):
    return_state = {}
    for name, quantity in state.items():
        if isinstance(quantity, sym.DataArray):
            return_state[name] = sym.DataArray(quantity.values.copy(), quantity.coords, quantity.dims, quantity.name, quantity.attrs)
        else:
            return_state[name] = quantity
    return return_state


class ClimateDynamics(object):
    def __init__(self, name, overwrite=False):
        log.info(f"Loading model {name}...")
        self.name, self.overwrite = name, overwrite
        self.filepath = os.path.join(var.SIMULATIONS_DIR, name)

        config = importlib.import_module(f"simulations.{self.name}.config")
        self.components = {name: comp for name, comp in config.COMPONENTS.items()}
        self.dycore = clm.GFSDynamicalCore(self.components.values(), number_of_damped_levels=5)
        self.grid = clm.get_grid(**config.GRID)
        self.state = clm.get_default_state([self.dycore, ], grid_state=self.grid)
        config.set_initial_state(self.state)
        self.time_step, self.steps, self.saving_steps, self.plotting_steps = config.TIME_STEP, config.STEPS, config.SAVING_STEPS, config.PLOTTING_STEPS
        self.figures = {k: (plt.figure(figsize=i[0], dpi=300),) + i[1:] for k, i in config.FIGURES.items()}
        self._make_dirs()
        self.monitors = (sym.NetCDFMonitor(os.path.join(self.filepath, f"{self.name}-store.nc"), write_on_store=True, store_names=config.FIELDS_TO_STORE),
                         sym.RestartMonitor(os.path.join(self.filepath, f"{self.name}-restart.nc")))

    def _make_dirs(self):
        for dir_name in var.SIMULATION_SUBDIRS:
            path = os.path.join(self.filepath, dir_name)
            try:
                os.mkdir(path)
            except FileExistsError:
                if self.overwrite or input(f"Directory {dir_name} already exists, overwrite? (y/n)  ").lower() == 'y':
                    shutil.rmtree(path)
                    try:
                        os.remove(os.path.join(self.filepath, f"{self.name}-store.nc"))
                        os.remove(os.path.join(self.filepath, f"{self.name}-restart.nc"))
                    except FileNotFoundError:
                        pass
                    os.mkdir(path)
                else:
                    log.info("Directory not overwritten, exiting.")
                    exit()
        for graph in self.figures:
            path = os.path.join(self.filepath, 'graphics', graph)
            os.mkdir(path)

    def _state_update(self):
        diag, self.state = self.dycore(self.state, self.time_step)
        self.state.update(diag)

    def run(self):
        log.info(f"Simulation {self.name} started...")
        for i in range(self.steps):
            try:
                np.seterr(all='raise')
                self._state_update()
                np.seterr(all='warn')
            except FloatingPointError:
                log.error(f"FloatingPointError encountered at cycle {i}, exiting model...")
                self._plot_function()
                self._save_to_monitors()
                break
            if i % (self.plotting_steps) == 0:
                log.info(f"\t reached cycle {i}\t  -  day {i // self.plotting_steps}")
                self._plot_function()
            if i % (self.saving_steps) == 0:
                self._save_to_monitors()
            self.state['time'] += self.time_step
        log.info(f"Simulation {self.name} ended")
        del self.dycore

    def _save_to_monitors(self):
        state = copy_state(self.state)
        for k in var.COMPONENTS_TO_SANIFY:
            state.pop(k, None)
        for m in self.monitors:
            m.store(state)

    def _plot_function(self):
        for name, f in self.figures.items():
            f[1](f[0], copy_state(self.state), name=self.name, **f[2])
            f[0].savefig(os.path.join(self.filepath, "graphics", name, f"{self.name}-{name}-{self.state['time'].strftime(var.DATETIME_FORMAT)}"))
