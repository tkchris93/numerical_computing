'''
Solutions file for the line search lab.
'''
import numpy as np
import scipy.optimize as opt

def goldenSection(f, a, b, niter=10):
    '''
    Perform a Golden Section Search on the objective function.
    Inputs:
        f -- unimodal objective function
        a -- left bound of the interval
        b -- right bound of the interval
        niter -- integer, number of iterations
    Returns:
        the approximated minimizer
    '''
    rho = 0.5 * (3 - np.sqrt(5))
    for i in range(niter):
        aprime = a + rho * (b-a)
        bprime = a + (1-rho) * (b-a)
        fa = f(aprime)
        fb = f(bprime)
        if fa > fb:
            a = aprime
        else:
            b = bprime
    return (a+b)/2.

def bisection(df, a, b, niter=10):
    '''
    Perform a Bisection Method Search on the objective function.
    Inputs:
        df -- derivative of unimodal objective function
        a -- left bound of the interval
        b -- right bound of the interval
        niter -- integer, number of iterations
    Returns:
        the approximated minimizer
    '''
    for i in range(niter):
        mid = (b+a)/2.
        d = df(mid)
        if d > 0:
            b = mid
        elif d < 0:
            a = mid
        else:
            return mid
    return (a+b)/2.


def newton1d(f, df, ddf, x, niter=10):
    '''
    Perform Newton's method to minimize a function from R to R.
    
    Parameters
    ----------
    f : callable function object 
        The objective function (twice differentiable)
    df : callable function object 
        The first derivative
    ddf : callable function object
        The second derivative
    x : float
        The initial guess
    niter : integer
        The number of iterations
        
    Returns
    ------
        min : float
            The approximated minimizer
    '''
    for i in xrange(niter):
        x = x-df(x)/ddf(x)
    return x

def secant1d(f, df, x0, x1, niter=10):
    '''
    Perform the Secant method to minimize a function from R to R.
    
    Parameters
    ----------
    f : callable function object 
        The objective function (twice differentiable)
    df : callable function object 
        The first derivative
    x : float
        The initial guess
    niter : integer
        The number of iterations
        
    Returns
    ------
        min : float
            The approximated minimizer
    '''
    for i in range(niter):
        x0, x1 = x1, x1 - (x1 - x0) / (df(x1) - df(x0)) * df(x1)
    return x1
    
def backtracking(f, slope, x, p, a=1, rho=.9, c=10e-4):
    '''
    Perform a backtracking line search to satisfy the Wolfe Conditions.
    Return the step length.
    Inputs:
        f -- the objective function
        df -- the the first derivative of the objective function
        x -- current iterate
        p -- current direction
        a -- intial step length (set to 1 in Newton and quasi-Newton methods)
        rho -- number in (0,1)
        c -- number in (0,1)
    Returns:
        the computed step size
    '''
    b = f(x)
    while f(x+a*p) > b + c*a*slope:
        a = rho*a
    return a