import os
import sympl as sym
import climt as clm
from datetime import timedelta

# Directories
DATA_DIR = os.path.join(os.getcwd(), 'data')
SIMULATIONS_DIR = os.path.join(DATA_DIR, 'simulations')
SIMULATION_SUBDIRS = ('graphics',)

# Files
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Model
COMPONENTS_TO_SANIFY = {'eastward_wind': "m/s", 'northward_wind': "m/s", }
