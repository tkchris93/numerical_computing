# solutions.py
"""Lab 16: Gaussian Quadrature. Solutions file."""

import numpy as np
from math import sqrt
from scipy.stats import norm
from scipy import linalg as la
from scipy.integrate import quad
from matplotlib import pyplot as plt


# Problem 1
def shift(f, a, b, plot=False):
    """Shift the function f on [a, b] to a new function g on [-1, 1] such that
    the integral of f from a to b is equal to the integral of g from -1 to 1.

    Inputs:
        f (function): a scalar-valued function on the reals.
        a (int): the left endpoint of the interval of integration.
        b (int): the right endpoint of the interval of integration.
        plot (bool): if True, plot f over [a,b] and g over [-1,1] in separate
            subplots.

    Returns:
        The new, shifted function.
    """
    # Define g.
    g = lambda x: f((b - a)*x/2. + (a + b)/2.)

    if plot is True:

        plt.subplot(121)    # Plot f(x) over [a,b]
        x1 = np.linspace(a, b, 200)
        plt.plot(x1, f(x1), 'b-', lw=2)
        plt.title(r"$f(x)$ on $[{}, {}]$".format(a,b))

        plt.subplot(122)    # Plot g(x) over [-1,1]
        x2 = np.linspace(-1, 1, 200)
        plt.plot(x2, g(x2), 'g-', lw=2)
        plt.title(r"$g(x)$ on $[-1, 1]$")

        plt.show()

    return g


# Problem 2
def estimate_integral(f, a, b, points, weights):
    """Estimate the value of the integral of the function f over [a,b].

    Inputs:
        f (function): a scalar-valued function on the reals.
        a (int): the left endpoint of the interval of integration.
        b (int): the right endpoint of the interval of integration.
        points ((n,) ndarray): an array of n sample points.
        weights ((n,) ndarray): an array of n weights.

    Returns:
        The approximate integral of f over [a,b].
    """
    return (b - a) * np.dot(weights, shift(f, a, b, False)(points)) / 2.


# Problem 3
def construct_jacobi(gamma, alpha, beta):
    """Construct the Jacobi matrix."""
    a = - beta / alpha
    b = np.sqrt(gamma[1:] / (alpha[:-1] * alpha[1:]))

    J = np.diag(a)
    B = np.diag(b)
    J[:-1,1:] += B
    J[1:,:-1] += B

    return J


# Problem 4
def points_and_weights(n):
    """Calculate the points and weights for a quadrature over [a,b] with n
    points.

    Returns:
        points ((n,) ndarray): an array of n sample points.
        weights ((n,) ndarray): an array of n weights.
    """

    # Calculate the recurrence coefficients.
    gamma = np.array([(k-1)/float(k) for k in xrange(1,n+1)])
    alpha = np.array([(2*k - 1)/float(k) for k in xrange(1,n+1)])
    beta = np.zeros(n)

    # Get the eigenvalues of the Jacobian.
    J = construct_jacobi(gamma, alpha, beta)
    eigs, vecs = la.eig(J)

    # Get the points and weights from the Jacobi eigenvalues and eigenvectors.
    points = eigs
    weights = 2 * vecs[0]**2
    return points.real, weights.real


# Problem 5
def gaussian_quadrature(f, a, b, n):
    """Using the functions from the previous problems, integrate the function
    'f' over the domain [a,b] using 'n' points in the quadrature.
    """
    points, weights = points_and_weights(n)
    return estimate_integral(f, a, b, points, weights)


# Problem 6
def normal_cdf(x):
    """Use scipy.integrate.quad() to compute the CDF of the standard normal
    distribution at the point 'x'. That is, compute P(X <= x), where X is a
    normally distributed random variable with mean = 0 and std deviation = 1.
    """
    return quad(norm.pdf, -5, x)[0]

