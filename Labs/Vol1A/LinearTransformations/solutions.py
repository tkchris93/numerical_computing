# solutions.py
"""Volume I: Linear Transformations. Solutions file."""

import time
import timeit
import numpy as np
from random import random
from matplotlib import pyplot as plt

def random_vector(n):
    """Generate a random vector of length n as a list."""
    return [random() for i in xrange(n)]

def random_matrix(n):
    """Generate a random nxn matrix as a list of lists."""
    return [[random() for j in xrange(n)] for i in xrange(n)]

def matrix_vector_product(A, x):
    """Compute the matrix-vector product Ax (as a list)."""
    m, n = len(A), len(x)
    return [sum([A[i][k] * x[k] for k in range(n)]) for i in range(m)]

def matrix_matrix_product(A, B):
    """Compute the matrix-matrix product AB (as a list of lists)."""
    m, n, p = len(A), len(B), len(B[0])
    return [[sum([A[i][k] * B[k][j] for k in range(n)])
                                    for j in range(p) ]
                                    for i in range(m) ]

# Solutions ===================================================================

def prob1(N=8):
    """Use time.time(), timeit.timeit(), or %timeit to time
    matrix_vector_product(n) and matrix-matrix-mult(n) with
    increasingly large inputs. Generate the inputs A, x, and B with
    random_matrix() and random_vector()} (so each input will be nxn or nx1).
    Only time the multiplication functions, not the generating functions.

    Report your findings in a single figure with two subplots: one with matrix-
    vector times, and one with matrix-matrix times. Choose a domain for n so
    that your figure accurately describes the growth, but avoid values of n
    that lead to execution times of more than 1 minute.
    """
    domain = 2**np.arange(1,N+1)
    vector_times, matrix_times = [], []

    for n in domain:
        A = random_matrix(n)
        x = random_vector(n)
        B = random_matrix(n)

        start = time()
        matrix_vector_product(A, x)
        vector_times.append(time() - start)

        start = time()
        matrix_matrix_product(A, B)
        matrix_times.append(time() - start)

    plt.subplot(121)
    plt.plot(domain, vector_times, 'b.-', lw=2, ms=15)
    plt.xlabel("n", fontsize=14); plt.ylabel("Seconds", fontsize=14)
    plt.title("Matrix-Vector Multiplication")

    plt.subplot(122)
    plt.plot(domain, matrix_times, 'g.-', lw=2, ms=15)
    plt.xlabel("n", fontsize=14)
    plt.title("Matrix-Matrix Multiplication")

    plt.show()


def prob2(N=8):

    domain = 2**np.arange(1,N+1)
    vector_times, matrix_times = [], []

    for n in domain:
        A = random_matrix(n)
        x = random_vector(n)
        B = random_matrix(n)

        start = time()
        matrix_vector_product(A, x)
        vec.append(time() - start)

        start = time()
        matrix_matrix_product(A, B)
        mat.append(time() - start)

    # First Figure: Matrix-Vector and Matrix-Matrix by themselves in subplots.
    plt.subplot(121)
    plt.plot(domain, vector_times, 'b.-', lw=2, ms=15)
    plt.xlabel("n"); plt.ylabel("Seconds")
    plt.title("Matrix-Vector Multiplication")

    plt.subplot(122)
    plt.plot(domain, matrix_times, 'g.-', lw=2, ms=15)
    plt.xlabel("n")
    plt.title("Matrix-Matrix Multiplication")

    plt.show()

    # Time NumPy operations.
    A, B, x = np.array(A), np.array(B), np.array(x)
    start = time.time()
    A.dot(x)
    npvec.append(time.time() - start)

    start = time.time()
    A.dot(B)
    npmat.append(time.time() - start)

    plt.subplot(121)
    plt.plot(domain, vector_times, '.-', lw=2, label="Matrix-Vector with Lists")
    plt.plot(domain, matrix_times, '.-', lw=2, label="Matrix-Matrix with Lists")
    plt.plot(domain, npvector_times, '.-', lw=2, label="Matrix-Vector with NumPy")
    plt.plot(domain, npmatrix_times, '.-', lw=2, label="Matrix-Matrix with NumPy")
    plt.xlabel("n"); plt.ylabel("Seconds")
    plt.legend(loc="upper left")

    plt.subplot(122)
    plt.loglog(domain, vector_times, '.-', lw=2, basex=2, basey=2,
                                            label="Matrix-Vector with Lists")
    plt.loglog(domain, matrix_times, '.-', lw=2, basex=2, basey=2,
                                            label="Matrix-Matrix with Lists")
    plt.loglog(domain, npvector_times, '.-', lw=2, basex=2, basey=2,
                                            label="Matrix-Vector with NumPy")
    plt.loglog(domain, npmatrix_times, '.-', lw=2, basex=2, basey=2,
                                            label="Matrix-Matrix with NumPy")
    plt.xlabel("n")
    plt.legend(loc="upper left")
    plt.show()


