from src import helper_functions as help_func
from src import sim_setup as sim
from src.phasescreen import atmos
import numpy as np
import time
import matplotlib.pyplot as plt


sim_size_x1 = 50
sim_size_x2 = 250

sim_res_x1 = 4000
sim_res_x2 = 15000



if __name__ == "__main__":

    Sim = sim.Simulation()
    Sim.update_simulation()

    Atm = atmos(Sim)
    scrns = Atm.moveScrns()

    # fig, ax = plt.subplots()

    # for i in range(len(scrns)):
    
    #     ax.imshow(scrns[i])
    #     plt.savefig(f'image_{i}.png')
    #     plt.pause(0.1)
    #     plt.draw()
    
    # fig, ax = plt.subplots()
    # animation = FuncAnimation(fig, animate, frames=len(scrns), interval=10)  # Adjust interval for speed
    # plt.show()
    
    ###############################################################################
    
    # elevation = np.linspace(10, 40, 4)

    # slant_range = help_func.slantRange(Sim, elevation).astype(int)  
    # slant_range = slant_range[::-1]
    
    # sim_res_    = help_func.interpol_linear_fit(slant_range, slant_range[0], slant_range[-1], sim_res_x1,  sim_res_x2).astype(int) 
    # sim_size_   = help_func.interpol_linear_fit(slant_range, slant_range[0], slant_range[-1], sim_size_x1, sim_size_x2).astype(int) 

    # Sim.logger.info(f"\nPropagate beam through atmosphere for {len(elevation)} elevation angles")

    # progress_bar    = sim.tqdm.tqdm(total=len(slant_range))
    # worker_thread   = sim.threading.Thread(target= help_func.worker,args=(progress_bar,))
    # worker_thread.start()

    # r0  = Sim.r0    
    # for rx_alt, elev, sim_res, sim_size in zip(slant_range[::-1], elevation, sim_res_[::-1], sim_size_[::-1]):
        
    #     Sim.sim_res  = int(sim_res)
    #     Sim.sim_size = int(sim_size)
        
    #     Sim.r0 = np.dot(r0, np.cos(np.deg2rad(elev - 90)))

    #     Sim.update_simulation()

    #     Sim.logger.info(f"Propagate beam through atmosphere for rx_alt {rx_alt/1e3} | elevation {elev} | sim_res {sim_res} | sim_size {sim_size} | r0 {Sim.r0}")
    #     screen_alt = np.append(Sim.screen_alt, rx_alt)

    #     Sim.logger.info(f"Propagate beam without turbulence")
    
    #     help_func.propagate_beam(Sim, 0, rx_alt, screen_alt)
    #     intensity = help_func.calc_intensity(Sim.el_field, Sim.power, Sim.w0)
    #     rx_intensity, rx_power = help_func.calc_RX_params(intensity,
    #                                                       Sim.sim_res,
    #                                                       Sim.rx_diameter,
    #                                                       Sim.pxl_scale)
    
    #     losses_no_turbulence = 10*np.log10(Sim.power/rx_power)
    #     # help_func.plot_intensity(intensity, Sim.sim_size, rx_alt, "Total")
    #     Sim.logger.info(f"RX power no turbulence =  {rx_power:.10f} W | {10*np.log10(1000*rx_power/1)} dBm")
    #     Sim.logger.info(f"Total Losses no turbulence =  {10*np.log10(Sim.power/rx_power):.10f} dB")        
        
    #     Sim.logger.info(f"Perform a simulation for {Sim.n_iterations} turbulent iterations")

    #     tot_losses = 0
    #     for i in range(Sim.n_iterations):
                     
    #         help_func.generate_phase_screens(Sim)
    #         help_func.propagate_beam(Sim, Sim.n_phase_screens, rx_alt, screen_alt)
    #         intensity = help_func.calc_intensity(Sim.el_field, Sim.power, Sim.w0)
    #         rx_intensity, rx_power = help_func.calc_RX_params(  intensity,
    #                                                             Sim.sim_res,
    #                                                             Sim.rx_diameter,
    #                                                             Sim.pxl_scale)
    #         if (i == 0):
    #             help_func.plot_intensity(intensity, Sim.sim_size, rx_alt, "Total", elev)

    #         Sim.logger.info(f"RX power =  {rx_power:.10f} W | {10*np.log10(1000*rx_power/1)} dBm")
    #         Sim.logger.info(f"Total Losses =  {10*np.log10(Sim.power/rx_power):.10f} dB")        
    #         tot_losses += 10*np.log10(Sim.power/rx_power)
        
    #     avg_losses          = tot_losses/Sim.n_iterations
    #     turbulence_losses   = avg_losses - losses_no_turbulence
    #     Sim.logger.info(f"Average Losses = {avg_losses:.10f} dB")
    #     Sim.logger.info(f"Turbulence Losses = {turbulence_losses:.10f} dB")
        
    #     screen_alt = 0
    #     progress_bar.update()

    # worker_thread.join()
    # progress_bar.close()
    
    
    ###############################################################################

    # sim.logger.info(f"Propagate beam without turbulence")
    
    # help_func.propagate_beam(sim, 0)
    # intensity = help_func.calc_intensity(sim.el_field, sim.power, sim.w0)
    # rx_intensity, rx_power = help_func.calc_RX_params(intensity,
    #                                                   sim.sim_res,
    #                                                   sim.rx_diameter,
    #                                                   sim.pxl_scale)
    
    # help_func.plot_intensity(intensity, sim.sim_size, sim.rx_alt, "Total")
    # sim.logger.info(f"RX power no turbulence =  {rx_power:.10f} W | {10*np.log10(1000*rx_power/1)} dBm")
    # sim.logger.info(f"Total Losses no turbulence =  {10*np.log10(sim.power/rx_power):.10f} dB")        
    # sim.logger.info(f"Perform a simulation for {sim.n_iterations} turbulent iterations")

    # progress_bar    = sim.tqdm.tqdm(total=sim.n_iterations-1)
    # worker_thread   = sim.threading.Thread(target= help_func.worker,args=(progress_bar,))
    # worker_thread.start()

    # tot_losses      = 0
    # for i in range(sim.n_iterations):
                
    #     help_func.generate_phase_screens(sim)
    #     help_func.propagate_beam(sim, sim.n_phase_screens)
    #     intensity = help_func.calc_intensity(sim.el_field, sim.power, sim.w0)
    #     rx_intensity, rx_power = help_func.calc_RX_params(intensity,
    #                                                   sim.sim_res,
    #                                                   sim.rx_diameter,
    #                                                   sim.pxl_scale)
    #     if (i == 0):
    #         help_func.plot_intensity(intensity, sim.sim_size, sim.rx_alt, "Total")
    #         help_func.plot_intensity(rx_intensity, sim.sim_size, sim.rx_alt, "Aperture")

    #     sim.logger.info(f"RX power =  {rx_power:.10f} W | {10*np.log10(1000*rx_power/1)} dBm")
    #     sim.logger.info(f"Total Losses =  {10*np.log10(sim.power/rx_power):.10f} dB")        
    #     tot_losses += 10*np.log10(sim.power/rx_power)

    #     progress_bar.update()

    # worker_thread.join()
    # progress_bar.close()

    # avg_losses = tot_losses/sim.n_iterations
    # sim.logger.info(f"Average Losses = {avg_losses:.10f} dB")

    ###############################################################################