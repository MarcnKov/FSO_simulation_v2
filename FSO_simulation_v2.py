from src import opticalpropagation
from src import phasescreen
from src import helper_functions as help_func

import matplotlib.pyplot as plt
import numpy as np
import tqdm
import threading
import logging
import json

##############################################################
#######################SIMULATION CONFIGRUATION###############

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('FSO_simulation_log.txt')

file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()

stream_handler.setFormatter(logging.Formatter('%(message)s'))

logger.addHandler(stream_handler)

#All values in a sim_config.json are in SI units
with open('sim_config.json') as config_file:
    params = json.load(config_file)

n_phase_screens = params['n_phase_screens'] 

sim_res = params['sim_res']
sim_size = params['sim_size']

rx_alt = params['rx_alt']
rx_diameter = params['rx_diameter']

wvl = params['wvl']
w0 = params['w0']
power = params['power']

max_turb_alt = params['max_turb_alt']
min_turb_alt = params['min_turb_alt']

wind_directions = np.full((n_phase_screens,), 0)
params['wind_directions'] = wind_directions.tolist()

wind_speeds = np.random.rand(n_phase_screens)*10
params['wind_speeds'] = wind_speeds.tolist()

# r0 = np.random.rand(n_phase_screens)*0.5 + 0.005
r0 = np.random.rand()*0.1 + 0.005
r0 = np.full((n_phase_screens,), r0)
params['r0'] = r0.tolist() 
  
l0 = np.full((n_phase_screens,), 1e-2)  
params["l0"] = l0.tolist()

L0 = np.full((n_phase_screens,),50)
params["L0"] = L0.tolist()

screen_alt = np.linspace(min_turb_alt, min(max_turb_alt,rx_alt-min_turb_alt), n_phase_screens)
screen_alt = np.append(screen_alt, rx_alt)
params["screen_alt"] = screen_alt.tolist()

with open('sim_config.json', 'w') as config_file:
    json.dump(params, config_file, indent=4)


for key, value in params.items():
    logger.info(f"{key}: {value}")

beam_size = help_func.beam_size(rx_alt, w0, wvl)
logger.info(f"Gaussian beam width =  {beam_size:.2f} m")

if sim_size < 1.2*beam_size:
    logger.warning(f"Small simulation size (screen) is detected. Set sim_size to ≥ {1.2*beam_size:.5f}")

#######################SIMULATION CONFIGURATION###############
##############################################################

pxl_scale = sim_size/float(sim_res) #simulation pixel scale

#Discretize simulation grid
nx, ny = np.meshgrid(np.arange(-sim_res/2,sim_res/2),
                     np.arange(-sim_res/2,sim_res/2))
  
delta = pxl_scale                   #simulation grid size dx
xn = nx*delta                       #simulation grid scaled in x
yn = ny*delta                       #simulation grid scaled in y
r_sq = xn**2+yn**2                  


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
                                                     delta,
                                                     delta,
                                                     dz)
    
    progress_bar.update()

worker_thread.join()
progress_bar.close()

logger.info("Plot intensity")
intensity = help_func.calc_intensity(el_field, power, w0)
rx_intensity, rx_power = help_func.calc_RX_params(intensity,
                                                  sim_res,
                                                  rx_diameter,
                                                  delta)

logger.info(f"Total power = {help_func.calc_tot_power(intensity, delta):.8f} W")
logger.info(f"RX power =  {rx_power:.8f} W")

help_func.plot_intensity(rx_intensity, sim_size, rx_alt, "Aperture")
help_func.plot_intensity(intensity, sim_size, rx_alt, "Total")