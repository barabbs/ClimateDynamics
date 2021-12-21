# empty simulation config file

from . import plot
import sympl as sym
import climt as clm
from datetime import timedelta

COMPONENTS = dict()

GRID = dict()

TIME_STEP = timedelta(minutes=10)
STEPS = 24 * 6 * 365
PLOTTING_STEPS = 24 * 6
SAVING_STEPS = 24 * 6

FIGURES = {'vertical': ((9, 5), plot.get_plot_vertical_profile((2, 2)), {'var_names': {'eastward_wind': {'cm': 'PiYG', 'title': 'eastward wind', 'transpose': True},
                                                                                       'specific_humidity': {'cm': 'Blues', 'title': 'specific humidity', 'transpose': True},
                                                                                       'air_temperature': {'cm': 'coolwarm', 'title': 'air temperature', 'transpose': True},
                                                                                       'atmosphere_relative_vorticity': {'cm': 'PuOr_r', 'title': 'atm. rel. vorticity', 'transpose': True}}}),
           'map': ((9, 5), plot.get_plot_sfc_map((2, 2)), {'var_names': {'eastward_wind': {'cm': 'PiYG', 'title': 'eastward wind'},
                                                                         'air_temperature': {'cm': 'coolwarm', 'title': 'air temperature'},
                                                                         'divergence_of_wind': {'cm': 'PiYG', 'title': 'divergence of wind'},
                                                                         'surface_geopotential': {'cm': 'YlOrBr_r', 'title': 'surface geopotential'}}})}

FIELDS_TO_STORE = None


def set_initial_state(state):
    pass
