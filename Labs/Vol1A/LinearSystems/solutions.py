# solutions.py
"""Volume I: Linear Systems. Solutions file."""

import numpy as np
from scipy import linalg as la

def REF(A, verbose=False):
    """Reduce an mxn matrix to REF."""
    A = np.array(A, dtype=float, copy=True)
    m,n = A.shape
    for i in xrange(min(m, n) - 1):
        if verbose:
            print A; raw_input()
        # Deal with 0's on the diagonal.
        if np.allclose(A[i:,i], np.zeros(m-i)):
            continue
        while np.allclose(A[i,i], 0):
            # A[i:-1], A[-1] = np.copy(A[i+1:]), np.copy(A[i])
            A[i:] = np.roll(A[i:], -1, axis=0)
        # Zero out the rows before the current entry.
        for j in xrange(i+1, m):
            A[j,i:] -= A[i,i:] * A[j,i]/A[i,i]
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
    for k in xrange(min(m,n) - 1):
        for i in xrange(j+1, m):
            A[i,j:] -= A[j,j:] * A[i,j]/A[j,j]
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



