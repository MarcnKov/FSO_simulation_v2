from datetime import datetime
import tqdm
import threading
import matplotlib.pyplot as plt
import numpy as np
import logging
import json

class Simulation:

    current_datetime = datetime.now()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('FSO_simulation_log.txt')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(stream_handler)

    logger.info(f"================= SIMULATION START ===============")

    with open('sim_config.json') as config_file:
        params = json.load(config_file)

    sim_type        = params['sim_type']
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
    windSpeeds      = params['windSpeeds']
    windDirs        = params['windDirs']

    if  len(screen_alt) != n_phase_screens or \
        len(r0)         != n_phase_screens or \
        len(l0)         != n_phase_screens or \
        len(windSpeeds) != n_phase_screens or \
        len(windDirs)   != n_phase_screens:

        logger.error("Sizes of arrays don't match n_phase_screens size. Halting execution.")
        raise ValueError("Sizes of arrays don't match n_phase_screens size.")

    logger.info(f"============= SIMULATION CONFIGURATION ===========")

    for key, value in params.items():
        logger.info(f"{key}: {value}")

    logger.info(f"================= ============== =================")

    def update_simulation(self):

        self.pxl_scale      = self.sim_size / float(self.sim_res)
        nx, ny              =   np.meshgrid(np.arange(-self.sim_res/2,self.sim_res/2),
                                            np.arange(-self.sim_res/2,self.sim_res/2))
        self.xn             = nx * self.pxl_scale
        self.yn             = ny * self.pxl_scale
        self.r_sq           = self.xn**2 + self.yn**2
        self.phase_screens  = np.zeros((self.sim_res, self.sim_res, self.n_phase_screens ),
                                       dtype=np.float32)
        self.el_field       = 0