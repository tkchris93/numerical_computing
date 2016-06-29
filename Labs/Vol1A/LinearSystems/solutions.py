# solutions.py
"""Volume I: Linear Systems. Solutions file."""

import numpy as np
from scipy import linalg as la

def REF(A, verbose=False):
    """Reduce an mxn matrix to REF."""
    A = np.array(A, dtype=float, copy=True)
    m,n = A.shape
    for j in xrange(min(m, n) - 1):
        if verbose:
            print A; raw_input()
        # Deal with 0's on the diagonal.
        if np.allclose(A[j:,j], np.zeros(m-i)):
            continue
        while np.allclose(A[j,j], 0):
            A[j:] = np.roll(A[j:], -1, axis=0)
        # Zero out the rows below the current entry.
        for i in xrange(j+1, m):
            A[i,j:] -= A[j,j:] * A[i,j] / A[j,j]
    # Set extra rows to zero.
    if m > n:
        A[n:] = 0
    return A

def REF_Simple(A):
    """Reduce a square matrix A to REF. During a row operation, do not
    modify any entries that you know will be zero before and after the
    operation."""
    A = np.array(A, dtype=np.float, copy=True)
    m,n = A.shape
    for j in xrange(min(m,n) - 1):
        for i in xrange(j+1, m):
            A[i,j:] -= A[j,j:] * A[i,j] / A[j,j]
    return A

def LU(A):
    """Compute the LU decomposition of A."""
    m, n = A.shape
    U = np.array(A, dtype=np.float, copy=True)
    L = np.eye(n)
    for j in xrange(n):
        for i in xrange(j+1, m):
            L[i,j] = U[i,j]/U[j,j]
            U[i,j:] -= L[i,j]*U[j,j:]
    return L,U

def LU_inplace(A):
    """Compute the LU decomposition of A *inplace*. Should be a bonus prob."""
    m, n = A.shape
    A = np.array(A, dtype=np.float, copy=False)
    for j in xrange(n):
        for i in xrange(j+1, m):
            A[i,j] /= A[j,j]
            A[i,j:] -= L[i,j]*U[j,j:]
    return L,U

def solve(A, b):
    """Use the LU decomposition and back substitution to solve the linear
    system Ax = b. You may assume that A is invertible (hence square).
    """
    A, b = np.array(A), np.ravel(b)
    m, n = A.shape
    assert m == n, "Matrix must be square."
    assert b.size == m, "Bad shape!"

    L, U = LU(A)

    # LU = PA --> LUx = PAx --> LUx = Pb.

    # First solve Ly = Pb (assume P = I).
    y = np.zeros(n)
    # y[0] = b[0]
    for k in xrange(n):
        y[k] = b[k] - np.dot(L[k,:k], y[:k])

    # Now solve Ux = y.
    x = np.zeros(n)
    for k in reversed(xrange(n)):
        x[k] = (y[k] - np.dot(U[k,k:], x[k:])) / U[k,k]

    return x


def lu_test(n=10):
    L = np.tril(np.random.random((n,n)), -1)
    np.fill_diagonal(L, 1)
    U = np.triu(np.random.random((n,n)))
    A = np.dot(L,U)
    A = np.random.random((n,n))
    b = np.random.random(n)
    x = solve(A,b)
    return np.allclose(A.dot(x), b)
