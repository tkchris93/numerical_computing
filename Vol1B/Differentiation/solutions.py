# solutions.py
"""Volume 1B: Differentiation. Solutions file."""


import numpy as np
from scipy import linalg as la
from matplotlib import pyplot as plt


# Problem 1
def centered_difference_quotient(f, pts, h=1e-5):
    """Compute the centered difference quotient for function (f)
    given points (pts).

    Inputs:
        f (function): the function for which the derivative will be
            approximated.
        pts (array): array of values to calculate the derivative.

    Returns:
        An array of the centered difference quotient.
    """
    Df_app = lambda x: .5*(f(x+h)-f(x-h)) / h
    return Df_app(pts)

# Problem 2
def calculate_errors(f,df,pts,h = 1e-5):
    """Compute the errors using the centered difference quotient approximation.

    Inputs:
        f (function): the function for which the derivative will be
            approximated.
        pts (array): array of values to calculate the derivative

    Returns:
        errors (array): array of the errors for the centered difference
            quotient approximation.
    """
    return np.absolute(df(pts) - centered_difference_quotient(f, pts))

# Problem 3
def Prob3():
    """Use the centered difference quotient to approximate the derivative of
        f(x)=(sin(x)+1)^x at x= pi/3, pi/4, and pi/6.
        Then compute the error of each approximation
        
    Returns:
        (derivative approximations, errors) (tuple): a tuple of one array of the derivative
        approximations and another array of the errors of the approximations
    """
    f = lambda x: (np.sin(x)+1)**x
    pts = np.array([np.pi/3, np.pi/4, np.pi/6])
    approx = centered_difference_quotient(f, pts)
    df = lambda x: (np.sin(x)+1)**x*(np.log(np.sin(x)+1) + x*np.cos(x)/(np.sin(x)+1))
    error = calculate_errors(f,df,pts)
    return approx, error

# Problem 4
def Prob4():
    """Use centered difference quotients to calculate the speed v of the plane at t = 10 s
    Returns:
        speed v of plane (float)
    
    """
    alphas = np.array([54.80, 54.06, 53.34])
    betas = np.array([65.59, 64.59, 63.62]) 
    
    #convert to radians
    alphas *= (np.pi/180.)
    betas *= (np.pi/180.) 
    
    #define a function that computes secant
    sec = lambda x: 1./np.cos(x)
    
    #compute dB/dt, dA/dt when t = 10 where B is beta and A is alpha 
    #using the centered difference quotient
    dBdt = (betas[2]-betas[0])/2
    dAdt = (alphas[2]-alphas[0])/2
    
    #beta(10) and alpha(10)
    beta = betas[1]
    alpha = alphas[1]
    
    #compute dx/dt and dy/dt when t = 10s
    dxdt = (-np.tan(alpha)*(sec(alpha)**2)*dBdt+np.tan(beta)*(sec(alpha)**2)*dAdt)/(np.tan(beta)-np.tan(alpha))**2
    dxdt *= 500
    dydt = ((sec(alpha)**2)*(np.tan(beta)**2)*dAdt-(sec(beta)**2)*(np.tan(alpha)**2)*dBdt)/(np.tan(beta)-np.tan(alpha))**2
    dydt *= 500
    
    dydx = np.abs(dydt/dxdt)
    return dydx


# Problem 5
def jacobian(f, n, m, pt, h=1e-5):
    """Compute the approximate Jacobian matrix of f at pt using the centered
    difference quotient.

    Inputs:
        f (function): the multidimensional function for which the derivative
            will be approximated.
        n (int): dimension of the domain of f.
        m (int): dimension of the range of f.
        pt (array): an n-dimensional array representing a point in R^n.
        h (float): a float to use in the centered difference approximation.

    Returns:
        Jacobian matrix of f at pt using the centered difference quotient.
    """
    J = np.zeros((n,m))
    A = np.eye(m)
    for j in range(m):
        Df_app = lambda x: .5*(f(x+h*A[j,:])-f(x-h*A[j,:]))/h
        J[:,j] = Df_app(pt)
    return J


# Problem 6
def findError():
    """Compute the maximum error of jacobian() for the function
    f(x,y)=[(e^x)sin(y) + y^3, 3y - cos(x)] on the square [-1,1]x[-1,1].

    Returns:
        Maximum error of your jacobian function.
    """
    f = lambda x: np.array([(np.e**x[0])*np.sin(x[1])+x[1]**3, 3.*x[1]-np.cos(x[0])])
    df = lambda x: np.array([[np.e**x[0]*np.sin(x[1]),np.e**x[0]*np.cos(x[1])+3*x[1]**2],[np.sin(x[0]),3]])
    maxerror = np.zeros((2,2))
    for i in np.linspace(-1,1,num=100):
        for j in np.linspace(-1,1,num=100):
            myerror = (df(np.array([i,j]))-jacobian(f,2,2,np.array([i,j])))
            if la.norm(myerror)>la.norm(maxerror):
                maxerror = myerror
    return la.norm(maxerror)

def test_one():
    print "Testing 1"
    f = lambda x: np.exp(x)
    print centered_difference_quotient(f,np.array([1,2,3,4]))

def test_two():
    print "Testing 2"
    f = lambda x: np.exp(x)
    df = f
    print calculate_errors(f,df, np.array([1,2,3,4]),h = 1e-5)

def test_three():
    print "Testing 3"
    print Prob3()

def test_four():
    print "Testing 4"
    print Prob4()

def test_five():
    print "Testing 5"
    f = lambda x: np.array([(np.e**x[0])*np.sin(x[1])+x[1]**3, 3.*x[1]-np.cos(x[0])])
    print jacobian(f, 2, 2, np.array([1.,1.]))

def test_six():
    print "Testing 6"
    print findError()


if __name__ == "__main__":
    test_one()
    test_two()
    test_three()
    test_four()
    test_five()
    test_six()

