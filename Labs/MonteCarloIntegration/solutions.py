# solutions.py
"""Volume I: Monte Carlo Integration
Solutions file. Written by Tanner Christensen, Jan 2016
"""

import numpy as np

def prob1(numPoints=100000):
    """Return an estimate of the volume of the unit sphere using Monte
    Carlo Integration.
    """
    points = np.random.rand(3, numPoints)
    points = points*2 - 1
    circleMask = [la.norm(points[:,1]) for i in xrange(numPoints)]
    numInCircle = np.sum(circleMask)
    return 8.*numInCircle/numPoints
    
def prob2(numPoints=100000):
    """Return an estimate of the area under the curve,
        f(x) |sin(10x)cos(10x) + sqrt(x)*sin(3x)| 
    from 1 to 5.
    """
    f = lambda x : np.abs(np.sin(10*x)*np.cos(10*x) + np.sqrt(x) * np.sin(3*x))
    points = np.random.rand(numPoints)
    points = points * 4 + 1
    return 4*np.sum(f(points))/numPoints

def mc_int(f, mins, maxs, numPoints=500, numIters=100):
    """Use Monte-Carlo integration to approximate the integral of f
    on the box defined by mins and maxs.
    
    Inputs:
        f (function) - The function to integrate. This function should 
            accept a 1-D NumPy array as input.
        mins (1-D np.ndarray) - Minimum bounds on integration.
        maxs (1-D np.ndarray) - Maximum bounds on integration.
        numPoints (int, optional) - The number of points to sample in 
            the Monte-Carlo method. Defaults to 500.
        numIters (int, optional) - An integer specifying the number of 
            times to run the Monte Carlo algorithm. Defaults to 100.
        
    Returns:
        estimate (int) - The average of 'numIters' runs of the 
            Monte-Carlo algorithm.
                
    Example:
        >>> f = lambda x: np.hypot(x[0], x[1]) <= 1
        >>> # Integral over the square [-1,1] x [-1,1]. Should be pi.
        >>> mc_int(f, np.array([-1,-1]), np.array([1,1]))
        3.1290400000000007
    """
    if len(mins) != len(maxs):
        raise ValueError("Dimension of mins and maxs must be the same")
    
    results = []
    for i in xrange(numIters):
        # create points
        dim = len(mins)
        side_lengths = maxs-mins
        points = np.random.rand(numPoints,dim)
        points = side_lengths*points + mins

        # calculate Volume
        V = 1
        for i in xrange(dim):
            V *= maxs[i] - mins[i]

        # apply the function f along axis=1 and sum all the results
        total = np.sum(np.apply_along_axis(f,1,points))
        results.append((V/float(numPoints))*total)
    estimate = np.average(results)
    return estimate

def prob4(numPoints=[500]):
    mins = -1*np.ones(4)
    maxs = np.ones(4)
    f = lambda x : np.sin(x[0])*x[1]**5 - x[1]**3 + x[2]*x[3] + x[1]*x[2]**2
    errors = []
    for n in numPoints:
        errors.append(mc_int(f, mins, maxs, n))
    return errors
    
if __name__ == "__main__":
    print prob4([100,200,300])
