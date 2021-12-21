# 200-irr_slab-surface_dcmip_pert simulation config file

from modules.baseconfig import *

COMPONENTS = {'convection': clm.EmanuelConvection(),
              'simple_physics': sym.TimeDifferencingWrapper(clm.SimplePhysics()),
              'radiation_lw': sym.UpdateFrequencyWrapper(clm.RRTMGLongwave(), timedelta(minutes=60)),
              'radiation_sw': sym.UpdateFrequencyWrapper(clm.RRTMGShortwave(), timedelta(minutes=60)),
              'slab_surface': clm.SlabSurface()}

GRID = {'nx': 128, 'ny': 62}


FIELDS_TO_STORE = ('atmosphere_hybrid_sigma_pressure_a_coordinate_on_interface_levels', 'atmosphere_hybrid_sigma_pressure_b_coordinate_on_interface_levels', 'surface_air_pressure', 'air_pressure',
                   'air_pressure_on_interface_levels', 'longitude', 'latitude', 'height_on_ice_interface_levels', 'air_temperature', 'eastward_wind', 'northward_wind', 'divergence_of_wind',
                   'atmosphere_relative_vorticity', 'surface_geopotential', 'specific_humidity', 'cloud_base_mass_flux', 'surface_temperature', 'surface_specific_humidity',
                   'longwave_optical_depth_on_interface_levels')


def set_initial_state(state):
    clm.set_constants_from_dict({'stellar_irradiance': {'value': 200, 'units': 'W m^-2'}})
    dcmip = clm.DcmipInitialConditions(add_perturbation=True)
    state.update(dcmip(state))
