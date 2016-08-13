# solutions.py
"""Volume I: QR 2 (Applications). Solutions file."""

import numpy as np
from scipy import linalg as la
from numpy.lib import scimath as sm
from matplotlib import pyplot as plt


# Problem 1
def least_squares(A, b):
    """Calculate the least squares solutions to Ax = b using QR decomposition.

    Inputs:
        A ((m,n) ndarray): A matrix of rank n <= m.
        b ((m, ) ndarray): A vector of length m.

    Returns:
        x ((n, ) ndarray): The solution to the normal equation.
    """
    Q,R = la.qr(A, mode="economic")
    return la.solve_triangular(R, np.dot(Q.T, b))

    # Or do back substitution by hand:
    m,n = A.shape
    Q,R = la.qr(A, mode="economic")
    y = np.dot(Q.T, b)
    x = np.zeros(n)

    for k in reversed(range(n)):
        x[k] = (y[k] - np.dot(R[k,k:], x[k:])) / R[k,k]

    return x


# Problem 2 with MLB DATA
def line_fit():
    """Load the data from MLB.npy. Use least squares to calculate the line
    that best relates height to weight.

    Plot the original data points and the least squares line together.
    """
    height, weight, age = np.load("MLB.npy").T
    A = np.column_stack((height, np.ones_like(height)))
    # Or use slicing:
    # A = np.ones((len(height), 2))
    # A[:,0] = height
    slope, intercept = least_squares(A, weight)

    x = np.linspace(height.min()-2, height.max()+2, 20)
    y = x*slope + intercept

    plt.plot(height, weight, '.')
    plt.plot(x, y, 'k-', lw=2)
    plt.show()


def polynomial_fit():
    """Load the data from polynomial.npy. Use least squares to calculate
    the polynomials of degree 3, 5, 7, and 19 that best fit the data.

    Plot the original data points and each least squares polynomial together
    in individual subplots.
    """
    x, y = np.load("polynomial.npy").T
    domain = np.linspace(x.min(), x.max(), 200)

    for i,n in enumerate([3, 5, 7, 19]):
        coeffs = la.lstsq(np.vander(x, n+1), y)[0]
        # coeffs = np.polyfit(x, y, deg=n)

        plt.subplot(2,2,i+1)
        plt.plot(x, y, 'k*')
        plt.plot(domain, np.polyval(coeffs, domain), 'b-', lw=2)
        plt.plot(domain, 2*np.sin(domain), 'k--')
        plt.title(r"$n = {}$".format(n))
        plt.axis([-6,6,-3,3])

    plt.suptitle("Solution to Problem 3")
    plt.show()

def plot_ellipse(a, b, c, d, e):
    """Plot (and show) an ellipse of the form ax^2 + bx + cxy + dy + ey^2 = 1.

    Parameters:
        a, b, c, d, e (floats): Coefficients from the equation of an ellipse
                                of the form ax^2 + bx + cxy + dy + ey^2 = 1.
    """
    theta = np.linspace(0, 2*np.pi, 200)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    A = a*(cos_t**2) + c*cos_t*sin_t + e*(sin_t**2)
    B = b*cos_t + d*sin_t
    r = (-B + np.sqrt(B**2 + 4*A))/(2*A)

    plt.plot(r*cos_t, r*sin_t)
    plt.gca().set_aspect("equal", "datalim")
    plt.show()

# Problem 3
def ellipse_fit():
    """Load the data from ellipse.npy. Use least squares to calculate the
    ellipse that best fits the data.

    Plot the original data points and the least squares ellipse together.
    """
    ellipsepts = np.load("ellipse.npy")#'data.npz')['ellipsepts']
    x_pts = ellipsepts[:,:1]
    y_pts = ellipsepts[:,1:]
    A = np.hstack((x_pts**2, x_pts, x_pts*y_pts, y_pts, y_pts**2))
    b = np.vstack((np.ones(len(ellipsepts))))
    a, b, c, d, e = la.lstsq(A,b)[0]
    plt.plot(x_pts, y_pts, 'k*')
    plot_ellipse(a, b, c, d, e)


# Problem 4
def power_method(A, tol):
    """Compute the dominant eigenvalue of A and its corresponding eigenvector.

    Inputs:
        A ((n,n) ndarray): A square matrix.
        tol (float): The stopping tolerance.

    Returns:
        eigval (foat): The dominant eigenvalue of A.
        eigvec ((n, ) ndarray): The eigenvector corresponding to 'eigval'.
    """
    size = A.shape[0]
    random_vector = []
    for i in xrange(size):
        random_vector.append(np.random.randint(10))
    norm = la.norm(random_vector)
    random_vector = np.array(random_vector, dtype = np.float)
    random_vector /= norm

    while True:
        product = np.dot(A,random_vector)
        new_vector = product / la.norm(product)
        if (la.norm(new_vector - random_vector) < tol):
            break
        random_vector = new_vector

    eigenvector = random_vector
    eigenvalue = np.inner(np.dot(A,eigenvector),eigenvector)/la.norm(eigenvector)
    return eigenvalue, eigenvector

# Problem 5
def QR_algorithm(A, niter, tol):
    """Return the eigenvalues of A using the QR algorithm."""
    H = la.hessenberg(A)
    for i in xrange(niter):
        Q,R = la.qr(H)
        H = np.dot(R,Q)
    S = H
    print S
    eigenvalues = []
    i = 0
    while i < S.shape[0]:
        if i == S.shape[0]-1:
            eigenvalues.append(S[i,i])
        elif abs(S[i+1,i]) < tol:
            eigenvalues.append(S[i,i])
        else:
            a = S[i,i]
            b = S[i,i+1]
            c = S[i+1,i]
            d = S[i+1,i+1]
            B = -1*(a+d)
            C = a*d-b*c
            eigen_plus = (-B + sm.sqrt(B**2 - 4*C))/2.
            eigen_minus = (-B - sm.sqrt(B**2 - 4*C))/2.

            eigenvalues.append(eigen_plus)
            eigenvalues.append(eigen_minus)
            i+=1
        i+=1
    return eigenvalues


# Additional Material
from matplotlib.animation import FuncAnimation

def polynomial_fit_animation():

    x, y = np.load("polynomial.npy").T
    domain = np.linspace(x.min(), x.max(), 200)
    y_vals = np.array([np.poly1d(np.polyfit(x, y, deg=n))(domain)
                                                    for n in xrange(20)])
    plt.plot(x, y, 'k*')
    plt.plot(domain, 2*np.sin(domain), 'k--', lw=1)

    fig = plt.figure(1)
    drawing, = plt.plot([],[], lw=2)
    plt.axis([domain.min()-1, domain.max()+1, -8, 8])

    def update(index):
        drawing.set_data(domain, y_vals[index])
        plt.title(r"$n = {}$".format(index))
        return drawing,

    a = FuncAnimation(fig, update, frames=y.shape[0], interval=1000)
    plt.show()
