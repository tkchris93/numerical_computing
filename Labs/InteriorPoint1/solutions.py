# solutions.py
"""Volume 2 Lab 19: Interior Point 1 (Linear Programs). Solution file."""
# This is Shane's temporary solutions file.

from __future__ import division
from scipy import linalg as la
import numpy as np

def startingPoint(A, b, c):
    """Calculate an initial guess to the solution of the linear program
    min c^T x, Ax = b, x>=0.
    Reference: Nocedal and Wright, p. 410.
    """
    # Calculate x, lam, mu of minimal norm satisfying both
    # the primal and dual constraints.
    B = la.inv(A.dot(A.T))
    x = A.T.dot(B.dot(b))
    lam = B.dot(A.dot(c))
    mu = c - A.T.dot(lam)

    # Perturb x and s so they are nonnegative.
    dx = max((-3./2)*x.min(), 0)
    dmu = max((-3./2)*mu.min(), 0)
    x += dx*np.ones_like(x)
    mu += dmu*np.ones_like(mu)

    # Perturb x and mu so they are not too small and not too dissimilar.
    dx = .5*(x*mu).sum()/mu.sum()
    dmu = .5*(x*mu).sum()/x.sum()
    x += dx*np.ones_like(x)
    mu += dmu*np.ones_like(mu)

    return x, lam, mu

# Problems 1-5
def interiorPoint(A, b, c, niter=20, tol=1e-16, verbose=False):
    """Interior Point, Baby!
    """

    m,n = A.shape
    def F(x_, l_, m_):
        return np.hstack((np.dot(A.T, l_) + m_ - c, np.dot(A, x_) - b, m_*x_))

    DF = np.zeros((2*n+m, 2*n+m))
    DF[:n,n:-n] = A.T
    DF[:n,-n:] = np.eye(n)
    DF[n:-n,:n] = A

    # Get the initial point and verify the dimensions.
    x, lam, mu = startingPoint(A, b, c)
    assert len(x) == len(mu) == len(c) == n
    assert len(lam) == len(b) == m

    e = np.ones_like(mu)
    sigma = .5

    i = 0
    nu = 1.
    while i < niter:# and nu >= tol:
        i += 1

        # Problem 3: Search Direction
        DF[-n:,:n] = np.diag(mu)
        DF[-n:,-n:] = np.diag(x)

        nu = np.dot(x, mu) / n
        nu_vec = np.hstack((np.zeros(n+m), e*nu*sigma))
        lu_piv = la.lu_factor(DF)
        direct = la.lu_solve(lu_piv, nu_vec - F(x,lam,mu))

        # Problem 4: Step Length
        trix, trilam, trimu = direct[:n], direct[n:-n], direct[-n:]
        mask = trimu < 0
        if np.any(mask):
            alpha = min(1, -(mu/trimu)[mask].min())
        else:
            alpha = 1
        mask = trix < 0
        if np.any(mask):
            delta = min(1, -(x/trix)[mask].min())
        else:
            delta = 1

        # Problem 5: Finish it up.
        x += delta*trix
        lam += alpha*trilam
        mu += alpha*trimu

        if verbose:
            print("Interation {:0>2} nu = {}".format(i+1, nu))
    if i < niter:
        print("Converged in {} iterations".format(i))
    return x, c.dot(x)

def randomLP2(m):
    """Generate a linear program min c^T x s.t. Ax = b, x>=0.
    First generate m feasible constraints, then add slack variables
    to convert it into the above form.
    Inputs:
        m -- positive integer >= n, number of desired constraints.
        n -- dimension of space in which to optimize.
    Outputs:
        A -- array of shape (m,n).
        b -- array of shape (m,).
        c -- array of shape (n,).
        x -- the solution to the LP.
    """
    n = m
    A = np.random.random((m,n))*20 - 10
    A[A[:,-1]<0] *= -1
    x = np.random.random(n)*10
    b = A.dot(x)
    c = A.sum(axis=0)/n
    return A, b, -c, x


def test_interiorPoint(m=7, n=5):
    from IntPointSolutions import randomLP
    A, b, c, v = randomLP(m, n)
    point, value = interiorPoint(A, b, c)
    assert np.allclose(v, point[:5]), "FAILED:\nv: {}\n\npt: {}".format(v, point[:5])

    # Test with CVXOPT
    # from cvxopt import matrix, solvers
    # A, b, c = matrix(A), matrix(b), matrix(c)
    # G = matrix(-np.eye(5))
    # h = matrix(np.zeros(5))
    # sol = solvers.lp(c, G, h, A, b)
    # assert np.allclose(point, np.array(sol["x"]).flatten()), "{}\n\n{}".format(point, sol["x"])
    # assert np.isclose(value, sol["primal objective"]), "{} {}".format(value, sol["primal objective"])

if __name__ == '__main__':
    for i in xrange(1000):
        print '\r{}'.format(i),
        test_interiorPoint()

