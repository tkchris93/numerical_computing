# newplots.py
"""Introductory Labs: Matploblib and Mayavi. Plotting file."""

import numpy as np
from matplotlib import pyplot as plt
# from mayavi import mlab

from functools import wraps
def _save(func):
    """Decorator for saving, clearing, and closing figures automatically."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            plt.clf()
            return func(*args, **kwargs)
        finally:
            plt.savefig(func.__name__+".pdf", format='pdf')
            plt.clf()
            plt.close('all')
    return wrapper


@_save
def basic1():
    y = np.array([i**2 for i in xrange(-5,6)])
    plt.plot(y)

@_save
def basic2():
    x = np.linspace(-5, 5, 50)
    y = x**2
    plt.plot(x, y)

@_save
def custom1():
    x = np.linspace(-2, 4, 100)
    plt.plot(x, np.exp(x), 'g:', linewidth=4, label="Exponential")
    # plt.xlabel("The x axis.")
    plt.title("This is the title.")
    plt.legend(loc="upper left")

@_save
def custom2():
    x = np.linspace(1, 4, 100)
    plt.plot(x, np.log(x), 'r+', linewidth=2)
    # plt.grid()
    plt.xlim(0, 5)
    plt.xlabel("The x axis")

@_save
def layout():
    for i in xrange(1,7):
        plt.subplot(2,3,i)
        plt.text(.44,.46,str(i),fontsize=20)
        plt.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off', top='off', left='off', right='off',
            labelbottom='off', labelleft='off') 

@_save
def subplots():
    x = np.linspace(-np.pi, np.pi, 200)
    plt.subplot(2, 1, 1)            # Draw the first subplot.
    plt.plot(x, np.sin(x), 'b', linewidth=2)
    plt.xlim(-np.pi, np.pi)
    plt.subplot(2, 1, 2)            # Draw the second subplot.
    plt.plot(x, np.cos(x), 'c', linewidth=2)
    plt.xlim(-np.pi, np.pi)

if __name__ == '__main__':
    basic1()
    basic2()
    custom1()
    custom2()
    layout()
    subplots()
