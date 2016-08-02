# solutions.py
"""Volume II: Wavelets
"""

import sys
from matplotlib import pyplot as plt
import numpy as np
import scipy as sp
from scipy.signal import fftconvolve

# Problem 1: Implement this AND the following function.
def dwt(X, L, H, n):
    """Compute the Discrete Wavelet Transform of X using filters L and H.

    Parameters:
        X (1D ndarray): The signal to be processed.
        L (1D ndarray): The low-pass filter.
        H (1D ndarray): The high-pass filter.
        n (int > 0): Controls the degree of transformation.
    
    Returns:
        a list of the wavelet decomposition arrays.
    """
    i = 0                                  #Some initialization steps
    A = X
    D = []
    while i < n:
        D.append(fftconvolve(A, H)[1::2])    #High-pass filtering
        A = (fftconvolve(A, L)[1::2])        #Low-pass filtering
        i += 1
    D.append(A)
    D = D[::-1]
    return D

def plot(X, L, H, n):
    """Plot the results of dwt with the given inputs.
    Your plot should be very similar to Figure 2.

    Parameters:
        X (1D ndarray): The signal to be processed.
        L (1D ndarray): The low-pass filter.
        H (1D ndarray): The high-pass filter.
        n (int > 0): Controls the degree of transformation.
    """

    coeffs = dwt(X, L, H, n)
    plt.subplot(n+2,1,1)
    plt.plot(X)
    for i in xrange(len(coeffs)):
        plt.subplot(n+2,1,i+2)
        plt.plot(coeffs[i])
    plt.show()

def test_prob1():
    """Tests Problem 1 as per the instructions in the .tex file."""
    L = np.ones(2)/np.sqrt(2)
    H = np.array([-1,1])/np.sqrt(2)
    n = 4
    domain = np.linspace(0,4*np.pi, 1024)
    noise = np.random.randn(1024)*.1
    X = np.sin(domain) + noise
    plot(X, L, H, n)

# Problem 2: Implement this function.
def idwt(coeffs, L, H):
    """
    Parameters:
        coeffs (list): a list of wavelet decomposition arrays.
        L (1D ndarray): The low-pass filter.
        H (1D ndarray): The high-pass filter.
    Returns:
        The reconstructed signal (as a 1D ndarray).
    """
    n = len(coeffs) - 1
    A = coeffs[0]
    coeffs = coeffs[1:]
    for i in xrange(n):
        D = coeffs[i]
        print len(D)
        up_A = np.zeros(2*A.size)
        up_A[::2] = A
        up_D = np.zeros(2*D.size)
        up_D[::2] = D
        print len(up_A),len(L),len(up_D),len(H)
        # now convolve and add, but discard last entry
        A = fftconvolve(up_A,L)[:-1] + fftconvolve(up_D,H)[:-1]
    return A

def test_prob2():
    """Tests Problem 1 as per the instructions in the .tex file."""
    L = np.ones(2)/np.sqrt(2)
    H = np.array([-1,1])/np.sqrt(2)
    n = 4
    
    domain = np.linspace(0,4*np.pi, 1024)
    noise = np.random.randn(1024)*.1
    X = np.sin(domain) + noise
    coeffs = dwt(X, L, H, n)

    Ln = [1/np.sqrt(2),1/np.sqrt(2)]
    Hn = [1/np.sqrt(2),-1/np.sqrt(2)]
    A = idwt(coeffs, Ln, Hn)
    plt.plot(A)
    return np.allclose(X, A)
