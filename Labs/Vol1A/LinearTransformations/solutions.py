# solutions.py
"""Volume I: Linear Transformations. Solutions file."""

import time
import timeit
import numpy as np
from matplotlib import pyplot as plt

# Helper Functions ============================================================
def matrix_multiplication(A, B):
    """Compute the matrix product AB, where each input is a list of lists."""
    if type(B[0]) is list:          # matrix-matrix multiplication.
        m, n, l = len(A), len(B), len(B[0])
        return [[sum([A[i][k] * B[k][j] for k in range(n)])
                                        for j in range(l) ]
                                        for i in range(m) ]
    else:                           # matrix-vector multiplication.
        m, n = len(A), len(B)
        return [sum([A[i][k] * B[k] for k in range(n)]) for i in range(m)]

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

# Examples ====================================================================



# Solutions ===================================================================

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

