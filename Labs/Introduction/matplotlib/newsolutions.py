
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
    pass

if __name__ == '__main__':
    prob1()

