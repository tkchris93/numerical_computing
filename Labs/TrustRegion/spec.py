# Name this file 'solutions.py
from scipy import linalg as la
import numpy as np

# problem 1
def trustRegion(f,grad,hess,subprob,x0,r0,rmax,eta,gtol=1e-5):
    """Implement the trust regions method.  
    
    Parameters:
        f : callable function object
            The objective function to minimize.
        g : callable function object
            The gradient (or approximate gradient) of the objective function
        hess : callable function object
            The hessian (or approximate hessian) of the objective function
        subprob: callable function object
            Returns the step p_k
        x0 : numpy array of shape (n,)
            The initial point
        r0 : float
            The initial trust-region radius
        rmax : float
            The max value for trust-region radii
        eta : float in [0,0.25)
            Acceptance threshold
        gtol : float
            Convergence threshold
        
    
    Returns:
        x : the minimizer of f
    Notes
    -----
    The functions f, g, and hess should all take a single parameter.
    The function subprob takes as parameters a gradient vector, hessian
         matrix, and radius.
    """
        
    raise NotImplementedError("Problem 1 Incomplete")

# problem 2   
def dogleg(gk,Bk,rk):
    """Calculate the dogleg minimizer of the quadratic model function.
    
    Parameters:
        gk : ndarray of shape (n,)
            The current gradient of the objective function
        Bk : ndarray of shape (n,n)
            The current (or approximate) hessian
        rk : float
            The current trust region radius
    Returns:
        pk : ndarray of shape (n,)
            The dogleg minimizer of the model function.
    """
    raise NotImplementedError("Problem 2 Incomplete")