# newplots.py
"""Volume I: Data Visualization. Plotting file."""

from __future__ import print_function
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../../matplotlibrc')

# Decorator ===================================================================

from matplotlib import colors, pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from functools import wraps
from sys import stdout
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
                if extension == "pdf":
                    plt.savefig("figures/"+filename, format='pdf')
                elif extension == "png":
                    plt.savefig("figures/"+filename, format='png',
                                                    size=(1024,768))
                print("done.")
                return out
            except Exception as e:
                print("\n\t", e, sep='')
            finally:
                plt.clf()
                plt.close('all')
        return wrapper
    return decorator

# Plots =======================================================================

import numpy as np

# Problem 2 -------------------------------------------------------------------

@_save("line_vs_scatter_line.pdf")
def line_vs_scatter_line():
    x = np.linspace(0, 4, 8)
    data = x**2
    plt.plot(x, data, 'b-', linewidth=2)
    return x, data

@_save("line_vs_scatter_scat.pdf")
def line_vs_scatter_scat(x, data):
    plt.plot(x, data, 'g.', markersize=15)

@_save("line_vs_scatter_both.pdf")
def line_vs_scatter_both(x, data):
    plt.plot(x, data, 'r.-', linewidth=2, markersize=15)


@_save("clean_histogram.pdf")
def clean_histogram(data):
    plt.hist(data, bins=30, lw=0, histtype="stepfilled")
    plt.tick_params(axis="y", which="both", left='off', labelleft='off')

@_save("line_vs_histogram_bad.pdf")
def line_vs_histogram_bad(N):
    data = np.random.beta(2, 4, size=N)
    plt.plot(data)
    return data

@_save("line_vs_histogram_hist.pdf")
def line_vs_histogram_hist(data):
    plt.hist(data, bins=30)

@_save("line_vs_histogram_line.pdf")
def line_vs_histogram_line(data):
    freq, bin_edges = np.histogram(data, bins=30)
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2.
    plt.hist(data, bins=30, alpha=.1)
    plt.plot(bin_centers, freq, 'g.-', ms=12)

@_save("earthquake_bad.pdf")
def earthquake_bad():
    years, magnitudes, longitude, latitude = np.load("earthquakes.npy").T
    plt.plot(years, magnitudes, '.')
    plt.xlabel("Year")
    plt.ylabel("Magnitude")

def prob2():
    # x, data = line_vs_scatter_line()
    # line_vs_scatter_scat(x, data)
    # line_vs_scatter_both(x, data)

    data = line_vs_histogram_bad(10000)
    clean_histogram(data)
    line_vs_histogram_hist(data)
    line_vs_histogram_line(data)

    # earthquake_bad()

# Problem 3 -------------------------------------------------------------------

@_save("rosenbrock.pdf")
def rosenbrock():
    fig = plt.figure()
    ax = Axes3D(fig, azim = -128, elev = 43)
    x = np.linspace(-2, 2, 50)
    y = np.linspace(-1, 3, 50)
    X, Y = np.meshgrid(x, y)
    Z = (1.-X)**2 + 100.*(Y-X**2)**2
    ax.plot_surface(X, Y, Z, rstride = 1, cstride = 1, cmap="viridis", linewidth=0, edgecolor='none', norm=colors.LogNorm())

    ax.set_xlim([-2, 2.0])
    ax.set_ylim([-1, 3.0])
    ax.set_zlim([0, 2500])

    plt.xlabel("x")
    plt.ylabel("y")

if __name__ == '__main__':
    prob2()
    # rosenbrock()
