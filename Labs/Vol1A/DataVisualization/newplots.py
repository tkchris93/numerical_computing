# newplots.py
"""Volume I: Data Visualization. Plotting file."""

from __future__ import print_function
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../../matplotlibrc')

# Decorator ===================================================================

from matplotlib import pyplot as plt
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

@_save("line_bad.pdf")
def lineplot_bad(N):
    data = np.random.exponential(size=N)
    plt.plot(data)
    return data

@_save("histogram_good.pdf")
def histogram_bad(data):
    plt.hist(data, bins=30)

@_save("earthquake_bad.pdf")
def earthquake_bad():
    years, magnitudes, longitude, latitude = np.load("earthquakes.npy").T
    plt.plot(years, magnitudes, '.')
    plt.xlabel("Year")
    plt.ylabel("Magnitude")


@_save("histogram_line.pdf")
def histogram_line(data):
    freq, bin_edges = np.histogram(data, bins=30)
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2.
    plt.hist(data, bins=30, alpha=.1)
    plt.plot(bin_centers, freq, 'b.-', ms=12)


def prob2():
    data = lineplot_bad(10000)
    histogram_bad(data)
    histogram_line(data)
    # earthquake_bad()

if __name__ == '__main__':
    prob2()
