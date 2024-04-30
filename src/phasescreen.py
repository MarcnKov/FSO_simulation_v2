"""
Finite Phase Screens
--------------------

Creation of phase screens of a defined size with Von Karmen Statistics.

Library is taken from aotools software package under the GPL 3 licence, link below
https://github.com/AOtools/aotools/blob/main/aotools/turbulence/phasescreen.py
"""
import scipy
import numpy as np
from numpy import fft
import time
import random
import logging
import matplotlib.pyplot as plt


class atmos(object):
    
    def __init__(self, Sim):

        self.Sim            = Sim
        self.scrn_size      = Sim.sim_res
        self.windDirs       = Sim.windDirs
        self.windSpeeds     = Sim.windSpeeds
        self.pixel_scale    = Sim.pxl_scale #1./Sim.pxl_scale
        self.wholeScrnSize  = Sim.sim_res
        self.scrnNo         = Sim.n_phase_screens
        self.L0             = Sim.L0
        self.l0             = Sim.l0
        self.r0             = Sim.r0
        self.looptime       = 1 #Sim.loopTime
        self.wvl            = Sim.wvl
        self.height         = Sim.rx_alt
        
        self.scrnPos        = {}
        self.wholeScrns     = {}

        scrnSize = int(round(self.scrn_size))

        self.scrns = np.zeros((self.scrnNo, self.scrn_size, self.scrn_size))

        self.fig, self.ax = plt.subplots()

        for i in range(0, self.scrnNo):
            
            # self.wholeScrns[i] = self.wholeScrns[0] 
            self.wholeScrns[i] = ft_phase_screen(self.r0[i],
                                                self.wholeScrnSize,
                                                self.pixel_scale,
                                                self.L0[i],
                                                self.l0[i],
                                                None,
                                                0)
            
            self.scrns[i] = self.wholeScrns[i][:scrnSize,:scrnSize]
                    
        windDirs = np.array(self.windDirs,dtype="float32") * np.pi/180.0
        windV = (self.windSpeeds * np.array([np.cos(windDirs), np.sin(windDirs)])).T
        windV *= 1 #self.looptime   
        windV /= self.pixel_scale

        self.windV = windV
      
        for i in range(0, self.scrnNo):
            self.scrnPos[i] = np.array([0,0])
            if windV[i,0] < 0:
                self.scrnPos[i][0] = self.wholeScrns[i].shape[0] - self.scrn_size
            if windV[i,1] < 0:
                self.scrnPos[i][1] = self.wholeScrns[i].shape[1] - self.scrn_size
        self.windV = windV
        
        #Init scipy interpolation objects which hold the phase screen data
        self.interpScrns = {}
        self.xCoords = {}
        self.yCoords = {}

        for i in range(0, self.scrnNo):

            self.interpScrns[i] = scipy.interpolate.RectBivariateSpline(
                                        np.arange(self.wholeScrnSize),
                                        np.arange(self.wholeScrnSize),
                                        self.wholeScrns[i])#, copy=True)
            
            self.xCoords[i] = np.arange(self.scrn_size).astype('float') + self.scrnPos[i][0]
            self.yCoords[i] = np.arange(self.scrn_size).astype('float') + self.scrnPos[i][1]

    def moveScrns(self):
        """
        Moves the phase screens one time-step, defined by the atmosphere object parameters.
        
        Returned phase is in units of nana-meters

        Returns:
            dict : a dictionary containing the new set of phase screens
        """
        self.Sim.logger.info("Moving phase screens") 
        
        # Other wise proceed with translating large phase screens
        for i in self.wholeScrns:
            
            # Deals with what happens when the window on the screen
            # reaches the edge - rolls it round and starts again.
            # X direction
            if (self.scrnPos[i][0] + self.scrn_size) >= self.wholeScrnSize:
                self.Sim.logger.info("pos > scrn_size: rolling phase screen X")
                self.wholeScrns[i] = np.roll(self.wholeScrns[i],
                                                int(-self.scrnPos[i][0]),axis=0)
                self.scrnPos[i][0] = 0
                # and update the coords...
                self.xCoords[i] = np.arange(self.scrn_size).astype('float')
                self.interpScrns[i] = scipy.interpolate.RectBivariateSpline(
                                            np.arange(self.wholeScrnSize),
                                            np.arange(self.wholeScrnSize),
                                            self.wholeScrns[i])
            if self.scrnPos[i][0] < 0:
                self.Sim.logger.info("pos < 0: rolling phase screen X")

                self.wholeScrns[i] = np.roll(self.wholeScrns[i],
                                                int(self.wholeScrnSize - self.scrnPos[i][0] - self.scrn_size),
                                                axis=0)
                self.scrnPos[i][0] = self.wholeScrnSize-self.scrn_size
                self.xCoords[i] = np.arange(self.scrn_size).astype('float') + self.scrnPos[i][0]
                self.interpScrns[i] = scipy.interpolate.RectBivariateSpline(
                                            np.arange(self.wholeScrnSize),
                                            np.arange(self.wholeScrnSize),
                                            self.wholeScrns[i])
            # Y direction
            if (self.scrnPos[i][1] + self.scrn_size) >= self.wholeScrnSize:
                self.Sim.logger.info("pos > scrn_size: rolling Phase Screen Y")
                self.wholeScrns[i] = np.roll(self.wholeScrns[i],
                                                int(-self.scrnPos[i][1]),axis=1)
                self.scrnPos[i][1] = 0
                self.yCoords[i] = np.arange(self.scrn_size).astype('float')
                self.interpScrns[i] = scipy.interpolate.RectBivariateSpline(
                                            np.arange(self.wholeScrnSize),
                                            np.arange(self.wholeScrnSize),
                                            self.wholeScrns[i])
            if self.scrnPos[i][1] < 0:
                self.Sim.logger.info("pos < 0: rolling Phase Screen Y")

                self.wholeScrns[i] = np.roll(self.wholeScrns[i],
                                                int(self.wholeScrnSize - self.scrnPos[i][1] - self.scrn_size),
                                                axis=1)
                self.scrnPos[i][1] = self.wholeScrnSize-self.scrn_size
                self.yCoords[i] = np.arange(self.scrn_size).astype('float') + self.scrnPos[i][1]
                self.interpScrns[i] = scipy.interpolate.RectBivariateSpline(
                                            np.arange(self.wholeScrnSize),
                                            np.arange(self.wholeScrnSize),
                                            self.wholeScrns[i])
            
            #logger.info("interpScrns {}".self.interpScrns[i])
            self.scrns[i] = self.interpScrns[i](self.xCoords[i], self.yCoords[i])

            self.ax.imshow(self.scrns[i])
            # plt.savefig(f'image_{i}.png')
            self.Sim.logger.info(f"{self.windV[i]}")
            # Move window coordinates.
            self.scrnPos[i] = self.scrnPos[i] + self.windV[i]/1e-4 #*dt
            self.xCoords[i] += self.windV[i][0].astype('float')
            self.yCoords[i] += self.windV[i][1].astype('float') 

        return self.scrns

