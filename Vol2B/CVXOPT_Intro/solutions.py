# solutions.py
"""Volume 2B: Intro to CVXOPT. Solutions File."""

import numpy as np
from cvxopt import matrix, solvers
from scipy.linalg import block_diag


def prob1():
    """Solve the following convex optimization problem:

    minimize        2x + y + 3z
    subject to      x + 2y          >= 3
                    2x + 10y + 3z   >= 10
                    x               >= 0
                    y               >= 0
                    z               >= 0

    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (sol['primal objective'])
    """

    # Note that 'matrix' initializes by column, not row.
    c = matrix([2., 1., 3.])
    G = matrix(np.array([[-1.,-2.,0.],
                         [-2.,-10.,-3.],
                         [-1.,0.,0.],
                         [0.,-1.,0.],
                         [0.,0.,-1.]]))

    h = matrix([ -3., -10., 0., 0., 0.])
    sol = solvers.lp(c,G,h)
    return np.ravel(sol['x']), sol['primal objective']

    # Answers:
    # np.array([ -1.14760916e-09,   1.50000000e+00,   6.95278285e-11])
    # 1.4999999996249482

# Problem 2
def l1Min(A, b):
    """Calculate the solution to the optimization problem

        minimize    ||x||_1
        subject to  Ax = b

    Parameters:
        A ((m,n) ndarray)
        b ((m, ) ndarray)

    Returns:
        The optimizer x (ndarray), without any slack variables u
        The optimal value (sol['primal objective'])
    """

    assert A.shape[0] == b.shape[0], "mismatched dimensions"

    n = A.shape[1]
    I = np.eye(n, dtype=np.float)

    '''The optimization problem to solve is:

    minimize                [u]
                      [1 0] [x]

    subject to      [-I  I] [u]     [0]
                    [-I -I] [x]  <= [0]

                            [u]
                    [0   A] [x]  ==  b
    '''

    # Build the matrices for cvxopt (make sure dtype=np.floats)
    c = matrix(np.hstack((np.ones(n), np.zeros(n))).astype(np.float))
    G = matrix(np.vstack((np.hstack((-I, I)),np.hstack((-I, -I)))))
    h = matrix(np.zeros(2*n))
    new_A = matrix(np.hstack((np.zeros_like(A), A)).astype(np.float))
    new_b = matrix(b.astype(np.float))

    # Perform the optimization.
    sol = solvers.lp(c, G, h, new_A, new_b)

    # Flatten out the array and remove the u values.
    return np.ravel(sol['x'])[n:], sol['primal objective']


def prob3():
    """Solve the transportation problem by converting the last equality constraint
    into inequality constraints.

    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (sol['primal objective'])
    """
    c = matrix([4., 7., 6., 8., 8., 9.])
    G = matrix(np.array([[-1.,0.,0.,0.,0.,0.],
                         [0.,-1.,0.,0.,0.,0.],
                         [0.,0.,-1.,0.,0.,0.],
                         [0.,0.,0.,-1.,0.,0.],
                         [0.,0.,0.,0.,-1.,0.],
                         [0.,0.,0.,0.,0.,-1.],
                         [0.,1.,0.,1.,0.,1.],
                         [0.,-1.,0.,-1.,0.,-1.]]))
    h = matrix([0.,0.,0.,0.,0.,0., 8., -8.])
    A = matrix(np.array([[1.,1.,0.,0.,0.,0.],
                         [0.,0.,1.,1.,0.,0.],
                         [0.,0.,0.,0.,1.,1.],
                         [1.,0.,1.,0.,1.,0.]]))
    b = matrix([7.,2.,4.,5.])
    sol = solvers.lp(c,G,h,A,b)
    return np.ravel(sol['x']), sol['primal objective']

    # Answers:
    # np.array([[ 5.00e+00],[ 2.00e+00],[ -7.03e-09],
    #           [ 2.00e+00],[ -5.45e-09],[ 4.00e+00]])
    # 86


