# plots.py
"""Introductory Labs: NumPy. Plotting file."""

import numpy as np
from matplotlib import pyplot as plt

def jacobi(n=100, tol=1e-8):
    """Solve Laplace's Equation using the Jacobi method and array slicing."""
    # Initialize the plate.
    U = np.zeros((n,n))

    # Set boundary conditions.
    U[:, 0] = 100                   # West boundary condition.
    U[:,-1] = 100                   # East boundary condition.
    U[ 0,:] = 0                     # North boundary condition.
    U[-1,:] = 0                     # South boundary condition.

    # Make a copy and initialize a difference variable.
    V = np.copy(U)
    diff = tol

    # Perform the iteration.
    while diff >= tol:
        V[1:-1,1:-1] = (U[:-2,1:-1] + U[2:,1:-1] + U[1:-1,:-2] + U[1:-1,2:])/4.
        diff = np.max(np.abs(U-V))
        U[1:-1,1:-1] = V[1:-1,1:-1]

    return U

def make_plots():
    U1 = jacobi(10)
    U2 = jacobi(100)

    # Save the results.
    plt.clf()
    plt.tick_params(axis='both', which='both',
                    labelleft='off', labelbottom='off',
                    bottom='off', top='off', left='off', right='off')
    plt.imshow(U1)
    plt.savefig("jacobi_small.pdf", format='pdf')

    plt.clf()
    plt.tick_params(axis='both', which='both',
                    labelleft='off', labelbottom='off',
                    bottom='off', top='off', left='off', right='off')
    plt.imshow(U2)
    plt.savefig("jacobi_big.pdf", format='pdf')
    plt.clf()
    plt.close()

if __name__ == '__main__':
    make_plots()
