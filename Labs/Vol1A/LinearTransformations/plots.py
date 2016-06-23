# plots.py
"""Volume I: Linear Transformations. Plotting file."""
from __future__ import print_function
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../../matplotlibrc')

from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from functools import wraps
from timeit import timeit
from random import random
from sys import stdout
from time import time
import numpy as np
import solutions


def _save(filename):
    """Decorator for saving, clearing, and closing figures automatically."""
    try:
        name, extension = filename.split(".")
    except (ValueError, TypeError) as e:
        raise ValueError("Invalid file name '{}'".format(filename))
    if extension not in {"pdf", "png"}:
        raise ValueError("Invalid file extension '{}'".format(extension))

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print("{:.<20}".format(func.__name__+'()'), end='')
                stdout.flush()
                plt.clf()
                out = func(*args, **kwargs)
                if extension == "pdf":
                    plt.savefig(filename, format='pdf')
                elif extension == "png":
                    plt.savefig(filename, format='png')
                print("done.")
                return out
            except Exception as e:
                print("\n", e, sep='')
            finally:
                plt.clf()
                plt.close('all')
        return wrapper
    return decorator

# Timing Pictures =============================================================

@_save("time_random_matrix2.pdf")
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
    plt.ylim(ymin=0)
    plt.ylabel("Seconds", fontsize=14, color="white")

@_save("matrixMatrixMultiplication.pdf")
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

    return domain, vector_times, matrix_times

@_save("loglogDemoGood.pdf")
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

@_save("cachingDemo.pdf")
def caching_demo():

    sizes = 2**np.arange(2,19,.2)
    times = []
    for size in sizes:
        A, B = np.random.random((2, size))
        def func():
            np.dot(A,B)
        times.append(timeit(func, number=50) / 50.)

    plt.loglog(sizes[1:], times[1:], basex=2, basey=2, lw=2, ms=15)
    plt.ylabel("Seconds")
    plt.xlabel("n")

def timing_drawings():
    timing_demo(12)
    a, b, c = prob1_solution(8)
    loglog_demo(a, b, c)
    caching_demo()

# Horse Pictures ==============================================================

horse = np.load("horse.npy")[:,::5]

def save_horse(data, title):
    plt.clf()
    plt.plot(data[0], data[1], 'k,')
    plt.title(title, fontsize=18)
    plt.axis([-1,1,-1,1])
    plt.gca().set_aspect("equal")
    plt.savefig("{}Horse.pdf".format(title), format="pdf")
    plt.clf()
    plt.close("all")

def original_horse():
    save_horse(horse, "Original")

def dilated_horse():
    dilation = np.dot([[1.25,0],[0,.25]], horse)
    save_horse(dilation, "Dilation")

def rotated_horse():
    theta = np.pi/3.
    rotation = np.dot([[np.cos(theta),-np.sin(theta)],
                       [np.sin(theta),np.cos(theta)]], horse)
    save_horse(rotation, "Rotation")

def sheared_horse():
    shear = np.dot([[1, .2],[0, 1]], horse)
    save_horse(shear, "Shear")

def reflected_horse():
    l1, l2 = 0, 1
    reflection = np.dot(np.array([[l1**2 - l2**2, 2*l1*l2],
                            [2*l1*l2, l2**2 - l1**2]])/(l1**2 + l2**2), horse)
    save_horse(reflection, "Reflection")

def translated_horse():
    translation = horse + np.vstack([.25, .25])
    save_horse(translation, "Translation")

def combo_horse():
    shear = np.dot([[1, -1.02],[.5, 1]], horse)
    trans = shear + np.vstack([.25, -.25])
    l1, l2 = -2, .5
    refle = np.dot(np.array([[l1**2 - l2**2, 2*l1*l2],
                            [2*l1*l2, l2**2 - l1**2]])/(l1**2 + l2**2), trans)
    save_horse(refle, "Combo")

@_save("trajectory.pdf")
def trajectory():
    direction = np.array(direction)
    T = np.linspace(time[0],time[1],100)
    start_P1 = [1,0]
    posP1_x = []
    posP1_y = []

    for t in T:
        posP2 = speed*t*direction/la.norm(direction)
        posP1 = translate2D(rotate2D(start_P1, t*omega), posP2)[0]
        posP1_x.append(posP1[0])
        posP1_y.append(posP1[1])

    plt.plot(posP1_x, posP1_y)
    plt.gca().set_aspect('equal')


def horse_drawings():
    def execute(func):
        print("{:.<20}".format(func.__name__+'()'), end='')
        stdout.flush()
        func()
        print("done.")
    for f in [original_horse, dilated_horse, rotated_horse, sheared_horse,
              reflected_horse, translated_horse, combo_horse]:
        execute(f)

# =============================================================================

def draw_all():
    timing_drawings()
    horse_drawings()

if __name__ == "__main__":
    draw_all()
