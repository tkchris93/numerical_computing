# solutions.py
"""Volume 1A: Iterative Solvers. Solutions File."""

import time
import numpy as np
from scipy import sparse
from scipy import linalg as la
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Helper functions
def diag_dom(n, num_entries=None):
    """Generate a strictly diagonally dominant nxn matrix.

    Inputs:
        n (int): the dimension of the system.
        num_entries (int): the number of nonzero values. Defaults to n^(3/2)-n.

    Returns:
        A ((n,n) ndarray): An nxn strictly diagonally dominant matrix.
    """
    if num_entries is None:
        num_entries = int(n**1.5) - n
    A = np.zeros((n,n))
    rows = np.random.choice(np.arange(0,n), size=num_entries)
    cols = np.random.choice(np.arange(0,n), size=num_entries)
    data = np.random.randint(-4, 4, size=num_entries)
    for i in xrange(num_entries):
        A[rows[i], cols[i]] = data[i]
    for i in xrange(n):
        A[i,i] = np.sum(np.abs(A[i])) + 1
    return A

def spar_diag_dom(n, num_entries=None):
    """Generate a sparse strictly diagonally dominant nxn matrix.

    Inputs:
        n (int): the dimension of the system.
        num_entries (int): the number of nonzero values. Defaults to n^(3/2)-n.

    Returns:
        A ((n,n) csr_matrix): A sparse nxn strictly diagonally dominant matrix.
    """
    return sparse.csr_matrix(diag_dom(n, num_entries))


# Problems 1 and 2
def jacobi_method(A, b, tol=1e-8, maxiters=100, plot=False):
    """Calculate the solution to the system Ax = b voa the Jacobi Method.

    Inputs:
        A ((n,n) ndarray): A square matrix.
        b ((n,) ndarray): A vector of length n.
        maxiters (int, optional): the maximum number of iterations to perform.
        tol (float): the convergence tolerance.
        plot (bool): if True, plot the convergence rate of the algorithm.
            (this is for Problem 2).

    Returns:
        x ((n,) ndarray): the solution to system Ax = b.
    """
    m,n = A.shape
    d = np.diag(A)
    x0 = np.zeros(n)
    error = []

    for k in xrange(maxiters):
        x1 = x0 + (b - A.dot(x0))/d
        error.append(la.norm(A.dot(x1) - b, ord=np.inf))
        if la.norm(x0 - x1, ord=np.inf) < tol:
            break
        x0 = x1

    if plot:
        plt.semilogy(error, lw=2)
        plt.ylabel("Absolute Error of Approximation")
        plt.xlabel("Iteration #")
        plt.title("Convergence of Jacobi Method")
        plt.show()

    return x1


# Old Problem 2
def plot_convergence(A, b, tol=1e-8, maxiters=100):
    """Plot the rate of convergence of the Jacobi Method.

    Inputs:
        A ((n,n) ndarray): A square matrix.
        b ((n,) ndarray): A vector of length n.
        maxiters (int, optional): the maximum number of iterations to perform.
        tol (float): the convergence tolerance.
    """
    x, x_approx = jacobi_method(A,b,tol,maxiters)

    x_approx = np.array(x_approx)
    norms = [la.norm(A.dot(xk) - b, ord=np.inf) for xk in x_approx]

    plt.semilogy(norms, lw=2)
    plt.ylabel("Absolute Error of Approximation")
    plt.xlabel("Iteration")
    plt.title("Convergence of Jacobi Method")
    plt.show()


# Problem 3
def gauss_seidel(A, b, tol=1e-8, maxiters=100, plot=False):
    """Calculate the solution to the system Ax = b via the Gauss-Seidel Method.

    Inputs:
        A ((n,n) ndarray): A square matrix.
        b ((n,) ndarray): A vector of length n.
        maxiters (int, optional): the maximum number of iterations to perform.
        tol (float): the convergence tolerance.
        plot (bool): if True, plot the convergence rate of the algorithm.

    Returns:
        x ((n,) ndarray): the solution to system Ax = b.
    """
    m,n = A.shape
    x0 = np.zeros(n)
    error = []

    for k in xrange(maxiters):
        x = x0.copy()
        for i in xrange(n):
            a_ii = A[i,i]
            x[i] = b[i]/a_ii + x[i] - np.dot(A[i],x)/a_ii
        diff = la.norm(x0-x, ord=np.inf)
        # error.append(la.norm(A.dot(x) - b, ord=np.inf))
        error.append(diff)
        x0 = x
        if diff < tol:
            break

    if plot:
        plt.semilogy(error, lw=2)
        plt.ylabel("Absolute Error of Approximation")
        plt.xlabel("Iteration")
        plt.title("Convergence of Gauss-Seidel Method")
        plt.show()

    return x


# Problem 4
def compare_times():
    """For a 5000 parameter system, compare the runtimes of the Gauss-Seidel
    method and la.solve(). Print an explanation of why Gauss-Seidel is so much
    faster.
    """
    A = diag_dom(5000)
    b = np.random.rand(5000)

    start = time.time()
    gauss_seidel(A,b)
    gauss_seidel_time = time.time() - start

    start = time.time()
    la.solve(A,b)
    la_solve_time = time.time() - start

    print "Gauss-Seidel: " + str(gauss_seidel_time)
    print "la.solve(): " + str(la_solve_time)


