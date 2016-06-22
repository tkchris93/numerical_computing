import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../../matplotlibrc')
del matplotlib

from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from random import random
from time import time
import numpy as np
import solutions

# Complexity Pictures =========================================================

def random_vector(n):
    """Generate a random vector of length n as a list."""
    return [random() for i in xrange(n)]

def random_matrix(n):
    """Generate a random nxn matrix as a list of lists."""
    return [[random() for j in xrange(n)] for i in xrange(n)]

def timing_demo(N=13):

    domain = 2**np.arange(1,N)
    times = []
    for n in domain:
        start = time()
        random_matrix(n)
        times.append(time() - start)
    
    plt.plot(domain, times, 'g.-', linewidth=2, markersize=15)
    plt.xlabel("n", fontsize=14)
    plt.ylabel("Seconds", fontsize=14)
    plt.savefig("time_random_matrix1.pdf", format="pdf")

    # Plot the dotted blue line over the green line.
    def f(x, a):
        return a*x**2
    a = curve_fit(f, domain, times)[0][0]

    refinement = np.linspace(1, 2**(N-1), 200)
    plt.plot(refinement, f(refinement, a), 'b--', lw=5)
    plt.ylabel("Seconds", fontsize=14, color="white")

    plt.savefig("time_random_matrix2.pdf", format="pdf")
    plt.clf()
    plt.close("all")

def matrix_multiplication_figures(N=10):
    
    domain = 2**np.arange(N)
    vec, mat = [], []
    
    for n in domain:
        A = random_matrix(n)
        x = random_vector(n)
        B = random_matrix(n)

        start = time()
        [sum([A[i][k] * x[k] for k in range(n)]) for i in range(n)]
        vec.append(time() - start)

        start = time()
        [[sum([A[i][k] * B[k][j] for k in range(n)])
                                 for j in range(n)]
                                 for i in range(n)]
        mat.append(time() - start)        

    # First Figure: Matrix-Vector and Matrix-Matrix by themselves in subplots.
    plt.subplot(121)
    plt.plot(domain, vec, '.-b', lw=2)
    plt.xlabel("n"); plt.ylabel("Seconds")
    plt.title("Matrix-Vector Multiplication")

    plt.subplot(122)
    plt.plot(domain, mat, '.-g', lw=2)
    plt.xlabel("n")
    plt.title("Matrix-Matrix Multiplication")

    plt.savefig("matrixmultiplication1.pdf", format="pdf")
    plt.clf()
    plt.close("all")

    # Second Figure: Matrix-Vector and Matrix-Matrix overlaid w/ diff scales.
    plt.subplot(121)
    plt.plot(domain, vec, '.-b', lw=2, label="Matrix-Vector")
    plt.plot(domain, mat, '.-g', lw=2, label="Matrix-Matrix")
    plt.xlabel("n"); plt.ylabel("Seconds")
    plt.legend(loc="upper left")

    plt.subplot(122)
    plt.loglog(domain, vec, '.-b', basex=2,basey=2,lw=2, label="Matrix-Vector")
    plt.loglog(domain, mat, '.-g', basex=2,basey=2,lw=2, label="Matrix-Matrix")
    plt.xlabel("n")
    plt.legend(loc="upper left")
    
    plt.savefig("matrixmultiplication2.pdf", format="pdf")
    plt.clf()
    plt.close("all")

# Horse Pictures ==============================================================

horse = np.load("horse.npy")[:,::10]

def plotOldNew(old, new, label):
    """Plot an original image and a modified version side by side.

    This plotting script gives better results than the one provided in the
    lab text. Please use this to plot your figures.
    
    Inputs:
        old (2xn ndarray): an array containing the original image's
            x-coordinates on the first row, y-coordinates on the second row.
        new (2xn ndarray): an array containing the transformed image's
            x-coordinates on the first row, y-coordinates on the second row.
        label (str): a title for the transformed image.

    Returns:
        The figure where the images are plotted.
    """
    # Find good boundaries for the plots.
    new_max, old_max = new.max(axis=1), old.max(axis=1)
    new_min, old_min = new.min(axis=1), old.min(axis=1)
    x_max = max((new_max[0], old_max[0])) + 1
    x_min = min((new_min[0], old_min[0])) - 1
    y_max = max((new_max[1], old_max[1])) + 1
    y_min = min((new_min[1], old_min[1])) - 1
    
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

    # Draw the original image.
    ax1.plot(old[0], old[1], 'k,')
    ax1.axis('equal')
    ax1.set_ylim([y_min, y_max])
    ax1.set_xlim([x_min, x_max])
    ax1.set_xlabel("Original", fontsize=14)

    # Draw the transformed image.
    ax2.plot(new[0], new[1], 'k,')
    ax2.axis('equal')
    ax2.set_ylim([y_min, y_max])
    ax2.set_xlim([x_min, x_max])
    ax2.set_xlabel(label, fontsize=14)
    return fig
    
def stretch():
    fig = plotOldNew(horse, solutions.dilate(horse, 1.5, 1.5), "Dilation")
    fig.savefig("stretch.pdf")
    plt.close(fig.number)

def rotate():
    fig = plotOldNew(horse, solutions.rotate(horse, np.pi/3.), "Rotation")
    fig.savefig("rotate.pdf", format="pdf")
    plt.close(fig.number)
    
def shear():
    fig = plotOldNew(horse, solutions.shear(horse, 0, 1), "Shear")
    fig.savefig("shear.pdf")
    plt.close(fig.number)
    
def reflect():
    fig = plotOldNew(horse, solutions.reflect(horse, [np.sqrt(3), 1]),
                                                                "Reflection")
    fig.savefig("reflect.pdf")
    plt.close(fig.number)
    
def translate():
    fig = plotOldNew(horse, solutions.translate(horse, (0, 2)), "Translation")
    fig.savefig("translate.pdf")
    plt.close(fig.number)
    
def combo():
    p = solutions.shear(horse, -1.02, .5)
    p = solutions.translate(p, np.array([-2, .5]))
    p = solutions.reflect(p, np.array([-2, .5]))
    
    fig = plotOldNew(horse, p, "General Affine")
    fig.savefig("combo.pdf")
    plt.close(fig.number)
    
def trajectory():
    f = solutions.plotTrajectory()
    plt.savefig('soln3.pdf')
    plt.clf()


if __name__ == "__main__":
    timing_demo()
    # matrix_multiplication_figures(10)
    # stretch()
    # rotate()
    # shear()
    # reflect()
    # translate()
    # combo()
