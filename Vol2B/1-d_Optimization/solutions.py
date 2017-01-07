# solutions.py
"""Volume 2B: 1-D Optimization. Solutions File."""

import numpy as np
from math import sqrt, exp
from scipy import optimize as opt


# Problem 1
def golden_section(f, a, b, niter=10):
    """Find the minimizer of the unimodal function f on the interval [a,b]
    using the golden section search method.

    Inputs:
        f (function): unimodal scalar-valued function on R.
        a (float): left bound of the interval of interest.
        b (float): right bound of the interval of interest.
        niter (int): number of iterations to compute.

    Returns:
        the approximated minimizer (the midpoint of the final interval).
    """
    rho = (3 - sqrt(5)) / 2.
    for _ in xrange(niter):
        aprime = a + rho*(b - a)
        bprime = a + (1 - rho)*(b - a)
        if f(aprime) > f(bprime):
            a = aprime
        else:
            b = bprime
    return (a + b) / 2.

def test_golden_section():
    return golden_section(lambda x: exp(x) - 4*x, 0, 3, niter=15)


# Problem 2
def bisection(df, a, b, niter=10):
    """Find the minimizer of the unimodal function with derivative df on the
    interval [a,b] using the bisection algorithm.

    Inputs:
        df (function): derivative of a unimodal scalar-valued function on R.
        a (float): left bound of the interval of interest.
        b (float): right bound of the interval of interest.
        niter (int): number of iterations to compute.
    """
    for _ in xrange(niter):
        mid = (b + a) / 2.
        d = df(mid)
        if d > 0:
            b = mid
        elif d < 0:
            a = mid
        else:
            return mid
    return (a + b) / 2.

def test_bisection():
    return bisection(lambda x: exp(x) - 4*x, 0, 3, niter=15)


# Problem 3
def newton1d(f, df, ddf, x, niter=10):
    """Minimize the scalar function f with derivative df and second derivative
    df using Newton's method.

    Inputs:
        f (function): A twice-differentiable scalar-valued function on R.
        df (function): The first derivative of f.
        ddf (function): The second derivative of f.
        x (float): The initial guess.
        niter (int): number of iterations to compute.

    Returns:
        The approximated minimizer.
    """
    for i in xrange(niter):
        x = x - df(x)/ddf(x)
    return x


# Problem 4
def secant1d(f, df, x0, x1, niter=10):
    """Minimize the scalar function f using the secant method.

    Inputs:
        f (function): A differentiable scalar-valued function on R.
        df (function): The first derivative of f.
        x (float): The initial guess.
        niter (int): number of iterations to compute.

    Returns:
        The approximated minimizer.
    """
    for i in range(niter):
        x0, x1 = x1, x1 - (x1 - x0) / (df(x1) - df(x0)) * df(x1)
    return x1


# Problem 5
def backtracking(f, slope, x, p, a=1, rho=.9, c=10e-4):
    """Do a backtracking line search to satisfy the Wolfe Conditions.
    Return the step length.

    Inputs:
        f (function): A scalar-valued function on R.
        slope (float): The derivative of f at x.
        x (float): The current approximation to the minimizer.
        p (float): The current search direction.
        a (float): Initial step length (set to 1 in Newton and quasi-Newton
            methods).
        rho (float): Parameter in (0,1).
        c (float): Parameter in (0,1).

    Returns:
        The computed step size.
    """
    b = f(x)
    while f(x + a*p) > b + c*a*slope:
        a = rho*a
    return a
