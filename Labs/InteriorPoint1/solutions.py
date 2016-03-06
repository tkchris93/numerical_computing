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
def interiorPoint(A, b, c, niter=20):
    """Interior Point, Baby!
    """

    m,n = A.shape
    def F(x_, l_, m_):
        return np.hstack((np.dot(A.T, l_) + m_ - c, np.dot(A, x_) - b, m_*x_))

    # def DF(x_, m_):
    #     top = np.hstack((np.zeros((n,n)), A.T, np.eye(n)))
    #     mid = np.hstack((A, np.zeros((m,m)), np.zeros((m,n))))
    #     low = np.hstack((np.diag(m_), np.zeros((n,m)), np.diag(x_)))
    #     return np.row_stack((top, mid, low))

    DF = np.zeros((2*n+m, 2*n+m))
    DF[:n,n:-n] = A.T
    DF[:n,-n:] = np.eye(n)
    DF[n:-n,:n] = A

    # Get the initial point and verify the dimensions.
    x, lam, mu = startingPoint(A, b, c)
    assert len(x) == len(mu) == len(c) == n
    assert len(lam) == len(b) == m

    e = np.ones_like(mu)
    sigma = .1

    for i in xrange(niter):

        DF[-n:,:n] = np.diag(mu)
        DF[-n:,-n:] = np.diag(x)

        # Problem 3: Search Direction
        nu = np.dot(x, mu) / n
        nu_vec = np.hstack((np.zeros(n+m), e*nu*sigma))
        lu_piv = la.lu_factor(DF)
        direct = la.lu_solve(lu_piv, F(x,lam,mu))
        # direct = la.solve(DF(x,mu), nu_vec - F(x,lam,mu))

        # Problem 4: Step Length
        trix, trilam, trimu = direct[:n], direct[n:-n], direct[-n:]
        print trix, trilam, trimu
        print x, lam, mu
        raw_input()
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

        x += delta*trix
        lam += alpha*trilam
        mu += alpha*trimu

        print(nu)

    return x, c.dot(x)



if __name__ == '__main__':
    # A = np.array([[1, -1.1],[3.1,  1],[4.2,  3]], dtype=np.float)
    # b = np.array([2, 5, 7], dtype=np.float)
    # c = np.array([3, 2], dtype=np.float)

    from IntPointSolutions import randomLP
    A, b, c, v = randomLP(3,2)
    A = A[:,:2]
    c = c[:2]
    print A, b, c; raw_input()
    interiorPoint(A, b, c)


