# qr_decomposition.py
"""Volume I: QR 1 (Decomposition).
<Name>
<Class>
<Date>
"""

import numpy as np
from scipy import linalg as la


# Problem 1
def qr_gram_schmidt(A):
    """Compute the QR decomposition of A via the Modified Gram-Schmidt method.

    Inputs:
        A ((m,n) ndarray): A matrix of rank n.

    Returns:
        Q ((m,n) ndarray): An orthonormal matrix.
        R ((n,n) ndarray): An upper triangular matrix.
    """
    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def abs_det(A):
    """Use the QR decomposition to efficiently compute the absolute value of
    the determinant of A.

    Inputs:
        A ((n,n) ndarray): A square matrix.

    Returns:
        (float) the absolute value of the detetminant of A.
    """
    raise NotImplementedError("Problem 2 Incomplete")


# Problem 3
def solve(A, b):
    """Use the QR decomposition to efficiently solve the system Ax = b.

    Inputs:
        A ((n,n) ndarray): An invertible matrix.
        b ((n, ) ndarray): A vector of length n.

    Returns:
        x ((n, ) ndarray): The solution to the system Ax = b.
    """
    raise NotImplementedError("Problem 3 Incomplete")

# Problem 4
def qr_householder(A):
    """Compute the QR decomposition of A via Householder reflections.

    Inputs:
        A ((m,n) ndarray): A matrix of rank n.

    Returns:
        Q ((m,n) ndarray): An orthonormal matrix.
        R ((n,n) ndarray): An upper triangular matrix.
    """
    raise NotImplementedError("Problem 4 Incomplete")

# Problem 5
def hessenberg(A):
    """Compute the Hessenberg form H of A, along with the orthonormal matrix Q
    such that A = (Q^T)HQ.

    Inputs:
        A ((m,m) ndarray): An invertible matrix.

    Returns:
        Q ((m,m) ndarray): An orthonormal matrix.
        H ((m,m) ndarray): The upper hessenberg form of A.
    """
    raise NotImplementedError("Problem 5 Incomplete")


# Additional Material
def qr_givens(A):
    """Compute the QR decomposition of A via Givens triangularization,
    assuming that at the ijth stage of the algorithm, a_ij will be nonzero.

    Inputs:
        A ((m,n) ndarray): A matrix of rank n.

    Returns:
        Q ((m,n) ndarray): An orthonormal matrix.
        R ((n,n) ndarray): An upper triangular matrix.
    """
    pass


def qr_givens_hessenberg(H):
    """Compute the QR decomposition of the upper Hessenberg matrix H via
    Givens triangularization.

    Inputs:
        H ((m,n) ndarray): A matrix of rank n in upper Hessenberg form.

    Returns:
        Q ((m,n) ndarray): An orthonormal matrix.
        R ((n,n) ndarray): An upper triangular matrix.
    """
    pass
