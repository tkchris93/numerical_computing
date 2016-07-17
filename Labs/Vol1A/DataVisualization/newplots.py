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

@_save("earthquake_bad.pdf")
def earthquake_bad():
    years, magnitudes, longitude, latitude = np.load("earthquakes.npy").T
    plt.plot(years, magnitudes, '.')
    plt.xlabel("Year")
    plt.ylabel("Magnitude")


if __name__ == '__main__':
    earthquake_bad()
