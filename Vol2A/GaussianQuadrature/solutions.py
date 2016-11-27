# solutions.py
"""Lab 16: Gaussian Quadrature. Solutions file."""

import numpy as np
from math import sqrt
from scipy import stats
from scipy import linalg as la
from scipy.integrate import quad
from matplotlib import pyplot as plt


# Problem 1
def shift(f, a, b, plot=False):
    """Shift the function f on [a, b] to a new function g on [-1, 1] such that
    the integral of f from a to b is equal to the integral of g from -1 to 1.

    Inputs:
        f (function): a scalar-valued function on the reals.
        a (int): the left endpoint of the interval of integration.
        b (int): the right endpoint of the interval of integration.
        plot (bool): if True, plot f over [a,b] and g over [-1,1] in separate
            subplots.

    Returns:
        The new, shifted function.
    """
    # Define g.
    g = lambda x: f((b - a)*x/2. + (a + b)/2.)

    if plot is True:

        plt.subplot(121)    # Plot f(x) over [a,b]
        x1 = np.linspace(a, b, 200)
        plt.plot(x1, f(x1), 'b-', lw=2)
        plt.title(r"$f(x)$ on $[{}, {}]$".format(a,b))

        plt.subplot(122)    # Plot g(x) over [-1,1]
        x2 = np.linspace(-1, 1, 200)
        plt.plot(x2, g(x2), 'g-', lw=2)
        plt.title(r"$g(x)$ on $[-1, 1]$")

        plt.show()

    return g


# Problem 2
def estimate_integral(f, a, b, points, weights):
    """Estimate the value of the integral of the function f over [a,b].

    Inputs:
        f (function): a scalar-valued function on the reals.
        a (int): the left endpoint of the interval of integration.
        b (int): the right endpoint of the interval of integration.
        points ((n,) ndarray): an array of n sample points.
        weights ((n,) ndarray): an array of n weights.

    Returns:
        The approximate integral of f over [a,b].
    """
    return (b - a) * np.dot(weights, shift(f, a, b, False)(points)) / 2.


# Problem 3
def construct_jacobi(gamma, alpha, beta):
    """Construct the Jacobi matrix."""
    a = - beta / alpha
    b = np.sqrt(gamma[1:] / (alpha[:-1] * alpha[1:]))

    J = np.diag(a)
    B = np.diag(b)
    J[:-1,1:] += B
    J[1:,:-1] += B

    return J


# Problem 4
def points_and_weights(n):
    """Calculate the points and weights for a quadrature over [a,b] with n
    points.

    Returns:
        points ((n,) ndarray): an array of n sample points.
        weights ((n,) ndarray): an array of n weights.
    """

    # Calculate the recurrence coefficients.
    gamma = np.array([(k-1)/float(k) for k in xrange(1,n+1)])
    alpha = np.array([(2*k - 1)/float(k) for k in xrange(1,n+1)])
    beta = np.zeros(n)

    # Get the eigenvalues of the Jacobian.
    J = construct_jacobi(gamma, alpha, beta)
    eigs, vecs = la.eig(J)

    # Get the points and weights from the Jacobi eigenvalues and eigenvectors.
    points = eigs
    weights = 2 * vecs[0]**2

    return points.real, weights.real

    evals, evecs = eig(jac)
    print evecs
    weights = [(evecs[i,0]**2)*2 for i in xrange(evecs.shape[0])]
    return evals, weights


# Problem 5
def gaussian_quadrature(f, a, b, n):
    """Using the functions from the previous problems, integrate the function
    'f' over the domain [a,b] using 'n' points in the quadrature.
    """
    points, weights = points_and_weights(n)
    return estimate_integral(f, a, b, points, weights)

    evals, evecs = eig(jac)
    print evecs
    weights = [(evecs[i,0]**2)*2 for i in xrange(evecs.shape[0])]
    return evals, weights


# Problem 6
def normal_cdf(x):
    """Use scipy.integrate.quad() to compute the CDF of the standard normal
    distribution at the point 'x'. That is, compute P(X <= x), where X is a
    normally distributed random variable with mean = 0 and std deviation = 1.
    """
    return quad(norm.pdf, -5, x)[0]


# ============================== END OF FILE ============================== #

from numpy.random import randn

# Test script
def test(student_module):
    """Test script. Import the student's solutions file as a module.

     5 points for problem 2
    30 points for problem 6
     5 points for problem 7

    Inputs:
        student_module: the imported module for the student's file.

    Returns:
        score (int): the student's score, out of TOTAL.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

def _autoclose(func):
    """function decorator for closing figures automatically."""
    def wrapper(*args, **kwargs):
        try:
            plt.ion()
            return func(*args, **kwargs)
        finally:
            plt.close('all')
            plt.ioff()
    return wrapper

class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine -----------------------------------------------------------
    def test_all(self, student_module, total=40):
        """Grade the provided module on each problem and compile feedback."""
        # Reset feedback and score.
        self.feedback = ""
        self.score = 0

        def test_one(problem, number, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\nProblem %d (%d points):"%(number, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += %d"%points
            except BaseException as e:
                self.feedback += "\n%s: %s"%(self._errType(e),e)

        # Grade each problem.
        test_one(self.problem2, 2, 5)   # Problem 1:  5 points.
        test_one(self.problem6, 6, 30)  # Problem 2: 30 points.
        test_one(self.problem7, 7, 5)   # Problem 2:  5 points.

        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: %d/%d = %s%%"%(
                                    self.score, total, percentage)
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t%s'%comments

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        if isinstance(error, BaseException):
            return str(type(error)).lstrip("<type 'exceptions.").rstrip("'>")
        else:
            return str(error)

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if abs(correct - student) < 1e-6:
            return 1
        else:
            self.feedback += "\n%s"%message
            self.feedback += "\n\tCorrect response: %s"%correct
            self.feedback += "\n\tStudent response: %s"%student
            return 0

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score."""
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of %d: "%points))
            except:
                credit = -1
        if credit != points:
            # Add comments (optionally),
            comments = raw_input("Comments: ")
            if len(comments) > 0:
                self.feedback += "\n%s"%comments
            # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n%s"%message
        return credit

    # Problems ----------------------------------------------------------------
    @_autoclose
    def problem1(self, s):
        """Test shift(). 5 points."""
        s.prob2()
        return self._grade(5, "prob2() failed")

    def problem5(self, s):
        """Test gaussian_quadrature(). 30 points.""" # LOL spread it out...
        f = lambda x: x**2
        points =  10*self._eqTest(21, s.gaussian_quadrature(f, 1, 4, 5),
                            "gaussian_quadrature() failed for f(x) = "
                            "x^2 over [1, 4]")

        g = lambda x: 4*x**3 - 3*x**2 + 2*x - 5
        points += 10*self._eqTest(46, s.gaussian_quadrature(g, 2, 3, 6),
                            "gaussian_quadrature() failed for f(x) = "
                            "4x^3 - 3x^2 + 2x - 5 over [2, 3]")

        h = lambda x: (x-5)**3
        points += 10*self._eqTest(0, s.gaussian_quadrature(h, 3, 7, 5),
                            "gaussian_quadrature() failed for f(x) = "
                            "(x-5)^3 over [3, 7]")
        return points

    def problem6(self, s):
        """Test normal_cdf(). 5 points."""
        points  = 2*self._eqTest(norm.cdf(1), s.normal_cdf(1),
                                        "normal_cdf(1) failed")
        x = randn()
        points += 3*self._eqTest(norm.cdf(x), s.normal_cdf(x),
                                        "normal_cdf({!f}) failed".format(x))
        return points
