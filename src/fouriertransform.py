"""
Module containing useful FFT based function and classes

Library is taken from aotools software package under the GPL 3 licence, link below
https://github.com/AOtools/aotools/blob/main/aotools/fouriertransform.py
"""
import numpy


def ft(data, delta):
    """
    A properly scaled 1-D FFT

    Parameters:
        data (ndarray): An array on which to perform the FFT
        delta (float): Spacing between elements

    Returns:
        ndarray: scaled FFT
    """
    DATA = numpy.fft.fftshift(
            numpy.fft.fft(
                    numpy.fft.fftshift(data, axes=(-1))),
            axes=(-1)) * delta
    return DATA

def ift(data, delta_f):
    """
    Scaled inverse 1-D FFT

    Parameters:
        data (ndarray): Data in Fourier Space to transform
        delta_f (ndarray): Frequency spacing of grid

    Returns:
        ndarray: Scaled data in real space
    """

    DATA = numpy.fft.ifftshift(
            numpy.fft.ifft(
                    numpy.fft.ifftshift(data, axes=(-1))),
            axes=(-1)) * data.shape[-1] * delta_f

    return DATA


def ft2(data, delta):
    """
    A properly scaled 2-D FFT

    Parameters:
        data (ndarray): An array on which to perform the FFT
        delta (float): Spacing between elements

    Returns:
        ndarray: scaled FFT
    """

    DATA = numpy.fft.fftshift(
            numpy.fft.fft2(
                    numpy.fft.fftshift(data, axes=(-1,-2))
                    ), axes=(-1,-2)
            )*delta**2

    return DATA

def ift2(data, delta_f):
    """
    Scaled inverse 2-D FFT

    Parameters:
        data (ndarray): Data in Fourier Space to transform
        delta_f (ndarray): Frequency spacing of grid

    Returns:
        ndarray: Scaled data in real space
    """
    N = data.shape[-1]
    DATA = numpy.fft.ifftshift(
            numpy.fft.ifft2(
                    numpy.fft.ifftshift(data, axes=(-1,-2)
                    ), axes=(-1,-2))
            , axes=(-1,-2)) * (N * delta_f)**2

    return DATA

def rft(data, delta):
    """
    A properly scaled real 1-D FFT

    Parameters:
        data (ndarray): An array on which to perform the FFT
        delta (float): Spacing between elements

    Returns:
        ndarray: scaled FFT
    """
    DATA = numpy.fft.fftshift(
            numpy.fft.rfft(
                    numpy.fft.fftshift(data, axes=(-1))),
            axes=(-1)) * delta
    return DATA

def irft(data, delta_f):
    """
    Scaled real inverse 1-D FFT

    Parameters:
        data (ndarray): Data in Fourier Space to transform
        delta_f (ndarray): Frequency spacing of grid

    Returns:
        ndarray: Scaled data in real space
    """

    DATA = numpy.fft.ifftshift(
            numpy.fft.irfft(
                    numpy.fft.ifftshift(data, axes=(-1))),
            axes=(-1)) * data.shape[-1] * delta_f

    return DATA

def rft2(data, delta):
    """
    A properly scaled, real 2-D FFT

    Parameters:
        data (ndarray): An array on which to perform the FFT
        delta (float): Spacing between elements

    Returns:
        ndarray: scaled FFT
    """
    DATA = numpy.fft.fftshift(
            numpy.fft.rfft2(
                    numpy.fft.fftshift(data, axes=(-1,-2))
                    ), axes=(-1,-2)
            )*delta**2

    return DATA

def irft2(data, delta_f):
    """
    Scaled inverse real 2-D FFT

    Parameters:
        data (ndarray): Data in Fourier Space to transform
        delta_f (ndarray): Frequency spacing of grid

    Returns:
        ndarray: Scaled data in real space
    """
    N = data.shape[-1]
    DATA = numpy.fft.ifftshift(
            numpy.fft.irfft2(
                    numpy.fft.ifftshift(data, axes=(-1,-2)), 
                    axes=(-1,-2)
                    ),
            axes=(-1,-2)) * (N * delta_f)**2
    return DATA
