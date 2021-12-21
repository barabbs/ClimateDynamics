# improved_dcmip_no_perturbation simulation config file

from modules.baseconfig import *
import numpy as np

COMPONENTS = {'convection': clm.EmanuelConvection(),
              'simple_physics': sym.TimeDifferencingWrapper(clm.SimplePhysics()),
              'radiation_lw': sym.UpdateFrequencyWrapper(clm.RRTMGLongwave(), timedelta(minutes=60)),
              'radiation_sw': sym.UpdateFrequencyWrapper(clm.RRTMGShortwave(), timedelta(minutes=60)),
              'slab_surface': clm.SlabSurface()}

GRID = {'nx': 128, 'ny': 62}

FIELDS_TO_STORE = ('air_temperature', 'air_pressure', 'eastward_wind',
                   'northward_wind', 'air_pressure_on_interface_levels',
                   'surface_pressure', 'upwelling_longwave_flux_in_air',
                   'specific_humidity', 'surface_temperature',
                   'latitude', 'longitude',
                   'convective_heating_rate')


def set_initial_state(state):
    clm.set_constants_from_dict({'stellar_irradiance': {'value': 200, 'units': 'W m^-2'}})
    latitudes = state['latitude'].values
    longitudes = state['longitude'].values

    zenith_angle = np.radians(latitudes)

    state['zenith_angle'].values = zenith_angle
    state['eastward_wind'].values[:] = np.random.randn(
        *state['eastward_wind'].shape)
    state['ocean_mixed_layer_thickness'].values[:] = 50

    surf_temp_profile = 290 - (40 * np.sin(zenith_angle) ** 2)
    state['surface_temperature'].values = surf_temp_profile
    dcmip = clm.DcmipInitialConditions(add_perturbation=False)
    state.update(dcmip(state))
