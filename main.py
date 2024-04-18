from src import helper_functions as help_func
from src import sim_setup as sim
import numpy as np

if __name__ == "__main__":
        
    sim.logger.info(f"Propagate beam without turbulence")
    
    help_func.propagate_beam(sim, 0)
    intensity = help_func.calc_intensity(sim.el_field, sim.power, sim.w0)
    rx_intensity, rx_power = help_func.calc_RX_params(intensity,
                                                      sim.sim_res,
                                                      sim.rx_diameter,
                                                      sim.pxl_scale)
    
    help_func.plot_intensity(intensity, sim.sim_size, sim.rx_alt, "Total")
    sim.logger.info(f"RX power no turbulence =  {rx_power:.10f} W | {10*np.log10(1000*rx_power/1)} dBm")
    sim.logger.info(f"Total Losses no turbulence =  {10*np.log10(sim.power/rx_power):.10f} dB")        
    sim.logger.info(f"Perform a simulation for {sim.n_iterations} turbulent iterations")

    progress_bar    = sim.tqdm.tqdm(total=sim.n_iterations-1)
    worker_thread   = sim.threading.Thread(target= help_func.worker,args=(progress_bar,))
    worker_thread.start()

    tot_losses      = 0
    for i in range(sim.n_iterations):
                
        help_func.generate_phase_screens(sim)
        help_func.propagate_beam(sim, sim.n_phase_screens)
        intensity = help_func.calc_intensity(sim.el_field, sim.power, sim.w0)
        rx_intensity, rx_power = help_func.calc_RX_params(intensity,
                                                      sim.sim_res,
                                                      sim.rx_diameter,
                                                      sim.pxl_scale)
        if (i == 0):
            help_func.plot_intensity(intensity, sim.sim_size, sim.rx_alt, "Total")
            help_func.plot_intensity(rx_intensity, sim.sim_size, sim.rx_alt, "Aperture")

        sim.logger.info(f"RX power =  {rx_power:.10f} W | {10*np.log10(1000*rx_power/1)} dBm")
        sim.logger.info(f"Total Losses =  {10*np.log10(sim.power/rx_power):.10f} dB")        
        tot_losses += 10*np.log10(sim.power/rx_power)

        progress_bar.update()

    worker_thread.join()
    progress_bar.close()

    avg_losses = tot_losses/sim.n_iterations
    sim.logger.info(f"Average Losses = {avg_losses:.10f} dB")
