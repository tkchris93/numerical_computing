# newplots.py
"""Introductory Labs: Matploblib and Mayavi. Plotting file."""

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
def basic2(n=50):
    x = np.linspace(-5, 5, n)
    y = x**2
    plt.plot(x, y)

@_save
def custom1(n=100):
    x = np.linspace(-2, 4, n)
    plt.plot(x, np.exp(x), 'g:', linewidth=4, label="Exponential")
    # plt.xlabel("The x axis.")
    plt.title("This is the title.", fontsize=18)
    plt.legend(loc="upper left")

@_save
def custom2(n=100):
    x = np.linspace(1, 4, n)
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
def subplots(n=200):
    x = np.linspace(-np.pi, np.pi, n)
    plt.subplot(2, 1, 1)            # Draw the first subplot.
    plt.plot(x, np.sin(x), 'b', linewidth=2)
    plt.xlim(-np.pi, np.pi)
    plt.subplot(2, 1, 2)            # Draw the second subplot.
    plt.plot(x, np.cos(x), 'c', linewidth=2)
    plt.xlim(-np.pi, np.pi)

@_save
def scatter():
    x = np.random.randint(1, 11, 20)
    y = np.random.randint(1, 11, 20)

    # Draw two histograms and a scatter plot to display the data.
    plt.hist(x, bins=10, range=[.5, 10.5])
    plt.savefig("histogram.pdf", format='pdf')
    plt.clf()

    plt.scatter(x, y, s=100)

# @_save
def sinxsiny(n=201):
    x = np.linspace(-np.pi, np.pi, n) 
    y = x.copy()
    X, Y = np.meshgrid(x, y)

    plt.pcolormesh(X, Y, np.sin(X) * np.sin(Y))
                        # edgecolors='face', shading='flat')
    plt.colorbar()
    plt.xlim(-np.pi, np.pi); plt.ylim(-np.pi, np.pi)
    plt.savefig("sinxsiny.png", size=(1024, 768))
    plt.clf()
    
@_save
def sinxsiny_3d():
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x = np.linspace(-np.pi, np.pi, 101)
    y = x.copy()
    X, Y = np.meshgrid(x, y)
    ax.view_init(elev=26, azim=-76)
    ax.plot_surface(X, Y, np.sin(X)*np.sin(Y))

def cmeshprob(n=200):
    x = np.linspace(-2*np.pi, 2*np.pi, n)
    y = np.copy(x)
    X, Y = np.meshgrid(x,y)
    Z = np.sin(X)*np.sin(Y)/(X*Y)

    plt.pcolormesh(X, Y, Z, cmap="Spectral")
    plt.colorbar()
    plt.xlim(-2*np.pi, 2*np.pi)
    plt.ylim(-2*np.pi, 2*np.pi)
    plt.savefig("pcolor2.png", size=(1024, 768))
    plt.clf()


if __name__ == '__main__':
    basic1()
    basic2()
    custom1()
    custom2()
    layout()
    subplots()
    scatter()
    sinxsiny()
    sinxsiny_3d()
    cmeshprob()
