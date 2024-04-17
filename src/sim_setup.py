from datetime import datetime
import tqdm
import threading
import matplotlib.pyplot as plt
import numpy as np
import logging
import json

#######################CONFIGURE LOGGING######################

current_datetime = datetime.now()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('FSO_simulation_log.txt')
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(stream_handler)

#######################GET PARAMETERS########################

logger.info(f"================= ============== =================")
logger.info(f"================= SIMULATION START ===============")
logger.info(f"================ {current_datetime.strftime('%Y-%m-%d %H:%M')} ================")
logger.info(f"================= ============== =================")

with open('sim_config.json') as config_file:
    params = json.load(config_file)

n_iterations    = params['n_iterations']
n_phase_screens = params['n_phase_screens']
sim_res         = params['sim_res']
sim_size        = params['sim_size']
rx_alt          = params['rx_alt']
rx_diameter     = params['rx_diameter']
wvl             = params['wvl']         
w0              = params['w0']
power           = params['power']
screen_alt      = params['screen_alt']
r0              = params['r0']
l0              = params['l0']
L0              = params['L0']

if  len(screen_alt) != n_phase_screens or \
    len(r0)         != n_phase_screens or \
    len(l0)         != n_phase_screens or \
    len(L0)         != n_phase_screens:

    logger.error("Sizes of arrays don't match n_phase_screens size. Halting execution.")
    raise ValueError("Sizes of arrays don't match n_phase_screens size.")

#######################SIMULATION CONFIGURATION###############

for key, value in params.items():
    logger.info(f"{key}: {value}")

#append rx altitutde to the screen altitudes 
screen_alt = np.append(screen_alt, rx_alt)

#Simulation pixel scale
pxl_scale = sim_size/float(sim_res)

#Discretize simulation grid
nx, ny = np.meshgrid(np.arange(-sim_res/2,sim_res/2),
                     np.arange(-sim_res/2,sim_res/2))

#simulation grid scales in x,y
xn      = nx*pxl_scale                       
yn      = ny*pxl_scale                    
r_sq    = xn**2+yn**2                  

#Allocate phase screens
phase_screens = np.zeros((sim_res,
                          sim_res,
                          n_phase_screens))

#Define Electric Field variable
el_field = 0