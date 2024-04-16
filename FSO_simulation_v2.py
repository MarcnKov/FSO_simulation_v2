from src import opticalpropagation
from src import phasescreen
from src import helper_functions as help_func
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import tqdm
import threading
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

n_phase_screens = params['n_phase_screens']
sim_res         = params['sim_res']
sim_size        = params['sim_size']
rx_alt          = params['rx_alt']
rx_diameter     = params['rx_diameter']
wvl             = params['wvl']         
w0              = params['w0']
power           = params['power']
max_turb_alt    = params['max_turb_alt']
min_turb_alt    = params['min_turb_alt']

if len(params['r0']) != 0 and len(params['r0']) == n_phase_screens:
    r0 = params['r0']
else:
    r0 = np.random.rand(n_phase_screens)*0.2
    logger.info(f"n_phase_screens size and r0 array sizes don't match. Generating random array of r0 values.")

if len(params['screen_alt']) != 0 and len(params['screen_alt']) == n_phase_screens:
    screen_alt = params['screen_alt']
else:
    screen_alt = np.linspace(min_turb_alt,
                             min(max_turb_alt,rx_alt-min_turb_alt),
                             n_phase_screens)
    logger.info(f"n_phase_screens size and screen_alt array sizes don't match. Generating uniformely spaced array of screen_alt.")

l0              = params['l0'] if len(params['l0']) != 0 else 1e-2
l0              = np.full((n_phase_screens,), l0[0])  
L0              = params['L0'] if len(params['L0']) != 0 else 50
L0              = np.full((n_phase_screens,),L0[0])

params["r0"]    = np.array(r0).tolist()
params["l0"]    = l0.tolist()
params["L0"]    = L0.tolist()

# params["screen_alt"] = screen_alt.tolist()

#######################SIMULATION CONFIGURATION###############

with open('sim_config.json', 'w') as config_file:
    json.dump(params, config_file, indent=4)

for key, value in params.items():
    logger.info(f"{key}: {value}")

#append rx altitutde to the screen altitudes 
screen_alt      = np.append(screen_alt, rx_alt)

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

logger.info("Generate Atmopsheric Phase Screens")
progress_bar = tqdm.tqdm(total=n_phase_screens-1)
worker_thread = threading.Thread(target=help_func.worker,
                                 args=(progress_bar,))
worker_thread.start()

for i in range(0, n_phase_screens):
    phase_screens[:,:,i] = phasescreen.ft_phase_screen(r0[i], 
                                                       sim_res,
                                                       pxl_scale,
                                                       L0[i],
                                                       l0[i])
    progress_bar.update()

worker_thread.join()
progress_bar.close()

logger.info("Propagate beam up to the first phase screen")
dz = rx_alt if n_phase_screens == 0 else screen_alt[0]
el_field = help_func.gaussian_beam_ext(r_sq,
                                         dz,
                                         w0,
                                         wvl)


logger.info("Propagate beam through phase screens")

progress_bar = tqdm.tqdm(total=n_phase_screens-1)
worker_thread = threading.Thread(target=help_func.worker,
                                 args=(progress_bar,))
worker_thread.start()
for i in range(1, n_phase_screens+1):

    dz = abs(screen_alt[i] - screen_alt[i-1])    

    el_field *= np.exp(1j*phase_screens[:,:,i-1])
    el_field[:] = opticalpropagation.angularSpectrum(el_field,
                                                     wvl,
                                                     pxl_scale,
                                                     pxl_scale,
                                                     dz)
    
    progress_bar.update()

worker_thread.join()
progress_bar.close()

logger.info("Plot intensity")
intensity = help_func.calc_intensity(el_field, power, w0)
rx_intensity, rx_power = help_func.calc_RX_params(intensity,
                                                  sim_res,
                                                  rx_diameter,
                                                  pxl_scale)

logger.info(f"Total power = {help_func.calc_tot_power(intensity, pxl_scale):.10f} W")
logger.info(f"RX power =  {rx_power:.10f} W")
logger.info(f"RX power =  {10*np.log10(1000*rx_power/1):.10f} dBm")
logger.info(f"Total Losses =  {10*np.log10(power/rx_power):.10f} dB")

help_func.plot_intensity(rx_intensity, sim_size, rx_alt, "Aperture")
help_func.plot_intensity(intensity, sim_size, rx_alt, "Total")
