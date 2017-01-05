# numerical_differentiation.py
"""Volume 1B: Numerical Differentiation.
<Name>
<Class>
<Date>
"""


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
    raise NotImplementedError("Problem 1 Incomplete")

# Problem 2
def calculate_errors(f,df,pts,h = 1e-5):
    """Compute the errors using the centered difference quotient approximation.

    Inputs:
        f (function): the function for which the derivative will be
            approximated.
        df (function): the function of the derivative
        pts (array): array of values to calculate the derivative

    Returns:
        an array of the errors for the centered difference quotient
            approximation.
    """
    raise NotImplementedError("Problem 2 Incomplete")

# Problem 3
def prob3():
    """Use the centered difference quotient to approximate the derivative of
    f(x)=(sin(x)+1)^x at x= π/3, π/4, and π/6.
    Then compute the error of each approximation

    Returns:
        an array of the derivative approximations
        an array of the errors of the approximations
    """
    raise NotImplementedError("Problem 3 Incomplete")

# Problem 4
def prob4():
    """Use centered difference quotients to calculate the speed v of the plane
    at t = 10 s

    Returns:
        (float) speed v of plane
    """
    raise NotImplementedError("Problem 4 Incomplete")


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
        (ndarray) Jacobian matrix of f at pt using the centered difference
            quotient.
    """
    raise NotImplementedError("Problem 5 Incomplete")


# Problem 6
def findError():
    """Compute the maximum error of jacobian() for the function
    f(x,y)=[(e^x)sin(y) + y^3, 3y - cos(x)] on the square [-1,1]x[-1,1].

    Returns:
        Maximum error of your jacobian function.
    """
    raise NotImplementedError("Problem 6 Incomplete")


