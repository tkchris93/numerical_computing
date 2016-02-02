# solutions.py
"""Volume II: Compressed Sensing. Solutions file."""

import numpy as np
from cvxopt import matrix, solvers
from matplotlib import pyplot as plt
from visualize2 import visualizeEarth
from camera import Camera

def l1min(A, b):
    """Calculate the solution to the optimization problem

        minimize    ||x||_1
        subject to  Ax = b

    Return only the solution x (not any slack variable), as a flat NumPy array.

    Parameters:
        A ((m,n) ndarray)
        b ((m, ) ndarray)

    Returns:
        x ((n, ) ndarray): The solution to the minimization problem.
    """

    assert A.shape[0] == b.shape[0], "mismatched dimensions"

    n = A.shape[1]
    I = np.eye(n, dtype=np.float)

    '''The optimization problem to solve (via cvxopt) is:

    minimize                [u]
                      [1 0] [x]

    subject to      [-I  I] [u]     [0]
                    [-I -I] [x]  <= [0]

                            [u]
                    [0   A] [x]  ==  b
    '''

    # Build the matrices for cvxopt (make sure dtype=np.floats)
    c = matrix(np.hstack((np.ones(n), np.zeros(n))).astype(np.float))
    G = matrix(np.vstack((np.hstack((-I, I)),np.hstack((-I, -I)))))
    h = matrix(np.zeros(2*n))
    new_A = matrix(np.hstack((np.zeros_like(A), A)).astype(np.float))
    new_b = matrix(b.astype(np.float))

    # Perform the optimization.
    sol = solvers.lp(c, G, h, new_A, new_b)

    # Flatten out the array and only get the x value.
    return np.array(sol['x']).ravel()[n:]

def prob2(filename='ACME.png'):
    """Reconstruct the image in the indicated file using 100, 200, 250, and 270
    measurements. Seed the pseudorandom number generator before each
    measurement to obtain consistent results.

    Produce a plot with 4 subplots, one for each reconstruction.

    Report the 2-norm distance between each reconstructed image and the
    original image.
    """
    image = 1 - plt.imread(filename)[:,:,0]
    measurements, err2 = [100, 200, 250, 270], []
    
    for m in measurements:
        # Get 'm' random measurements.
        np.random.seed(1337)
        A = np.random.randint(0,2,(m,image.shape[0]*image.shape[1]))
        b = A.dot(image.flatten())

        # Reconstruct the image and calculate the 2-norm error.
        reconstruction = l1min(A,b).reshape(image.shape)
        err.append(np.linalg.norm(image - reconstruction))

        # Plot the image.
        plt.subplot(2,2,measurements.index(m)+1)
        plt.imshow(reconstruction)
        plt.title("{} measurements".format(m))
    
    # Show the subplots and return the error list.
    plt.suptitle("Reconstruction of {}".format(filename))
    plt.show()
    
    return err

from sys import stdout

def prob3():
    """
            UNDER CONSTRUCTION

            Does anyone know where the solutions file is?
    """
    raise NotImplementedError("This function is incomplete")

    data = np.load("StudentEarthData.npz")
    faces, vertices, colors = data['faces'], data['vertices'], data['C']
    V = data['V']
    visualizeEarth(faces, vertices, colors)

    MyCamera = Camera(faces, vertices, colors)
    theta = np.linspace(0, 2*np.pi, 30)
    phi = np.linspace(0, np.pi, 30)
    for t in theta:
        print '\rtheta = {}'.format(t),; stdout.flush()
        for p in phi:
            MyCamera.add_pic(t,p,3)
    A,b = MyCamera.returnData()

    return A,b

    reconstruction = l1min(A,b)

    print A, '\n', b

    '''
    measurements = [450, 550, 650]
    for m in measurements:
        np.random.seed(1337)
        # A = np.random.randint(0,2,(m, ))
    '''