# Problem 5
def sparse_gauss_seidel(A, b, tol=1e-8, maxiters=100):
    """Calculate the solution to the sparse system Ax = b via the Gauss-Seidel
    Method.

    Inputs:
        A ((n,n) csr_matrix): An nxn sparse matrix.
        b ((n,) ndarray): A vector of length n.
        maxiters (int, optional): the maximum number of iterations to perform.
        tol (float): the convergence tolerance.

    Returns:
        x ((n,) ndarray): the solution to system Ax = b.
        x_approx (list): list of approximations at each iteration.
    """

    if type(A) != sparse.csr_matrix:
        A = sparse.csr_matrix(A)
    n = A.shape[0]
    x0 = np.zeros(n)
    x = np.ones(n)
    x_approx = []
    for k in xrange(maxiters):
        x = x0.copy()
        diag = A.diagonal()
        for i in xrange(n):
            rowstart = A.indptr[i]
            rowend = A.indptr[i+1]
            Aix = np.dot(A.data[rowstart:rowend],
                        x[A.indices[rowstart:rowend]])
            x[i] += (b[i] - Aix)/diag[i]
        if np.max(np.abs(x0-x)) < tol:
            return x, x_approx
        x0 = x
        x_approx.append(x)
    return x, x_approx


# Problem 6
def sparse_sor(A, b, omega, tol=1e-8, maxiters=100):
    """Calculate the solution to the system Ax = b via Successive Over-
    Relaxation.

    Inputs:
        A ((n,n) csr_matrix): An nxn sparse matrix.
        b ((n,) ndarray): A vector of length n.
        maxiters (int, optional): the maximum number of iterations to perform.
        tol (float): the convergence tolerance.

    Returns:
        x ((n,) ndarray): the solution to system Ax = b.
        x_approx (list): list of approximations at each iteration.
    """
    if type(A) != sparse.csr_matrix:
        A = sparse.csr_matrix(A)
    n = A.shape[0]
    x0 = np.zeros(n)
    x = np.ones(n)
    x_approx = []
    for k in xrange(maxiters):
        x = x0.copy()
        diag = A.diagonal()
        for i in xrange(n):
            rowstart = A.indptr[i]
            rowend = A.indptr[i+1]
            Aix = np.dot(A.data[rowstart:rowend],
                        x[A.indices[rowstart:rowend]])
            x[i] += omega*(b[i] - Aix)/diag[i]
        if np.max(np.abs(x0-x)) < tol:
            return x, x_approx
        x0 = x
        x_approx.append(x)
    return x, x_approx


# Problem 6
def finite_difference(n):
    data = [[-4]*n, [1]*n, [1]*n]
    diags = [0,1,-1]
    subA = sparse.spdiags(data, diags, n, n)
    A = sparse.block_diag((subA,)*n)
    A.setdiag(1, n)
    A.setdiag(1,-n)

    # the vector b is still royally screwed up
    b = np.zeros(n**2)
    left_bound = np.arange(0,n**2, n)
    right_bound = np.arange(n-1, n**2, n)

    b[left_bound] = -100
    b[right_bound] = -100

    return A, b

def compare_omega():
    # Find an approximation for the optimal omega
    n = 20
    A,b = finite_difference(n)
    timings = []
    for o in np.arange(1,2,.05):
        before = time.time()
        x = sparse_sor(A,b,o,maxiters=10000,tol=10**-2)[0]
        after = time.time()
        timings.append(after - before)
    plt.plot(np.arange(1,2,.05), timings)
    plt.show()


# Testing solutions file.
def test_jacobi():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        jacobi_sol = jacobi_method(A,b)
        sol = la.solve(A,b)
        results.append(np.allclose(jacobi_sol, sol))
    return np.alltrue(results)

def test_plot_convergence():
    A = np.array([[2,0,-1],[-1,3,2],[0,1,3]])
    b = np.array([3,3,-1])
    jacobi_method(A,b,plot=True)
    gauss_seidel(A,b,plot=True)
    plt.show()
    return True

def test_gauss_seidel():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        gs_sol = gauss_seidel(A,b)
        sol = la.solve(A,b)
        results.append(np.allclose(gs_sol, sol))
    return np.alltrue(results)

def test_compare_times():
    compare_times()
    return True

def test_sparse_gauss_seidel():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        sgs_sol, sgs_approx = sparse_gauss_seidel(A,b)
        sol = la.solve(A,b)
        results.append(np.allclose(sgs_sol, sol))
    return np.alltrue(results)

def test_sparse_sor():
    results = []
    for n in [5, 10, 50, 100]:
        A = diag_dom(n)
        b = np.random.rand(n)
        sor_sol, sor_approx = sparse_sor(A,b,0.8,maxiters=300)
        sol = la.solve(A,b)
        results.append(np.allclose(sor_sol, sol))
    return np.alltrue(results)

def test_all():
    if not test_jacobi():
        print "Failed Jacobi"
        return False
    test_plot_convergence()
    if not test_gauss_seidel():
        print "Failed Gauss-Seidel"
        return False

    test_compare_times()
    if not test_sparse_gauss_seidel():
        print "Failed Sparse Gauss-Seidel"
        return False

    if not test_sparse_sor():
        print "Failed SOR"
        return False

    print "Passed All Tests!"
    return True

if __name__ == "__main__":
    test_all()
