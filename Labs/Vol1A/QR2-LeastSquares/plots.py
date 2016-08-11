# plots.py
"""Volume I: QR 2 (Least Squares and Eigenvalues). Plotting file."""
from __future__ import print_function
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../../matplotlibrc')

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

# Figures =====================================================================

import numpy as np
from scipy.stats import linregress

@_save("line_fit_example.pdf")
def line():
    x = np.linspace(0, 10, 20)
    y = .5*x - 3 + np.random.randn(20)
    m, b = linregress(x, y)[:2]

    plt.plot(x, y, 'k*', label="Data Points")
    plt.plot(x, m*x + b, 'b-', lw=2, label="Least Squares Fit")
    plt.legend(loc="upper left")

# =============================================================================

def draw_all():
    line()

if __name__ == "__main__":
    draw_all()
