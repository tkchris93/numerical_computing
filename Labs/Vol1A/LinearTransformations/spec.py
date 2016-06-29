# name this file 'solutions.py'.
"""Volume I: Linear Transformations.
<Name>
<Class>
<Date>
"""

from random import random

def random_vector(n):
    """Generate a random vector of length n as a list."""
    return [random() for i in xrange(n)]

def random_matrix(n):
    """Generate a random nxn matrix as a list of lists."""
    return [[random() for j in xrange(n)] for i in xrange(n)]

def matrix_vector_product(A, x):
    """Compute the matrix-vector product Ax as a list."""
    m, n = len(A), len(x)
    return [sum([A[i][k] * x[k] for k in range(n)]) for i in range(m)]

def matrix_matrix_product(A, B):
    """Compute the matrix-matrix product AB as a list of lists."""
    m, n, p = len(A), len(B), len(B[0])
    return [[sum([A[i][k] * B[k][j] for k in range(n)])
                                    for j in range(p) ]
                                    for i in range(m) ]

# Problem 1
def prob1(N=8):
    """Use time.time(), timeit.timeit(), or %timeit to time
    matrix_vector_product() and matrix-matrix-mult() with increasingly large
    inputs. Generate the inputs A, x, and B with random_matrix() and
    random_vector() (so each input will be nxn or nx1).
    Only time the multiplication functions, not the generating functions.

    Report your findings in a single figure with two subplots: one with matrix-
    vector times, and one with matrix-matrix times. Choose a domain for n so
    that your figure accurately describes the growth, but avoid values of n
    that lead to execution times of more than 1 minute.
    """
    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def prob2(N=8):
    """Time matrix_vector_product(), matrix_matrix_product(), and np.dot().

    Report your findings in a single figure with two subplots: one with all
    four sets of execution times on a regular linear scale, and one with all
    four sets of exections times on a log-log scale.
    """
    raise NotImplementedError("Problem 2 Incomplete")


# Problem 3
def stretch(A, a, b):
    """Scale the points in 'A' by 'a' in the x direction and 'b' in the
    y direction.

    Inputs:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        a (float): scaling factor in the x direction.
        b (float): scaling factor in the y direction.
    """
    raise NotImplementedError("Problem 3 Incomplete")

def shear(A, a, b):
    """Slant the points in 'A' by 'a' in the x direction and 'b' in the
    y direction.

    Inputs:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        a (float): scaling factor in the x direction.
        b (float): scaling factor in the y direction.
    """
    raise NotImplementedError("Problem 3 Incomplete")

def reflect(A, a, b):
    """Reflect the points in 'A' about the origin by 'theta' radians.

    Inputs:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        theta (float): The rotation angle in radians.
    """
    raise NotImplementedError("Problem 3 Incomplete")

def rotate(A, theta):
    """Rotate the points in 'A' about the origin by 'theta' radians.

    Inputs:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        theta (float): The rotation angle in radians.
    """
    raise NotImplementedError("Problem 3 Incomplete")


# Problem 4
def solar_system(T, omega_e, omega_m):
    """Plot the trajectories of the earth and moon over the time interval [0,T]
    assuming the initial position of the earth is (10,0) and the initial
    position of the moon is (11,0).

    Parameters:
        T (int): The final time.
        omega_e (float): The earth's angular velocity.
        omega_m (float): The moon's angular velocity.
    """
    raise NotImplementedError("Problem 4 Incomplete")


def solar_system_animation(earth, moon):
    """Animate the earth orbiting the sun and the moon orbiting the earth.

    Inputs:
        earth ((2,N) ndarray): The earth's postion with x-coordinates on the
            first row and y coordinates on the second row.
        moon ((2,N) ndarray): The moon's postion with x-coordinates on the
            first row and y coordinates on the second row.
    """

    animation_fig = plt.figure()                    # Make a new figure.
    plt.axis([-15,15,-15,15])                       # Set the window limits.
    plt.gca().set_aspect("equal")                   # Make the window square.

    earth_dot,  = plt.plot([],[], 'bo', ms=10)      # Blue dot for the earth.
    earth_path, = plt.plot([],[], 'b-')             # Blue line for the earth.
    moon_dot,   = plt.plot([],[], 'go', ms=5)       # Green dot for the moon.
    moon_path,  = plt.plot([],[], 'g-')             # Green line for the moon.
    plt.plot([0],[0],'y*',ms=30)                    # Yellow star for the sun.

    def animate(index):
        """Update the four earth and moon plots."""
        earth_dot.set_data(earth[0,index], earth[1,index])
        earth_path.set_data(earth[0,:index], earth[1,:index])
        moon_dot.set_data(moon[0,index], moon[1,index])
        moon_path.set_data(moon[0,:index], moon[1,:index])
        return earth_dot, earth_path, moon_dot, moon_path

    a = animation.FuncAnimation(animation_fig, animate,
                                frames=earth.shape[1], interval=25)
    plt.show()

