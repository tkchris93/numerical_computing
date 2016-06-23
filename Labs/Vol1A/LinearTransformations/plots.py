# plots.py
"""Volume I: Linear Transformations. Plotting file."""
from __future__ import print_function
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../../matplotlibrc')

from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from random import random
from sys import stdout
from time import time
import numpy as np
import solutions

# Complexity Pictures =========================================================

def timing_demo(N=12):
    """Generate the two figures used just before Problem 1."""

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
    """Generate the two figures used at the end of Problem 1."""

    domain = 2**np.arange(1,N+1)
    vector_times, matrix_times = [], []

    for n in domain:
        A = solutions.random_matrix(n)
        x = solutions.random_vector(n)
        B = solutions.random_matrix(n)

        start = time()
        solutions.matrix_vector_product(A, x)
        vector_times.append(time() - start)

        start = time()
        solutions.matrix_matrix_product(A, B)
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

    return domain, vector_times, matrix_times

def loglog_demo(domain, vector_times, matrix_times):
    """Generate the two figures between Problem 1 and Problem 2."""

    plt.plot(domain, vector_times, 'b.-', lw=2, ms=15, label="Matrix-Vector")
    plt.plot(domain, matrix_times, 'g.-', lw=2, ms=15, label="Matrix-Matrix")
    plt.legend(loc="upper left")
    plt.savefig("loglogDemoBad.pdf", format="pdf")
    plt.clf()
    plt.close("all")

    plt.loglog(domain, vector_times, 'b.-', basex=2, basey=2, lw=2, ms=15)
    plt.loglog(domain, matrix_times, 'g.-', basex=2, basey=2, lw=2, ms=15)
    plt.savefig("loglogDemoGood.pdf", format="pdf")
    plt.clf()
    plt.close("all")

def timing_drawings():
    print("timing_demo()...", end=''); stdout.flush()
    timing_demo(12)
    print("done.\nprob1_solution()...", end=''); stdout.flush()
    a, b, c = prob1_solution(9)
    print("done.\nloglog_demo()...", end=''); stdout.flush()
    loglog_demo(a, b, c)
    print("done.")

# Horse Pictures ==============================================================

horse = np.load("horse.npy")[:,::5]

def save_horse(data, title):
    plt.clf()
    plt.plot(data[0], data[1], 'k,')
    plt.title(title, fontsize=14)
    plt.axis([-1,1,-1,1])
    plt.gca().set_aspect("equal")
    plt.savefig("{}Horse.pdf".format(title), format="pdf")
    plt.clf()
    plt.close("all")

def original_horse():
    save_horse(horse, "Original")

def dilated_horse():
    dilation = np.dot([[.5,0],[0,1.5]], horse)
    save_horse(dilation, "Dilation")

def rotated_horse():
    theta = np.pi/3.
    rotation = np.dot([[np.cos(theta),-np.sin(theta)],
                       [np.sin(theta),np.cos(theta)]], horse)
    save_horse(rotation, "Rotation")

def sheared_horse():
    shear = np.dot([[1, .2],[.2, 1]], horse)
    save_horse(shear, "Shear")

def reflected_horse():
    l1, l2 = 0, 1
    reflection = np.dot(np.array([[l1**2 - l2**2, 2*l1*l2],
                            [2*l1*l2, l2**2 - l1**2]])/(l1**2 + l2**2), horse)
    save_horse(reflection, "Reflection")

def translated_horse():
    translation = horse + np.vstack([.25, .25])
    save_horse(translation, "Translation")

def combo_horse():      # TODO
    p = solutions.shear(horse, -1.02, .5)
    p = solutions.translate(p, np.array([-2, .5]))
    p = solutions.reflect(p, np.array([-2, .5]))

    fig = plotOldNew(horse, p, "General Affine")
    fig.savefig("combo.pdf")
    plt.close(fig.number)


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

def horse_drawings():
    print("original_horse()...", end=''),; stdout.flush()
    original_horse()
    print("done.\ndilated_horse()...", end=''),; stdout.flush()
    dilated_horse()
    print("done.\nrotated_horse()...", end=''),; stdout.flush()
    rotated_horse()
    print("done.\nsheared_horse()...", end=''),; stdout.flush()
    sheared_horse()
    print("done.\nreflected_horse()...", end=''),; stdout.flush()
    reflected_horse()
    print("done.\ntranslated_horse()...", end=''),; stdout.flush()
    translated_horse()
    print("done.\n", end=''),; stdout.flush()
    # combo()

# =============================================================================

def draw_all():
    timing_drawings()
    horse_drawings()

if __name__ == "__main__":
    # draw_all()
    horse_drawings()
