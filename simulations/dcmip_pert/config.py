# dcmip_pert simulation config file

from modules.baseconfig import *

COMPONENTS = {'convection': clm.EmanuelConvection(),
              'simple_physics': sym.TimeDifferencingWrapper(clm.SimplePhysics()),
              'radiation': sym.UpdateFrequencyWrapper(clm.GrayLongwaveRadiation(), timedelta(minutes=60))}

GRID = {'nx': 62, 'ny': 62, 'nz': 10}


FIELDS_TO_STORE = ('atmosphere_hybrid_sigma_pressure_a_coordinate_on_interface_levels', 'atmosphere_hybrid_sigma_pressure_b_coordinate_on_interface_levels', 'surface_air_pressure', 'air_pressure',
                   'air_pressure_on_interface_levels', 'longitude', 'latitude', 'height_on_ice_interface_levels', 'air_temperature', 'eastward_wind', 'northward_wind', 'divergence_of_wind',
                   'atmosphere_relative_vorticity', 'surface_geopotential', 'specific_humidity', 'cloud_base_mass_flux', 'surface_temperature', 'surface_specific_humidity',
                   'longwave_optical_depth_on_interface_levels')


def set_initial_state(state):
    dcmip = clm.DcmipInitialConditions(add_perturbation=True)
    state.update(dcmip(state))
