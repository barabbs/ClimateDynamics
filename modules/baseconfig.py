# empty simulation config file

from . import plot
import sympl as sym
import climt as clm
from datetime import timedelta

COMPONENTS = dict()

GRID = dict()

TIME_STEP = timedelta(hours=1)
STEPS = 24

FIGURES = {'vertical': ((10, 3), plot.plot_vertical_profile, {'var_names': {'eastward_wind': {'cm': 'PiYG', 'title': 'eastward wind'},
                                                                            'air_temperature': {'cm': 'coolwarm', 'title': 'air temperature'},
                                                                            'atmosphere_relative_vorticity': {'cm': 'PuOr_r', 'title': 'atm. rel. vorticity'}}}),
           'map': ((9, 5), plot.plot_sfc_map, {'var_names': {'eastward_wind': {'cm': 'PiYG', 'title': 'eastward wind'},
                                                             'air_temperature': {'cm': 'coolwarm', 'title': 'air temperature'},
                                                             'divergence_of_wind': {'cm': 'PiYG', 'title': 'divergence of wind'},
                                                             'surface_geopotential': {'cm': 'YlOrBr_r', 'title': 'surface geopotential'}}})}

FIELDS_TO_STORE = None


# ['air_temperature', 'air_pressure', 'atmosphere_relative_vorticity', 'divergence_of_wind', 'eastward_wind', 'northward_wind', 'air_pressure_on_interface_levels',
#                    'specific_humidity', 'surface_air_pressure', 'surface_geopotential', 'surface_temperature', 'latitude', 'longitude', ]


def set_initial_state(state):
    pass