def ft_phase_screen(r0, N, delta, L0, l0, FFT=None, seed=None):
    """
    Creates a random phase screen with Von Karmen statistics.
    (Schmidt 2010)
    
    Parameters:
        r0 (float): r0 parameter of scrn in metres
        N (int): Size of phase scrn in pxls
        delta (float): size in Metres of each pxl
        L0 (float): Size of outer-scale in metres
        l0 (float): inner scale in metres
        seed (int, optional): seed for random number generator. If provided, 
            allows for deterministic screens  

    .. note::
        The phase screen is returned as a 2d array, with each element representing the phase 
        change in **radians**. This means that to obtain the physical phase distortion in nanometres, 
        it must be multiplied by (wavelength / (2*pi)), (where `wavellength` here is the same wavelength
        in which r0 is given in the function arguments)

    Returns:
        ndarray: np array representing phase screen in radians
    """
    delta = float(delta)
    r0 = float(r0)
    L0 = float(L0)
    l0 = float(l0)

    R = np.random.default_rng(seed)

    del_f = 1./(N*delta)

    fx = np.arange(-N/2., N/2.) * del_f

    (fx, fy) = np.meshgrid(fx,fx)
    f = np.sqrt(fx**2. + fy**2.)

    fm = 5.92/l0/(2*np.pi)
    f0 = 1./L0

    PSD_phi = (0.023*r0**(-5./3.) * np.exp(-1*((f/fm)**2)) / (((f**2) + (f0**2))**(11./6)))

    PSD_phi[int(N/2), int(N/2)] = 0

    cn = ((R.normal(size=(N, N))+1j * R.normal(size=(N, N))) * np.sqrt(PSD_phi)*del_f)

    phs = ift2(cn, 1, FFT).real

    return phs


def ift2(G, delta_f, FFT=None):
    """
    Wrapper for inverse fourier transform

    Parameters:
        G: data to transform
        delta_f: pixel seperation
        FFT (FFT object, optional): An accelerated FFT object
    """

    N = G.shape[0]

    if FFT:
        g = np.fft.fftshift(FFT(np.fft.fftshift(G))) * (N * delta_f) ** 2
    else:
        g = fft.ifftshift(fft.ifft2(fft.fftshift(G))) * (N * delta_f) ** 2

    return g
