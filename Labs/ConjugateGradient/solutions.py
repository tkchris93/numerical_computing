import numpy as np
from scipy import linalg as la
from scipy import optimize as opt
from matplotlib import pyplot as plt

# Problem 1
def conjugateGradient(b,x0,Q,tol = .0001):
    """Implement the Conjugate Gradient Method
    
    Parameters:
    b  ((n, ) ndarray)
    x0 ((n, ) ndarray)
    Q  ((n,n) ndarray)
    tol (float)
    
    Returns:
        x ((n, ) ndarray): The solution given by the Conjugate Gradient Method
        to the linear systm Qx = b
    """
    xk = x0
    rk = Q.dot(x0)-b
    dk = -rk
    k = 0
    while la.norm(rk) > tol:
        alphak = rk.T.dot(rk)/dk.T.dot(Q.dot(dk))
        xk1 = xk + alphak*dk
        rk1 = rk + alphak*Q.dot(dk)
        betak1 = rk1.T.dot(rk1)/rk.T.dot(rk)
        dk1 = -rk1 + betak1*dk
        k = k+1
        xk = xk1
        rk = rk1
        dk = dk1
    return xk1

# Problem 2
def prob2(filename = 'linregression.txt'):
    """Use the conjugateGradient() function to solve the linear regression problem.
    Using the data from linregression.txt.  Return the solution x*."""
    
    data = np.loadtxt(filename)
    m,n = data.shape
    b = data[:,0]
    A = np.hstack((np.ones((m,1)),data[:,1:]))
    x0 = np.random.random(n)
    return conjugateGradient(A.T.dot(b),x0,A.T.dot(A))

# Problem 3
def prob3(filename = 'logregression.txt'):
    """Find the maximum likelihood estimate for the data in logregression.txt.
    Use the function fmin_cg() from scipy.optimize. """
    def objective(b):
        return (np.log(1+np.exp(x.dot(b))) - y*(x.dot(b))).sum()
    
    data = np.loadtxt(filename)
    m,n = data.shape
    y = np.array([0, 0, 0, 0, 1, 0, 1, 0, 1, 1])
    x = np.ones((10, 2))
    x[:,1] = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    y = data[:,0]
    x = np.hstack((np.ones((m,1)),data[:,1:]))
    guess = np.random.random(4)
    b = opt.fmin_cg(objective, guess)
    dom = np.linspace(0, 1.1, 100)
    plt.plot(x, y, 'o')
    plt.plot(dom, 1./(1+np.exp(-b[0]-b[1]*dom)))
    plt.show()
    return b
    
if __name__ == '__main__':
    n = 10
    A = np.random.random((n,n))
    Q = A.T.dot(A)
    b = np.random.random(n)
    x0 = np.random.random(n)
    x = conjugateGradient(b, x0, Q)
    print np.allclose(x, la.solve(Q,b))
    print prob2()
    print prob3()