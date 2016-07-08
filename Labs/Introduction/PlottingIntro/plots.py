# newplots.py
"""Introductory Labs: Matploblib and Mayavi. Plotting file."""

import numpy as np
from matplotlib import pyplot as plt
from mayavi import mlab

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import widgets as wg

from functools import wraps

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
                print("{:.<25}".format(func.__name__+'()'), end='')
                stdout.flush()
                plt.clf()
                out = func(*args, **kwargs)
                if extension == "pdf":
                    plt.savefig(filename, format='pdf')
                elif extension == "png":
                    plt.savefig(filename, format='png', size=(1024, 768))
                print("done.")
                return out
            except Exception as e:
                print("\n", e, sep='')
            finally:
                plt.clf()
                plt.close('all')
        return wrapper
    return decorator


@_save("basic1.pdf")
def basic1():
    y = np.array([i**2 for i in xrange(-5,6)])
    plt.plot(y)

@_save("basic2.pdf")
def basic2(n=50):
    x = np.linspace(-5, 5, n)
    y = x**2
    plt.plot(x, y)

@_save("custom1.pdf")
def custom1(n=100):
    x = np.linspace(-2, 4, n)
    plt.plot(x, np.exp(x), 'g:', linewidth=4, label="Exponential")
    # plt.xlabel("The x axis.")
    plt.title("This is the title.", fontsize=18)
    plt.legend(loc="upper left")

@_save("custom2.pdf")
def custom2(n=100):
    x = np.linspace(1, 4, n)
    plt.plot(x, np.log(x), 'r+', linewidth=2)
    # plt.grid()
    plt.xlim(0, 5)
    plt.xlabel("The x axis")

@_save("layout.pdf")
def layout():
    for i in xrange(1,7):
        plt.subplot(2,3,i)
        plt.text(.44,.46,str(i),fontsize=20)
        plt.tick_params(
            axis='both',       # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off', top='off', left='off', right='off',
            labelbottom='off', labelleft='off')

@_save("subplots.pdf")
def subplots(n=200):
    x = np.linspace(-np.pi, np.pi, n)
    plt.subplot(2, 1, 1)            # Draw the first subplot.
    plt.plot(x, np.sin(x), 'b', linewidth=2)
    plt.xlim(-np.pi, np.pi)
    plt.subplot(2, 1, 2)            # Draw the second subplot.
    plt.plot(x, np.cos(x), 'c', linewidth=2)
    plt.xlim(-np.pi, np.pi)

@_save("scatter.pdf")
def scatter():
    x = np.random.randint(1, 11, 20)
    y = np.random.randint(1, 11, 20)

    # Draw two histograms and a scatter plot to display the data.
    plt.hist(x, bins=10, range=[.5, 10.5])
    plt.savefig("histogram.pdf", format='pdf')
    plt.clf()

    plt.scatter(x, y, s=100)

@_save("sinxsiny.png")
def sinxsiny(n=201):
    x = np.linspace(-np.pi, np.pi, n)
    y = x.copy()
    X, Y = np.meshgrid(x, y)

    plt.pcolormesh(X, Y, np.sin(X) * np.sin(Y))
                        # edgecolors='face', shading='flat')
    plt.colorbar()
    plt.xlim(-np.pi, np.pi); plt.ylim(-np.pi, np.pi)

@_save("sinxsiny_3d.pdf")
def sinxsiny_3d():
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x = np.linspace(-np.pi, np.pi, 101)
    y = x.copy()
    X, Y = np.meshgrid(x, y)
    ax.view_init(elev=26, azim=-76)
    ax.plot_surface(X, Y, np.sin(X)*np.sin(Y))

@_save("pcolor2.png")
def pcolor2(n=200):
    x = np.linspace(-2*np.pi, 2*np.pi, n)
    y = np.copy(x)
    X, Y = np.meshgrid(x,y)
    Z = np.sin(X)*np.sin(Y)/(X*Y)

    plt.pcolormesh(X, Y, Z, cmap="Spectral")
    plt.colorbar()
    plt.xlim(-2*np.pi, 2*np.pi)
    plt.ylim(-2*np.pi, 2*np.pi)

def widget_plot():
    ax = plt.subplot(111)
    plt.subplots_adjust(bottom=.25)
    t = np.arange(0., 1., .001)
    a0 = 5.
    f0 = 3.
    s = a0 * np.sin(2 * np.pi * f0 * t)
    l = plt.plot(t, s)[0]
    plt.axis([0, 1, -10, 10])
    axfreq = plt.axes([.25, .05, .65, .03])
    axamp = plt.axes([.25, .1, .65, .03])
    sfreq = wg.Slider(axfreq, 'Freq', .1, 30., valinit=f0)
    samp = wg.Slider(axamp, 'Amp', .1, 10., valinit=a0)
    def update(val):
        amp = samp.val
        freq = sfreq.val
        l.set_ydata(amp * np.sin(2 * np.pi * freq * t))
        plt.draw()
    sfreq.on_changed(update)
    samp.on_changed(update)
    plt.show()

def save_all():
    basic1()
    basic2()
    custom1()
    custom2()
    layout()
    subplots()
    scatter()
    sinxsiny()
    sinxsiny_3d()

if __name__ == '__main__':
    save_all()
    widget_plot()
