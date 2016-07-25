# blackbox_function.py
"""Volume 2: Optimization Packages I (scipy.optimize). Auxiliary File."""

import numpy as np
from scipy import linalg as la

def blackbox(y_free):
    """
    Finds the combined length of a curve approximated piece-wise by a set 
        of points within two different topologies.
    Accepts:
        y_free (1xn ndarray): the non-endpoint y-values of the curve.

    Returns:
        total_length (float): the length of the approximated curve.
    """

    def length(y_free, start, end, topology):
        """Find the length of the y_free curve for specified topology,
        with start and end as endpoints. Note that start and end must 
        be 2-tuples of integers.

        Accepts:
            start (2-tuple of ints): initial endpoint
            end (2-tuple of ints): final endpoint
        """
        # Record total number of points
        m = len(y_free) + 2 # Number points: free variables plus endpoints

        # Account for the current topology
        y_free = topology - y_free

        # Generate the evenly-spaced x-values of the curve.
        x = np.linspace(start[0], end[0], m)

        # Pad the free variables with the fixed endpoint values, 0 and b.
        y = np.hstack((start[1], y_free, end[1]))

        # Calculate and return the line integral of the approximated curve.
        partial_norms = []
        for i,item in enumerate(y[:-1]):
            partial_norms.append(la.norm(np.array([x[i+1]-x[i],y[i+1] - item])))
        return np.sum(partial_norms)


    # Initialize coordinates of endpoint conditions.
    start = (0, 0) 
    end = (90, 0)

    # Partition y_free into two equal portions.
    assert len(y_free) == 89*2, "Require y_free to be of length 89*2."
    n = len(y_free)/2
    yfree1 = y_free[:n]
    yfree2 = y_free[n:]

    # Define topologies
    topo1 = [56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0,
             56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0,
             56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0,
             49.5, 49.350000000000001, 49.200000000000003,
             49.075000000000003, 49.0, 49.0, 49.0, 49.0, 49.0, 49.0, 49.0,
             56.0, 52.5, 52.5, 52.5, 52.5, 52.5, 52.5, 56.0, 49.0, 49.0,
             49.0, 49.0, 49.0, 49.0, 49.0, 49.075000000000003,
             49.200000000000003, 49.350000000000001, 49.5, 56.0, 56.0,
             56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0,
             56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0,
             56.0, 56.0, 56.0, 56.0, 56.0, 56.0, 56.0]
    topo2 = [55.600000000000009, 55.200000000000003, 54.800000000000004,
             54.400000000000006, 54.000000000000007, 53.600000000000009,
             53.200000000000003, 52.800000000000004, 52.400000000000006,
             52.000000000000007, 50.400000000000006, 49.120000000000005,
             48.000000000000007, 44.800000000000004, 39.200000000000003,
             39.200000000000003, 39.085714285714289, 38.971428571428575,
             38.857142857142861, 38.742857142857147, 38.628571428571433,
             38.51428571428572, 38.400000000000006, 38.285714285714285,
             38.171428571428578, 38.057142857142857, 37.94285714285715,
             37.828571428571429, 37.714285714285722, 37.600000000000001,
             37.485714285714288, 37.371428571428574, 37.25714285714286,
             37.142857142857146, 37.028571428571432, 36.914285714285718,
             36.457142857142863, 36.0, 35.634285714285717, 35.268571428571434,
             34.948571428571434, 34.628571428571433, 33.714285714285715,
             32.800000000000004, 28.800000000000004, 32.800000000000004,
             33.714285714285715, 34.628571428571433, 34.948571428571434,
             35.268571428571434, 35.634285714285717, 36.0, 36.457142857142863,
             36.914285714285718, 37.028571428571432, 37.142857142857146,
             37.25714285714286, 37.371428571428574, 37.485714285714288,
             37.600000000000001, 37.714285714285722, 37.828571428571429,
             37.94285714285715, 38.057142857142857, 38.171428571428578,
             38.285714285714285, 38.400000000000006, 38.51428571428572,
             38.628571428571433, 38.742857142857147, 38.857142857142861,
             38.971428571428575, 39.085714285714289, 39.200000000000003,
             39.200000000000003, 44.800000000000004, 48.000000000000007,
             49.120000000000005, 50.400000000000006, 52.000000000000007,
             52.400000000000006, 52.800000000000004, 53.200000000000003,
             53.600000000000009, 54.000000000000007, 54.400000000000006,
             54.800000000000004, 55.200000000000003, 55.600000000000009]

    # Return the combined lengths of the two curves
    return length(yfree1, start, end, topo1) + length(yfree2, start, end, topo2)
    
    

