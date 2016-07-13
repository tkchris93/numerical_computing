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
import os

def _save(filename):
    """Decorator for saving, clearing, and closing figures automatically."""
    try:
        name, extension = filename.split(".")
    except (ValueError, TypeError) as e:
        raise ValueError("Invalid file name '{}'".format(filename))
    if extension not in {"pdf", "png"}:
        raise ValueError("Invalid file extension '{}'".format(extension))
    if not os.path.isdir("figures"):
        os.mkdir("figures")


    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                print("{:.<40}".format(filename), end='')
                stdout.flush()
                plt.clf()
                out = func(*args, **kwargs)
                plt.savefig("figures/"+filename, format=extension)
                print("done.")
                return out
            except Exception as e:
                print("\n\t", e, sep='')
            finally:
                plt.clf()
                plt.close('all')
        return wrapper
    return decorator

# Horse Pictures ==============================================================

horse = np.load("horse.npy")[:,::10]

def save_horse(data, title, top=True):
    plt.clf()
    plt.plot(data[0], data[1], 'k,')
    if top:
        plt.title(title, fontsize=24)
    else:
        plt.xlabel(title, fontsize=24)
    plt.tick_params(
        axis='both',       # changes apply to both axes
        which='both',      # both major and minor ticks are affected
        bottom='off', top='off', left='off', right='off',
        labelbottom='off', labelleft='off')
    plt.axis([-1,1,-1,1])
    plt.gca().set_aspect("equal")
    plt.savefig("figures/{}Horse.pdf".format(title), format="pdf")
    plt.clf()
    plt.close("all")

def original_horse():
    save_horse(horse, "Original")

def stretched_horse(data=horse, save=True):
    dilation = np.dot([[.5,0],[0,1.2]], data)
    if save:
        save_horse(dilation, "Stretch")
    return dilation

def sheared_horse(data=horse, save=True):
    shear = np.dot([[1, .5],[0, 1]], data)
    if save:
        save_horse(shear, "Shear")
    return shear

def reflected_horse(data=horse, save=True):
    l1, l2 = 0, 1
    reflection = np.dot(np.array([[l1**2 - l2**2, 2*l1*l2],
                            [2*l1*l2, l2**2 - l1**2]])/(l1**2 + l2**2), data)
    if save:
        save_horse(reflection, "Reflection", top=False)
    return reflection

def rotated_horse(data=horse, save=True):
    theta = np.pi/2.
    rotation = np.dot([[np.cos(theta),-np.sin(theta)],
                       [np.sin(theta),np.cos(theta)]], data)
    if save:
        save_horse(rotation, "Rotation", top=False)
    return rotation

def combo_horse(data=horse):
    data = stretched_horse(data, save=False)
    data = sheared_horse(data, save=False)
    data = reflected_horse(data, save=False)
    data = rotated_horse(data, save=False)
    save_horse(data, "Composition", top=False)

def translated_horse():
    translation = horse + np.vstack([.75, .5])
    save_horse(translation, "Translation")

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

@_save("SolarSystem.pdf")
def solar_system(T=3*np.pi/2, omega_e=1, omega_m=13, N=400):
    time = np.linspace(0, T, N)
    earth, moon = [np.array([10,0])], [np.array([11,0])]

    def rotation(theta):
        return np.array([[np.cos(theta),-np.sin(theta)],
                         [np.sin(theta),np.cos(theta)]])

    for t in time[1:]:
        earth.append(rotation(t*omega_e).dot(earth[0]))
        moon.append(rotation(t*omega_m).dot([1, 0]) + earth[-1])

    earth = np.transpose(earth)
    moon = np.transpose(moon)

    plt.plot(earth[0], earth[1], label="Earth", lw=2)
    plt.plot(moon[0], moon[1], label="Moon", lw=2)
    plt.xlabel("x"); plt.ylabel("y")
    plt.gca().set_aspect("equal")
    plt.legend(loc="upper left")


def horse_drawings():
    for func in [original_horse, stretched_horse, sheared_horse, rotated_horse,
                 reflected_horse, combo_horse, translated_horse]:
        print("{:.<40}".format(func.__name__+'()'), end='')
        stdout.flush()
        func()
        print("done.")
    solar_system()

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
    plt.savefig("figures/time_random_matrix1.pdf", format="pdf")

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

    plt.savefig("figures/matrixVectorMultiplication.pdf", format="pdf")
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
    plt.savefig("figures/loglogDemoBad.pdf", format="pdf")
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
            A + B
        times.append(timeit(func, number=50) / 50.)

    plt.loglog(sizes[1:], times[1:], basex=2, basey=2, lw=2, ms=15)
    plt.ylabel("Seconds")
    plt.xlabel("n")


def timing_drawings():
    timing_demo(12)
    a, b, c = prob1_solution(8)
    loglog_demo(a, b, c)
    caching_demo()

# =============================================================================

def draw_all():
    horse_drawings()
    timing_drawings()

if __name__ == "__main__":
    draw_all()
