# plots.py
"""Volume I: Linear Transformations. Plotting file."""
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

def timing_demo(N=12):
    """Generates the two figures used just before Problem 1.
    """

    domain = 2**np.arange(1,N+1)
    times = []
    for n in domain:
        start = time()
        solutions.random_matrix(n)
        times.append(time() - start)

    plt.plot(domain, times, 'g.-', linewidth=2, markersize=15)
    plt.xlabel("n", fontsize=14)
    plt.ylabel("Seconds", fontsize=14)
    plt.savefig("time_random_matrix1.pdf", format="pdf")

    # Plot the dotted blue line over the green line.
    def f(x, a, b):
        return a*x**2 + b
    a, b = curve_fit(f, domain, times)[0]

    refinement = np.linspace(1, 2**N, 200)
    plt.plot(refinement, f(refinement, a, b), 'b--', lw=5)
    plt.ylabel("Seconds", fontsize=14, color="white")

    plt.savefig("time_random_matrix2.pdf", format="pdf")
    plt.clf()
    plt.close("all")

def prob1_solution(N=9):

    domain = 2**np.arange(1,N+1)
    vector_times, matrix_times = [], []

    for n in domain:
        A = solutions.random_matrix(n)
        x = solutions.random_vector(n)
        B = solutions.random_matrix(n)

        start = time()
        solutions.matrix_vector_multiplication(A, x)
        vector_times.append(time() - start)

        start = time()
        solutions.matrix_matrix_multiplication(A, B)
        matrix_times.append(time() - start)

    # Matrix-Vector Multiplication.
    plt.plot(domain, vector_times, 'b.-', lw=2, ms=15)
    plt.xlabel("n", fontsize=14); plt.ylabel("Seconds", fontsize=14)
    plt.title("Matrix-Vector Multiplication")

    plt.savefig("matrixVectorMultiplication.pdf", format="pdf")
    plt.clf()
    plt.close()

    # Matrix-Matrix Multiplication.
    plt.plot(domain, matrix_times, 'g.-', lw=2, ms=15)
    plt.xlabel("n", fontsize=14); plt.ylabel("Seconds", fontsize=14, color="w")
    plt.title("Matrix-Matrix Multiplication")

    plt.savefig("matrixMatrixMultiplication.pdf", format="pdf")
    plt.clf()
    plt.close("all")

def loglog_demo(N=9):

    domain = 2**np.arange(1, N+1)
    vec, mat = [], []

    for n in domain:
        A = solutions.random_matrix(n)
        x = solutions.random_vector(n)
        B = solutions.random_matrix(n)

        start = time()
        solutions.matrix_vector_multiplication(A, x)
        vec.append(time() - start)

        start = time()
        solutions.matrix_matrix_multiplication(A, B)
        mat.append(time() - start)

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

def draw_all():
    print("timing_demo()..."),
    timing_demo(12)
    print("done.\nprob1_solution()..."),
    prob1_solution(9)
    print("done.\nloglog_demo()..."),
    # loglog_demo()
    # stretch()
    # rotate()
    # shear()
    # reflect()
    # translate()
    # combo()


if __name__ == "__main__":
    draw_all()
