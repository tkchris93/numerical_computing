# solutions.py
"""Volume 1B: SymPy and Autograd solutions."""

import sympy as sy
import time
import numpy
from autograd import grad, jacobian
import autograd.numpy as np

# Problem 1
def mye(n):
    """Computes e to the nth digit
    
    Inputs:
        n (integer): nth digit to calculate e
        
    Returns:
        approximation (float): approximation of e
    """
    tot = sy.Rational(0,1)
    term = 1
    bound = sy.Rational(1,10)**(n+1)
    i = 0
    while bound <= term:
        term = sy.Rational(1, sy.factorial(i))
        tot += term
        i += 1
    return sy.Float(tot,n)
    
# Problem 2
def Prob2():
    """Solves y = e^x + x for x
    
    Returns:
        solution (list)
    """
    x,y = sy.symbols('x,y')
    equation = sy.Eq(y, sy.exp(x)+x)
    return sy.solve(equation,x)

# Problem 3
def Prob3():
    """Computes the integral of sin(x^2) from 0 to infinity

    Returns:
        integral (float)
    """
    x = sy.symbols('x')
    return sy.N(sy.integrate(sy.sin(x**2), (x, 0, sy.oo)))
    
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
    
# Problem 4
def Prob4():
    """ Calculates the derivative of e^sin(cos(x)) at x = 1
        Times how long it takes to compute the derivative using SymPy as well as centered difference quotients
        Calculates the error for each approximation
        
    Print the time it takes to compute and the error for both SymPy and centered difference quotients        
    
    Returns:
        SymPy approximation (float)
    """
    
    #Using SymPy
    x = sy.symbols('x')
    f = sy.exp(sy.sin(sy.cos(x)))
    start = time.time()
    grad_f = sy.diff(f)
    derivative = grad_f.subs(x,1.)
    end = time.time()
    print "Time to compute derivative using SymPy:", end-start, '\n'
    df = sy.exp(sy.sin(sy.cos(x)))*sy.cos(sy.cos(x))*(-sy.sin(x))
    print "Error using SymPy:", numpy.abs(df.subs(x,1.)-derivative), '\n'
    
    #Using centered difference quotient
    f = lambda x: numpy.exp(numpy.sin(numpy.cos(x)))
    start = time.time()
    derivative = centered_difference_quotient(f, 1)
    end = time.time()
    print "Time to compute derivative using centered difference quotient:", end-start, '\n'
    df = lambda x: numpy.exp(numpy.sin(numpy.cos(x)))*numpy.cos(numpy.cos(x))*(-numpy.sin(x))
    print "Error using centered difference quotient:", numpy.abs(df(1)-derivative), '\n'
    
    return derivative
    
    
# Problem 5
def Prob5():
    """Solves the differential equation when x = 1
    
    Returns:
        Solution when x = 1
    """
    x = sy.symbols('x')
    f = sy.Function('f')
    expr = f(x).diff(x, 6) +3*f(x).diff(x,4) + 3*f(x).diff(x, 2) + f(x) - x**10*sy.exp(x)-x**11*sy.sin(x)-x**12*sy.exp(x)*sy.sin(x)-x**13*sy.cos(2*x) - x**14*sy.exp(x)*sy.cos(3*x)
    sol = sy.dsolve(expr)
    return sol.subs(x, 1.)
    
    
# Problem 6
def Prob6():
    """ Computes the derivative of ln(sqrt(sin(sqrt(x)))) at x = pi/4
        Times how long it take to compute using SymPy, autograd, and centered difference quotients
        Computes the error of each approximation
        
    Print the time
    Print the error
    
    Returns:
        derviatie (float): the derivative computed using autograd
    """
    #central difference quotient
    function = lambda x: numpy.log(numpy.sqrt(numpy.sin(numpy.sqrt(x))))
    start = time.time()
    derivative = centered_difference_quotient(function,numpy.pi/4)
    end = time.time()
    print "Time to compute derivative using centered difference quotient:", end-start, '\n'
    df = lambda x: (numpy.cos(numpy.sqrt(x))/numpy.sin(numpy.sqrt(x)))/(4*numpy.sqrt(x))
    print "Error using centered difference quotient:", numpy.abs(df(numpy.pi/4)-derivative), '\n'
        
    #SymPy
    x = sy.symbols('x')
    f = sy.log(sy.sqrt(sy.sin(sy.sqrt(x))))
    start = time.time()
    grad_f = sy.diff(f)
    derivative = grad_f.subs(x,1.)
    end = time.time()
    print "Time to compute derivative using SymPy:", end-start
    df = (sy.cos(sy.sqrt(x))/sy.sin(sy.sqrt(x)))/(4*sy.sqrt(x))
    print "Error using SymPy:", numpy.abs(sy.N(df.subs(x,sy.pi/4.))-derivative), '\n'
    
    #autograd
    g = lambda x: np.log(np.sqrt(np.sin(np.sqrt(x))))
    start = time.time()
    grad_g = grad(g)
    derivative = grad_g(np.pi/4)
    end = time.time()
    print "Time to compute derivative using autorad:", end-start, '\n'
    df = lambda x: (np.cos(np.sqrt(x))/np.sin(np.sqrt(x)))/(4*np.sqrt(x))
    print "Error using autograd:", numpy.abs(df(np.pi/4)-derivative), '\n'
    
    return derivative
    
# Problem 7
def Prob7():
    """ Computes Jacobian for the function f(x,y)=[(e^x)sin(y) + y^3, 3y - cos(x)]
        Times how long it takes to compute the Jacobian using SymPy and autograd  
    
    Print the times
    
    Returns:
        Jacobian (array): jacobian found using autograd at (x,y) = (1,1)
    """
    #Computing Jacobian using autograd
    f = lambda x: np.array([np.exp(x[0])*np.sin(x[1])+x[1]**3,3*x[1]-np.cos(x[0])])
    start = time.time()
    grad_f = jacobian(f)
    grad_f(np.array([1.,1.]))
    end = time.time()
    print "Time to compute derivative using autorad:" , end-start, '\n'
    
    #Computing Jacobian using SymPy
    x,y= sy.symbols('x,y')
    F = sy.Matrix([sy.exp(x)*sy.sin(y)+y**3,3*y-sy.cos(x)])
    start = time.time()
    F.jacobian([x,y]).subs([(x,1.), (y,1.)])
    end = time.time()
    print "Time to compute derivative using SymPy:", end-start
    
    return grad_f(np.array([1.,1.]))

def test_one():
    print "Testing 1"
    print mye(10), '\n'

def test_two():
    print "Testing 2"
    print Prob2(), '\n'

def test_three():
    print "Testing 3"
    print Prob3(), '\n'

def test_four():
    print "Testing 4"
    print Prob4(), '\n'

def test_five():
    print "Testing 5"
    print Prob5(), '\n'

def test_six():
    print "Testing 6"
    print Prob6(), '\n'

def test_seven():
    print "Testing 7"
    print Prob7(), '\n'


if __name__ == "__main__":
    test_one()
    test_two()
    test_three()
    test_four()
    test_five()
    test_six()
    test_seven()
