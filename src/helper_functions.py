import sys
import os

sys.path.append(os.getcwd())

from . import pupil
from math import ceil
import matplotlib.pyplot as plt
import numpy as np

from src.opticalpropagation import angularSpectrum
from src.phasescreen import ft_phase_screen

# Define constants
EARTH_RADIUS    = 6371e3

def worker(progress_bar):
    with progress_bar._lock:
        progress_bar.update()

def generate_phase_screens(sim):
    
    sim.logger.info("\nGenerate Atmopsheric Phase Screens")

    for i in range(0, sim.n_phase_screens):
        
        sim.phase_screens[:,:,i] = ft_phase_screen( sim.r0[i], 
                                                    sim.sim_res,
                                                    sim.pxl_scale,
                                                    sim.L0[i],
                                                    sim.l0[i])

def propagate_beam(sim, n_phase_screens):

    sim.logger.info("Propagate beam up to the first phase screen")

    dz = sim.rx_alt if n_phase_screens == 0 else sim.screen_alt[0]
    
    sim.el_field = gaussian_beam_ext(sim.r_sq,dz,sim.w0,sim.wvl)
 
    sim.logger.info("Propagate beam through phase screens")

    for i in range(1, n_phase_screens+1):
    
        dz = abs(sim.screen_alt[i] - sim.screen_alt[i-1])    
     
        sim.el_field    *= np.exp(1j*sim.phase_screens[:,:,i-1])
        sim.el_field[:]  = angularSpectrum( sim.el_field,
                                            sim.wvl,
                                            sim.pxl_scale,
                                            sim.pxl_scale,
                                            dz)

def gaussian_beam_ext(r_sq, z, w0, wvl, flag = False):   
    
    """
    Evaluates Gaussian beam field or its phase
    Parameters:
        r_sq (ndarray) : x**2 + y**2 (m)
        z    (float) : distance b/w TX and phase screen (m)
        flag (bool)  : returns phase if true, else returns Efield
    Returns:
        ndarray: calculated gaussian field at (xi,yi,zi)
    """
    
    #wave number
    k = 2*np.pi/wvl
    
    #refractive index of the medium
    n = 1 #to modify --> n = n(z)
    
    #Rayleigh range
    z_r = np.pi*w0**2*n/wvl
    
    #beam width
    w_z = w0*np.sqrt(1+(z/z_r)**2)
    
    #wavefront radius of curvature
    R_z = z*(1+(z_r/z)**2)
    
    #Guy phase
    ph_z = np.arctan(z/z_r)
    phase = np.exp(-1j*(k*z + k*r_sq/(2*R_z) - ph_z))
    if (flag):
        return phase
    return  w0/w_z*np.exp(-r_sq/w_z**2)*phase


def beam_size(z, w0, wvl):

    k = 2*np.pi/wvl
    #Rayleigh range
    z_r = np.pi*w0**2/wvl
    return 2*w0*np.sqrt(1+(z/z_r)**2)

def calc_intensity(el_field, power, w0):

    I_0 = 2*power/(np.pi*w0**2)
    return I_0*np.abs(el_field)**2 

def calc_tot_power(intensity, dx):
    return dx**2 * np.sum(intensity)

def calc_RX_params(intensity, n_sim_pxls, rx_diameter, dx):
    
    """
    Calculates RX Intensity at the aperture 

    Returns:
        float : RX Intensity at aperture
        float : RX power at aperture
    """

    n_rx_pxls = rx_diameter/dx
    aperture = pupil.circle(ceil(n_rx_pxls/2), n_sim_pxls).astype(bool)
    rx_intensity = np.where(aperture,intensity, 0)
    rx_power = dx**2*np.sum(rx_intensity)  
    
    return rx_intensity, rx_power 

def calc_scintillation_idx(self):

    """
    Calculates RX scintillation index 
    Returns:
        float : scintillation index 
    """
    I_aperture  = self.calc_RX_intensity()    
    variance    = np.var(I_aperture,    where = self.aperture)
    mean        = np.mean(I_aperture,   where = self.aperture)

    return variance/mean**2

def plot_intensity(intensity, sim_size, rx_alt, txt):
       
    #determine extent
    extent = -sim_size/2, sim_size/2, -sim_size/2, sim_size/2

    fig, ax = plt.subplots(1, 2)
    
    image = ax[0].imshow(intensity, extent=extent)
    ax[0].set_title(txt + ' intensity at ' + str(rx_alt/1000) + ' (km)')
    ax[0].set_xlabel(r'$x_n/2$' + ' (m)')
    ax[0].set_ylabel(r'$y_n/2$' + ' (m)')

    colorbar = fig.colorbar(image, ax=ax[0], fraction=0.05, label='Intensity')

    ax[1].plot(intensity[:, np.shape(intensity)[0]//2 ])
    ax[1].set_title('Intensity cross-section')
    ax[1].set_xlabel(r'$x_n/2$' + ' (m)')
    ax[1].set_ylabel(r'$W/m^2$' + ' (m)')
    
    plt.show()


def slantRange(sim, elevation):
  """
    Calculate slant range from satellite to ground station.

    Parameters:
    elevation (float): Elevation angle of the satellite in degrees.

    Returns:
    float: Slant range from satellite to ground station in meters.
    """
  ANG_EARTH_RAD   = EARTH_RADIUS/(EARTH_RADIUS + sim.rx_alt)

  nadir_angle = np.arcsin(ANG_EARTH_RAD*np.cos(np.radians(elevation)))
  
  #earth centre angle  
  epsilon = np.radians(90 - np.degrees(nadir_angle) - elevation)
  slant_range = EARTH_RADIUS*np.sin(epsilon)/np.sin(nadir_angle)

  return slant_range
