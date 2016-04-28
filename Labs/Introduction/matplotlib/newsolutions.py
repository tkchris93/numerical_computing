
import numpy as np
from matplotlib import pyplot as plt

def prob1():
    def var_of_means(n):
        A = np.random.randn(n,n)
        return A.mean(axis=1).var()

    y = np.array([var_of_means(n) for n in xrange(100, 1100, 100)])
    plt.plot(y)
    plt.show()

def prob2():
    x = np.linspace(-2*np.pi, 2*np.pi, 200)
    plt.plot(x, np.sin(x))
    plt.plot(x, np.cos(x))
    plt.plot(x, np.arctan(x))
    plt.show()

def prob3():
    x1, x2 = np.split(np.linspace(-2, 6, 200), [75])
    # x1, x2 = np.linspace(-2, 1, 75), np.linspace(1, 6, 125)
    plt.plot(x1, 1/(x1 - 1), 'm--', linewidth=4)
    plt.plot(x2, 1/(x2 - 1), 'm--', linewidth=4)
    plt.ylim(-6, 6)
    plt.show()

def prob4():
    x = np.linspace(-np.pi, np.pi, 200)
    
    plt.subplot(221)
    plt.plot(x, np.sin(x), linewidth=2)
    plt.xlim(-np.pi, np.pi)
    plt.ylim(-2, 2)
    plt.title(r"$\sin(x)$")

    plt.subplot(222)
    plt.plot(x, np.sin(2*x), linewidth=2)
    plt.xlim(-np.pi, np.pi)
    plt.ylim(-2, 2)
    plt.title(r"$\sin(2x)$")

    plt.subplot(223)
    plt.plot(x, 2*np.sin(2*x), linewidth=2)
    plt.xlim(-np.pi, np.pi)
    plt.ylim(-2, 2)
    plt.title(r"$2 \sin(x)$")

    plt.subplot(224)
    plt.plot(x, 2*np.sin(2*x), linewidth=2)
    plt.xlim(-np.pi, np.pi)
    plt.ylim(-2, 2)
    plt.title(r"$2 \sin(2x)$")

    plt.show()

if __name__ == '__main__':
    prob4()
