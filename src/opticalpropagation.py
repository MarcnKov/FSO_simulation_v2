'''
A library of useful optical propagation methods.

Many extracted from the book by Schmidt, 2010: Numerical Methods
of optical proagation

Function is taken from aotools software package under the GPL 3 licence, link below
https://github.com/AOtools/aotools/blob/main/aotools/opticalpropagation.py 
'''

import numpy as np
from . import fouriertransform


def angularSpectrum(inputComplexAmp, wvl, inputSpacing, outputSpacing, z):
    """
    Propogates light complex amplitude using an angular spectrum algorithm

    Parameters:
        inputComplexAmp (ndarray): Complex array of input complex amplitude
        wvl (float): Wavelength of light to propagate
        inputSpacing (float): The spacing between points on the input array in metres
        outputSpacing (float): The desired spacing between points on the output array in metres
        z (float): Distance to propagate in metres

    Returns:
        ndarray: propagated complex amplitude
    """
    
    # If propagation distance is 0, don't bother 
    if z==0:
        return inputComplexAmp

    N = inputComplexAmp.shape[0] #Assumes Uin is square.
    k = 2*np.pi/wvl     #optical wavevector

    (x1,y1) = np.meshgrid(inputSpacing*np.arange(-N/2,N/2),
                             inputSpacing*np.arange(-N/2,N/2))
    r1sq = (x1**2 + y1**2) + 1e-10

    #Spatial Frequencies (of source plane)
    df1 = 1. / (N*inputSpacing)
    fX,fY = np.meshgrid(df1*np.arange(-N/2,N/2),
                           df1*np.arange(-N/2,N/2))
    fsq = fX**2 + fY**2

    #Scaling Param
    mag = float(outputSpacing)/inputSpacing

    #Observation Plane Co-ords
    x2,y2 = np.meshgrid( outputSpacing*np.arange(-N/2,N/2),
                            outputSpacing*np.arange(-N/2,N/2) )
    r2sq = x2**2 + y2**2

    #Quadratic phase factors
    Q1 = np.exp( 1j * k/2. * (1-mag)/z * r1sq)

    Q2 = np.exp(-1j * np.pi**2 * 2 * z/mag/k*fsq)

    Q3 = np.exp(1j * k/2. * (mag-1)/(mag*z) * r2sq)

    #Compute propagated field
    outputComplexAmp = Q3 * fouriertransform.ift2(
                    Q2 * fouriertransform.ft2(Q1 * inputComplexAmp/mag,inputSpacing), df1)
    return outputComplexAmp