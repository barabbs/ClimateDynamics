from . import var
from . import plot
import matplotlib.pyplot as plt
import sympl as sym
import climt as clm
import logging, os, importlib, shutil
from datetime import timedelta

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
    def __init__(self, name="EMPTY"):
        log.info("Loading model...")
        self.name = name
        self.filepath = os.path.join(var.SIMULATIONS_DIR, name)

        config = importlib.import_module(f"data.simulations.{self.name}.config")
        self.components = {name: comp for name, comp in config.COMPONENTS.items()}
        self.dycore = clm.GFSDynamicalCore(self.components.values(), number_of_damped_levels=5)
        self.grid = clm.get_grid(**config.GRID)
        self.state = clm.get_default_state([self.dycore, ], grid_state=self.grid)
        config.set_initial_state(self.state)
        self.time_step, self.steps = config.TIME_STEP, config.STEPS
        self.figures = {k: (plt.figure(figsize=i[0], dpi=300),) + i[1:] for k, i in config.FIGURES.items()}
        self._make_dirs()
        self.monitors = (sym.NetCDFMonitor(os.path.join(self.filepath, f"{name}-store.nc"), write_on_store=True, store_names=config.FIELDS_TO_STORE),
                         sym.RestartMonitor(os.path.join(self.filepath, f"{name}-restart.nc")))

    def _make_dirs(self):
        for dir_name in var.SIMULATION_SUBDIRS:
            path = os.path.join(self.filepath, dir_name)
            try:
                os.mkdir(path)
            except FileExistsError:
                if input(f"Directory {dir_name} already exists, overwrite? (y/n)  ").lower() == 'y':
                    shutil.rmtree(path)
                    os.mkdir(path)
                else:
                    log.info("Directory not overwritten, exiting.")
                    exit()
        for graph in self.figures:
            path = os.path.join(self.filepath, 'graphics', graph)
            os.mkdir(path)

    def _state_update(self, time_step):
        diag, self.state = self.dycore(self.state, time_step)
        self.state.update(diag)
        self.state['time'] += self.time_step
        # self.monitor.store(self.state)

    def run(self):
        log.info("Simulation Started...")
        for i in range(self.steps):
            if i % (24 * 3) == 0:
                log.info(f"\t- reached cycle {i}")
                self._plot_function()
                if i > 0:
                    self._save_to_monitors()
            self._state_update(self.time_step)
        log.info("Simulation Ended")

    def _save_to_monitors(self):
        # for comp, unit in var.COMPONENTS_TO_SANIFY.items():
        #     print(f"--- {comp}")
        #     print(self.state[comp].attrs['units'])
        #     self.state[comp] = self.state[comp].to_units(unit)
        #     print(self.state[comp].attrs['units'])
        for m in self.monitors:
            m.store(self.state)

    def _plot_function(self):
        for name, f in self.figures.items():
            f[1](f[0], copy_state(self.state), name=self.name, **f[2])
            f[0].savefig(os.path.join(self.filepath, "graphics", name, f"{self.name}-{name}-{self.state['time'].strftime(var.DATETIME_FORMAT)}"))
