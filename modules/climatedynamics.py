from . import var
from . import plot
import matplotlib.pyplot as plt
import sympl as sym
import climt as clm
import logging, os
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
    def __init__(self, name="EMPTY", components=var.MODEL_COMPONENTS, grid=var.MODEL_GRID, time_step=var.MODEL_TIME_STEP, steps=var.MODEL_STEPS, figures=plot.FIGURES):
        log.info("Loading model...")
        self.name = name
        self.filepath = os.path.join(var.GRAPHICS_DIR, name)
        try:
            os.mkdir(self.filepath)
        except FileExistsError:
            log.warning(f"Directory {name} already exists")
        self.components = {name: comp for name, comp in components.items()}
        self.dycore = clm.GFSDynamicalCore(self.components.values(), number_of_damped_levels=5)
        self.grid = clm.get_grid(**grid)
        self.state = clm.get_default_state([self.dycore, ], grid_state=self.grid)
        self._set_initial_state()
        self.time_step, self.steps = time_step, steps
        self.figures = {k: (plt.figure(figsize=i[0], dpi=300),) + i[1:] for k, i in figures.items()}

        # self.monitor = sym.PlotFunctionMonitor(self._plot_function)

    def _set_initial_state(self):
        dcmip = clm.DcmipInitialConditions(add_perturbation=True)
        self.state.update(dcmip(self.state))

    def _state_update(self):
        diag, self.state = self.dycore(self.state, self.time_step)
        self.state.update(diag)
        self.state['time'] += self.time_step
        # self.monitor.store(self.state)

    def run(self):
        log.info("Simulation Started...")
        for i in range(self.steps):
            if i % (24 * 3) == 0:
                self._plot_function()
                # self.monitor.store(self.state)
                log.info(f"\t- reached cycle {i}")
            self._state_update()
        log.info("Simulation Ended")

    def _plot_function(self):
        for name, f in self.figures.items():
            f[1](f[0], copy_state(self.state), name=self.name, **f[2])
            f[0].savefig(os.path.join(self.filepath, f"{self.name}-{name}-{self.state['time'].strftime(var.DATETIME_FORMAT)}"))
