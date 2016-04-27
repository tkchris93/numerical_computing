# newplots.py
"""Introductory Labs: Matploblib and Mayavi. Plotting file."""

import numpy as np
from matplotlib import pyplot as plt
# from mayavi import mlab

from functools import wraps
def _clear(func):
    """Decorator for clearing and closing figures automatically."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            plt.clf()
            return func(*args, **kwargs)
        finally:
            plt.clf()
            plt.close('all')
    return wrapper


@_clear
def basic1():
    y = np.array([i**2 for i in xrange(-5,6)])
    plt.plot(y)
    plt.savefig("basic1.pdf", format='pdf')

@_clear
def basic2():
    x = np.linspace(-5, 5, 50)
    y = x**2
    plt.plot(x, y)
    plt.savefig("basic2.pdf", format='pdf')

@_clear
def custom1():
    x = np.linspace(-2, 4, 100)
    plt.plot(x, np.exp(x), 'g:', linewidth=4, label="Exponential")
    # plt.xlabel("The x axis.")
    plt.title("This is the title.")
    plt.legend(loc="upper left")
    plt.savefig("custom1.pdf", format='pdf')

@_clear
def custom2():
    x = np.linspace(1, 4, 100)
    plt.plot(x, np.log(x), 'r+', linewidth=2)
    # plt.grid()
    plt.xlim(0, 5)
    plt.xlabel("The x axis")
    plt.savefig("custom2.pdf", format='pdf')

if __name__ == '__main__':
    basic1()
    basic2()
    custom1()
    custom2()