# Horsefeathers ===============================================================

def plotOldNew(old, new):
    """Display a plot of points before and after a transform.

    Inputs:
        original (array) - Array of size (2,n) containing points in R2 as columns.
        new (array) - Array of size (2,n) containing points in R2 as columns.
    """
    window = [-5,5,-5,5]

    plt.subplot(121)
    plt.title('Before')
    plt.plot(old[0], old[1], ',k')
    plt.axis(window)
    plt.gca().set_aspect("equal")

    plt.subplot(221)
    plt.title('After')
    plt.plot(new[0], new[1], ',k')
    plt.axis(window)
    plt.gca().set_aspect("equal")
    plt.show()


def dilate(A, x_factor, y_factor):
    """Scale the points in A by x_factor in the x direction and y_factor in
    the y direction.

    Inputs:
        A (array) - Array of size (2,n) containing points in R2 stored as columns.
        x_factor (float) - scaling factor in the x direction.
        y_factor (float) - scaling factor in the y direction.
    """
    T = np.array([[x_factor,0],[0,y_factor]])
    return T.dot(A)

def translate(A, b):
    """Translate the points in A by the vector b.

    Inputs:
        A (array) - Array of size (2,n) containing points in R2 stored as columns.
        b (2-tuple (b1,b2)) - Translate points by b1 in the x direction and by b2
            in the y direction.
    """
    return A + np.vstack(b)

# Problem 2
def rotate(A, theta):
    """Rotate the points in A about the origin by theta radians.

    Inputs:
        A (array) - Array of size (2,n) containing points in R2 stored as columns.
        theta (float) - number of radians to rotate points in A.
    """
    T = np.array([[np.cos(theta),-np.sin(theta)],
                  [np.sin(theta),np.cos(theta)]])
    return T.dot(A)

def shear(A, a, b):
    return np.array([[1, a],[b, 1]]).dot(A)

def reflect(A, L):
    l1, l2 = L
    T = np.array([[l1**2 - l2**2, 2*l1*l2],
                  [2*l1*l2, l2**2 - l1**2]])/(l1**2 + l2**2)
    return T.dot(A)

# Problem 4
def rotatingParticle(time, omega, direction, speed):
    """Display a plot of the path of a particle P1 that is rotating
    around another particle P2.

    Inputs:
     - time (2-tuple (a,b)): Time span from a to b seconds.
     - omega (float): Angular velocity of P1 rotating around P2.
     - direction (2-tuple (x,y)): Vector indicating direction.
     - speed (float): Distance per second.
    """
    direction = np.array(direction)
    T = np.linspace(time[0],time[1],100)
    start_P1 = [1,0]
    posP1_x = []
    posP1_y = []

    for t in T:
        posP2 = speed*t*direction/la.norm(direction)
        posP1 = translate2D(rotate2D(start_P1, t*omega), posP2)[0]
        posP1_x.append(posP1[0])
        posP1_y.append(posP1[1])

    plt.plot(posP1_x, posP1_y)
    plt.gca().set_aspect('equal')
    plt.show()

if __name__ == '__main__':
    prob1(10)
    prob2(10)