def prob4():
    """Find the minimizer and minimum of

    g(x,y,z) = (3/2)x^2 + 2xy + xz + 2y^2 + 2yz + (3/2)z^2 + 3x + z

    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (sol['primal objective'])
    """
    P = matrix(np.array([[3.,2.,1.],
                         [2.,4.,2.],
                         [1.,2.,3.]]))

    q = matrix([3., 0., 1.])
    sol = solvers.qp(P, q)
    return np.ravel(sol['x']), sol['primal objective']

    # Answers:
    # np.array([[-1.50],[ 1.00],[-.5]])
    # -2.5


# Problem 5
def l2Min(A, b):
    """Calculate the solution to the optimization problem

        minimize    ||x||_2
        subject to  Ax = b

    Parameters:
        A ((m,n) ndarray)
        b ((m, ) ndarray)

    Returns:
        The optimizer x (ndarray)
        The optimal value (sol['primal objective'])
    """

    assert A.shape[0] == b.shape[0], "mismatched dimensions"

    n = A.shape[1]
    I = np.eye(n, dtype=np.float)

    # Build the matrices for cvxopt (make sure dtype=np.float)
    P = matrix(2*I)
    q = matrix(np.zeros(n))
    new_A = matrix(A.astype(np.float))
    new_b = matrix(b.astype(np.float))

    # Perform the optimization.
    sol = solvers.qp(P, q, A=new_A, b=new_b)

    # Flatten out the array and only get the x value.
    return np.ravel(sol['x']), sol['primal objective']


def prob6():
    """Solve the allocation model problem in 'ForestData.npy'.
    Note that the first three rows of the data correspond to the first
    analysis area, the second group of three rows correspond to the second
    analysis area, and so on.

    Returns (in order):
        The optimizer x (ndarray)
        The optimal value (sol['primal objective']*-1000)
    """
    data = np.load('ForestData.npy')

    c = matrix(data[:,3]*-1)

    A = block_diag(*[[1.,1.,1.] for _ in xrange(7)])
    b = data[::3,1].copy()

    # Flip the inequality signs on the next two
    G = np.vstack((-data[:,4], -data[:,5], -data[:,6], -np.eye(21)))
    h = np.hstack(([-40000., -5., -70.*788.], np.zeros(21)))

    c = matrix(c)
    A = matrix(A)
    b = matrix(b)
    G = matrix(G)
    h = matrix(h)

    sol = solvers.lp(c,G,h,A,b)
    return np.ravel(sol['x']), sol['primal objective']*-1000.

    # Answers:
    # np.array([[ 1.41e-08],[ 6.76e-08],[ 7.50e+01],[ 9.00e+01],[ 1.28e-07],
    #           [ 2.52e-07],[ 1.40e+02],[ 4.18e-07],[ 5.52e-06],[ 1.04e-08],
    #           [ 8.94e-09],[ 6.00e+01],[ 1.23e-07],[ 1.54e+02],[ 5.80e+01],
    #           [ 3.16e-08],[ 3.58e-08],[ 9.80e+01],[ 1.63e-08],[ 9.12e-09],
    #           [ 1.13e+02]])
    # 322514998.983


def _generate_forest_data():
    """Generate the forest data."""
    np.save("ForestData.npy",
            np.array([[1,  75, 1, 503, 310, .01, 40],
                      [0,   0, 2, 140,  50, .04, 80],
                      [0,   0, 3, 203,   0,   0, 95],
                      [2,  90, 1, 675, 198, .03, 55],
                      [0,   0, 2, 100,  46, .06, 60],
                      [0,   0, 3,  45,   0,   0, 65],
                      [3, 140, 1, 630, 210, .04, 45],
                      [0,   0, 2, 105,  57, .07, 55],
                      [0,   0, 3,  40,   0,   0, 60],
                      [4,  60, 1, 330, 112, .01, 30],
                      [0,   0, 2,  40,  30, .02, 35],
                      [0,   0, 3, 295,   0,   0, 90],
                      [5, 212, 1, 105,  40, .05, 60],
                      [0,   0, 2, 460,  32, .08, 60],
                      [0,   0, 3, 120,   0,   0, 70],
                      [6,  98, 1, 490, 105, .02, 35],
                      [0,   0, 2,  55,  25, .03, 50],
                      [0,   0, 3, 180,   0,   0, 75],
                      [7, 113, 1, 705, 213, .02, 40],
                      [0,   0, 2,  60,  40, .04, 45],
                      [0,   0, 3, 400,   0,   0, 95]], dtype=np.float))
