import os
import sympl as sym
import climt as clm
from datetime import timedelta

# Directories
DATA_DIR = os.path.join(os.getcwd(), 'data')
GRAPHICS_DIR = os.path.join(DATA_DIR, 'graphics')

# Files
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Model
MODEL_COMPONENTS = {'convection': clm.EmanuelConvection(),
                    'simple_physics': sym.TimeDifferencingWrapper(clm.SimplePhysics()),
                    'radiation': sym.UpdateFrequencyWrapper(clm.GrayLongwaveRadiation(), timedelta(minutes=60))}

MODEL_GRID = {'nx': 62, 'ny': 62, 'nz': 10}

MODEL_TIME_STEP = timedelta(minutes=20)
MODEL_STEPS = 24*3*365
