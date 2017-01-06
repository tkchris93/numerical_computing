# montecarlo_integration.py
"""Volume 1B: Monte Carlo Integration.
<Name>
<Class>
<Date>
"""


# Problem 1
def prob1(N=10000):
    """Return an estimate of the volume of the unit sphere using Monte
    Carlo Integration.

    Input:
        N (int, optional) - The number of points to sample. Defaults
            to 10000.

    """
    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def prob2(f, a, b, N=10000):
    """Use Monte-Carlo integration to approximate the integral of
    1-D function f on the interval [a,b].

    Inputs:
        f (function) - Function to integrate. Should take scalar input.
        a (float) - Left-hand side of interval.
        b (float) - Right-hand side of interval.
        N (int, optional) - The number of points to sample in
            the Monte-Carlo method. Defaults to 10000.

    Returns:
        estimate (float) - The result of the Monte-Carlo algorithm.

    Example:
        >>> f = lambda x: x**2
        >>> # Integral from 0 to 1. True value is 1/3.
        >>> prob2(f, 0, 1)
        0.3333057231764805
    """
    raise NotImplementedError("Problem 2 Incomplete")


# Problem 3
def prob3(f, mins, maxs, N=10000):
    """Use Monte-Carlo integration to approximate the integral of f
    on the box defined by mins and maxs.

    Inputs:
        f (function) - The function to integrate. This function should
            accept a 1-D NumPy array as input.
        mins (1-D np.ndarray) - Minimum bounds on integration.
        maxs (1-D np.ndarray) - Maximum bounds on integration.
        N (int, optional) - The number of points to sample in
            the Monte-Carlo method. Defaults to 10000.

    Returns:
        estimate (float) - The result of the Monte-Carlo algorithm.

    Example:
        >>> f = lambda x: np.hypot(x[0], x[1]) <= 1
        >>> # Integral over the square [-1,1] x [-1,1]. True value is pi.
        >>> mc_int(f, np.array([-1,-1]), np.array([1,1]))
        3.1290400000000007
    """
    NotImplementedError("Problem 3 Incomplete")


# Problem 4
def prob4():
    """Integrate the joint normal distribution.

    Return your Monte Carlo estimate, SciPy’s answer, and (assuming SciPy is
    correct) the relative error of your Monte Carlo estimate.
    """
    NotImplementedError("Problem 4 Incomplete")


# Problem 5
def prob5(numEstimates=50):
    """Plot the error of Monte Carlo Integration."""
    NotImplementedError("Problem 5 Incomplete")
