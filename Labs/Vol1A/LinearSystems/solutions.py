# solutions.py
"""Volume I: Linear Systems. Solutions file."""

import numpy as np
from time import time
from scipy import linalg as la
from matplotlib import pyplot as plt


# Problem 1
def ref(A):
    """Reduce a square matrix A to REF. During a row operation, do not
    modify any entries that you know will be zero before and after the
    operation."""
    A = np.array(A, dtype=np.float, copy=True)
    m,n = A.shape
    for j in xrange(min(m,n) - 1):
        for i in xrange(j+1, m):
            A[i,j:] -= A[j,j:] * A[i,j] / A[j,j]
    return A


# Problem 2
def lu_factor(A):
    """Compute the LU decomposition of A."""
    m, n = A.shape
    U = np.array(A, dtype=np.float, copy=True)
    L = np.eye(n)
    for j in xrange(n):
        for i in xrange(j+1, m):
            L[i,j] = U[i,j]/U[j,j]
            U[i,j:] -= L[i,j]*U[j,j:]
    return L,U


# Problem 3
def solve(A, b):
    """Use the LU decomposition and back substitution to solve the linear
    system Ax = b. You may assume that A is invertible (hence square).
    """
    A, b = np.array(A), np.ravel(b)
    m, n = A.shape
    assert m == n, "Matrix must be square."
    assert b.size == m, "Bad shape!"

    L, U = lu_factor(A)

    # First solve Ly = Pb (assume P = I).
    y = np.zeros(n)
    for k in xrange(n):
        y[k] = b[k] - np.dot(L[k,:k], y[:k])

    # Now solve Ux = y.
    x = np.zeros(n)
    for k in reversed(xrange(n)):
        x[k] = (y[k] - np.dot(U[k,k:], x[k:])) / U[k,k]

    return x


# Problem 4
def prob4(N=12):
    """Time different scipy.linalg functions for solving square linear systems.
    """
    domain = 2**np.arange(1,N+1)
    inv, solve, lu_factor, lu_solve = [], [], [], []
    for n in domain:
        A = np.random.random((n,n))
        b = np.random.random(n)

        start = time()
        la.inv(A).dot(b)
        inv.append(time()-start)

        start = time()
        la.solve(A, b)
        solve.append(time()-start)

        start = time()
        x = la.lu_factor(A)
        la.lu_solve(x, b)
        lu_factor.append(time()-start)

        start = time()
        la.lu_solve(x, b)
        lu_solve.append(time()-start)

    plt.subplot(121)
    plt.plot(domain, inv, '.-', lw=2, label="la.inv()")
    plt.plot(domain, solve, '.-', lw=2, label="la.solve()")
    plt.plot(domain, lu_factor, '.-', lw=2,
                                        label="la.lu_factor() + la.lu_solve()")
    plt.plot(domain, lu_solve, '.-', lw=2, label="la.lu_solve() alone")
    plt.legend(loc="upper left")

    plt.subplot(122)
    plt.loglog(domain, inv, '.-', basex=2, basey=2, lw=2)
    plt.loglog(domain, solve, '.-', basex=2, basey=2, lw=2)
    plt.loglog(domain, lu_factor, '.-', basex=2, basey=2, lw=2)
    plt.loglog(domain, lu_solve, '.-', basex=2, basey=2, lw=2)
    plt.suptitle("Problem 4 Solution")

    plt.show()


# Additional Material =========================================================

def ref_with_swaps(A):
    """Reduce an mxn matrix to REF."""
    A = np.array(A, dtype=float, copy=True)
    m,n = A.shape
    for j in xrange(min(m, n) - 1):
        # Deal with 0's on the diagonal.
        if np.allclose(A[j:,j], np.zeros(m-i)):
            continue
        while np.isclose(A[j,j], 0):
            A[j:] = np.roll(A[j:], -1, axis=0)
        # Zero out the rows below the current entry.
        for i in xrange(j+1, m):
            A[i,j:] -= A[j,j:] * A[i,j] / A[j,j]
    # Set extra rows to zero.
    if m > n:
        A[n:] = 0
    return A
