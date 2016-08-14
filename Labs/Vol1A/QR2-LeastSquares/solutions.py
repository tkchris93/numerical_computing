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


# Problem 3
def polynomial_fit():
    """Load the data from polynomial.npy. Use least squares to calculate
    the polynomials of degree 3, 5, 7, and 19 that best fit the data.

    Plot the original data points and each least squares polynomial together
    in individual subplots.
    """
    # Load the data and define a more refined domain for plotting.
    x, y = np.load("polynomial.npy").T
    domain = np.linspace(x.min(), x.max(), 200)

    for i,n in enumerate([3, 5, 7, 19]):

        # Use least squares to compute the coefficients of the polynomial.
        coeffs = la.lstsq(np.vander(x, n+1), y)[0]
        # coeffs = np.polyfit(x, y, deg=n)

        # Plot the polynomial and the data points in an individual subplot.
        plt.subplot(2,2,i+1)
        plt.plot(x, y, 'k*')
        plt.plot(domain, np.polyval(coeffs, domain), 'b-', lw=2)
        plt.plot(domain, 2*np.sin(domain), 'k--')
        plt.title(r"$n = {}$".format(n))
        plt.axis([-6,6,-3,3])

    plt.suptitle("Solution to Problem 3")
    plt.show()


def plot_ellipse(a, b, c, d, e):
    """Plot an ellipse of the form ax^2 + bx + cxy + dy + ey^2 = 1."""
    theta = np.linspace(0, 2*np.pi, 200)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    A = a*(cos_t**2) + c*cos_t*sin_t + e*(sin_t**2)
    B = b*cos_t + d*sin_t
    r = (-B + np.sqrt(B**2 + 4*A))/(2*A)

    plt.plot(r*cos_t, r*sin_t, lw=2)
    plt.gca().set_aspect("equal", "datalim")

# Problem 4
def ellipse_fit():
    """Load the data from ellipse.npy. Use least squares to calculate the
    ellipse that best fits the data.

    Plot the original data points and the least squares ellipse together.
    """
    # Load the data and construct the matrix A and the vector b.
    x, y = np.load("ellipse.npy").T
    A = np.column_stack((x**2, x, x*y, y, y**2))
    b = np.ones_like(x)

    # Use least squares to calculate the ellipse parameters.
    a, b, c, d, e = la.lstsq(A, b)[0]

    # Plot the results.
    plt.plot(x, y, 'k*')
    plot_ellipse(a, b, c, d, e)
    plt.show()


# Problem 5
def power_method(A, tol=1e-12, max_iters=20):
    """Compute the dominant eigenvalue of A and its corresponding eigenvector.

    Inputs:
        A ((n,n) ndarray): A square matrix.
        tol (float): The stopping tolerance.

    Returns:
        eigval (foat): The dominant eigenvalue of A.
        eigvec ((n, ) ndarray): The eigenvector corresponding to 'eigval'.
    """
    # Choose a random x_0 with norm 1.
    x = np.random.random(A.shape[0])
    x /= la.norm(x)

    for _ in xrange(max_iters):
        # x_{k+1} = Ax_k / ||Ax_k||
        w = np.dot(A, x)
        x_new = w / la.norm(w)
        # Check for convergence.
        if la.norm(x_new - x) < tol:
            break
        x = x_new

    eigval = np.dot(np.conj(x), np.dot(A,x)) / np.dot(np.conj(x),x)
    return eigval, x


# Problem 6
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

'''
def qralg(T, shift=True):
    """Run the QR algorithm on the real tridiagonal matrix 'T'."""

    Tnew = np.array(T, dtype=np.float64, copy=True)
    m,n = Tnew.shape
    errs = [T[-1,-1]]
    if m == 1:
        return Tnew, errs

    while abs(Tnew[-1,-2]) > 1e-12:
        if shift:
            a, b = Tnew[-1,-1], Tnew[-1,-2]
            d = (Tnew[-2,-2] - a)/2.
            s = np.sign(d)
            if s == 0: s = 1
            mu = a - s*b**2/(np.abs(d) + np.sqrt(d**2 + b**2))
            Mu = np.eye(m)*mu
            Q,R = la.qr(Tnew - Mu)
            Tnew = R.dot(Q) + Mu
        else:
            Q,R = la.qr(Tnew)
            Tnew = R.dot(Q)
        Tnew = _perfect_symmetry(Tnew)
        errs.append(Tnew[-1,-2])

    return Tnew, errs
'''

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
