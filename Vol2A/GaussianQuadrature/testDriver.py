# testDriver.py
"""Volume 2 Lab 12: Gaussian Quadrature. Test Driver."""

# Decorators ==================================================================

import signal
from functools import wraps
from matplotlib import pyplot as plt

def _autoclose(func):
    """Decorator for closing figures automatically."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            plt.ion()
            return func(*args, **kwargs)
        finally:
            plt.close('all')
            plt.ioff()
    return wrapper

def _timeout(seconds):
    """Decorator for preventing a function from running for too long.

    Inputs:
        seconds (int): The number of seconds allowed.

    Notes:
        This decorator uses signal.SIGALRM, which is only available on Unix.
    """
    assert isinstance(seconds, int), "@timeout(sec) requires an int"

    class TimeoutError(Exception):
        pass

    def _handler(signum, frame):
        """Handle the alarm by raising a custom exception."""
        message = "Timeout after {} seconds".format(seconds)
        print(message)
        raise TimeoutError(message)


    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handler)
            signal.alarm(seconds)               # Set the alarm.
            try:
               return func(*args, **kwargs)
            finally:
                signal.alarm(0)                 # Turn the alarm off.
        return wrapper
    return decorator

# Test Driver =================================================================

import numpy as np
from math import sqrt, pi
from scipy.stats import norm
from scipy.integrate import quad

from inspect import getsourcelines
from solutions import construct_jacobi

np.set_printoptions(suppress=True)


def test(student_module):
    """Grade a student's entire solutions file.

     5 points for problem 1
     5 points for problem 2
     5 points for problem 3
     5 points for problem 4
    15 points for problem 5
     5 points for problem 6

    Inputs:
        student_module: the imported module for the student's file.

    Returns:
        score (int): the student's score, out of 40.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback


class _testDriver(object):
    """Class for testing a student's work.

    Attributes:
        Score (int)
        Feedback (str)
    """

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine ------------------------------------------------------------
    def test_all(self, student_module, total=40):
        """Grade the provided module on each problem and compile feedback."""
        # Reset feedback and score.
        self.feedback = ""
        self.score = 0

        def test_one(problem, label, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\n{} ({} points):".format(label, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += {}".format(points)
            except BaseException as e:
                self.feedback += "\n{}: {}".format(self._errType(e), e)

        # Grade each problem.
        test_one(self.problem1, "Problem 1",  5)  # Problem 1:  5 points.
        test_one(self.problem2, "Problem 2",  5)  # Problem 2:  5 points.
        test_one(self.problem3, "Problem 3",  5)  # Problem 3:  5 points.
        test_one(self.problem4, "Problem 4",  5)  # Problem 4: 15 points.
        test_one(self.problem5, "Problem 5", 15)  # Problem 5:  5 points.
        test_one(self.problem6, "Problem 6",  5)  # Problem 6:  5 points.

        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: {}/{} = {}%".format(
                                    self.score, total, round(percentage, 2))
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t{}'.format(comments)

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        return str(type(error).__name__)

    def _checkCode(self, func, keyword):
        """Check a function's source code for a key word. If the word is found,
        print the code to the screen and prompt the grader to check the code.
        Use this function to detect cheating. Returns a score out of 10.
        """
        code = getsourcelines(func)[0][len(func.__doc__.splitlines())+1 :]
        if any([keyword in line for line in code]):
            print("\nStudent {}() code:\n{}\nCheating? [OK=10, Bad=0]".format(
                                                func.__name__, "".join(code)))
            return self._grade(10)
        return 10

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if np.allclose(correct, student):
            return 1
        else:
            self.feedback += "\n{}".format(message)
            self.feedback += "\n\tCorrect response: {}".format(correct)
            self.feedback += "\n\tStudent response: {}".format(student)
            return 0

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score.
        If full points are not earned, get feedback on the problem.
        """
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of {}: ".format(points)))
            except:
                credit = -1
        if credit != points:
            # Add comments (optionally),
            comments = raw_input("Comments: ")
            if len(comments) > 0:
                self.feedback += "\n{}".format(comments)
            # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n{}".format(message)
        return credit

    # Problems ----------------------------------------------------------------
    @_autoclose
    def problem1(self, s):
        """Test shift(). 5 points."""

        # Define a function and use the student's function to shift it.
        f = lambda x: (x-3)**3
        a,b = 1,4
        g = s.shift(f, a, b, True)

        # Award points for figures and correct shifting.
        points = self._grade(2, "shift() failed")
        points += 3 * self._eqTest(quad(f, a, b)[0], 1.5 * quad(g, -1, 1)[0],
                               "integral of f on [1,4] != (3/2) * integral of "
                               "g on [-1,1] for f(x) = (x-3)^2")
        return points

    @_timeout(2)
    def problem2(self, s):
        """Test estimate_integral(). 5 points."""
        # Define some points and weights.
        s1 = 2 * sqrt(10. / 7.)
        pts = np.array([-sqrt(5 + s1) / 3., -sqrt(5 - s1) / 3., 0.,
                         sqrt(5 - s1) / 3.,  sqrt(5 + s1) / 3.])
        s2 = 13 * sqrt(70)
        weights = np.array([(322 - s2) / 900., (322 + s2) / 900., 128 / 225.,
                            (322 + s2) / 900., (322 - s2) / 900.])

        points = 2 * self._eqTest(0,
                        s.estimate_integral(np.sin, -pi, pi, pts, weights),
                        "estimate_integral() failed for sin(x) over [-pi, pi]")
        points += 3 * self._eqTest(0.00019354294514,
                        s.estimate_integral(np.cos, -pi, pi, pts, weights),
                        "estimate_integral() failed for cos(x) over [-pi, pi]")
        return points

    @_timeout(2)
    def problem3(self, s):
        """Test construct_jacobi(). 5 points."""
        gamma = np.array([(k-1)/float(k) for k in xrange(1,6)])
        alpha = np.array([(2*k - 1)/float(k) for k in xrange(1,6)])
        beta = np.zeros(5)
        return 5 * self._eqTest(construct_jacobi(gamma, alpha, beta),
                                        s.construct_jacobi(gamma, alpha, beta),
                                                "construct_jacobi() failed.")

    @_timeout(2)
    def problem4(self, s):
        """Test points_and_weights(). 5 points."""
        s1 = 2 * sqrt(10. / 7.)
        pts = np.sort([-sqrt(5 + s1) / 3., -sqrt(5 - s1) / 3., 0.,
                        sqrt(5 - s1) / 3.,  sqrt(5 + s1) / 3.])
        s2 = 13 * sqrt(70)
        weights = np.sort([(322 - s2) / 900., (322 + s2) / 900., 128 / 225.,
                           (322 + s2) / 900., (322 - s2) / 900.])
        s_pts, s_weights = s.points_and_weights(5)
        s_pts, s_weights = np.sort(s_pts), np.sort(s_weights)

        points = 2 * self._eqTest(pts, s_pts, "points_and_weights(5) failed "
                                                                    "(points)")
        points += 3 * self._eqTest(weights, s_weights, "points_and_weights(5) "
                                                            "failed (weights)")
        return points

    def problem5(self, s):
        """Test gaussian_quadrature(). 15 points."""
        @_timeout(2)
        def all_tests():
            f = lambda x: x**2
            points =  5 * self._eqTest(21, s.gaussian_quadrature(f, 1, 4, 5),
                                "gaussian_quadrature() failed for f(x) = "
                                "x^2 over [1, 4]")

            g = lambda x: 4*x**3 - 3*x**2 + 2*x - 5
            points += 5 * self._eqTest(46, s.gaussian_quadrature(g, 2, 3, 6),
                                "gaussian_quadrature() failed for f(x) = "
                                "4x^3 - 3x^2 + 2x - 5 over [2, 3]")

            h = lambda x: (x-5)**3
            points += 5 * self._eqTest(0, s.gaussian_quadrature(h, 3, 7, 5),
                                "gaussian_quadrature() failed for f(x) = "
                                "(x-5)^3 over [3, 7]")
            return points
        points = all_tests()

        points *= self._checkCode(s.gaussian_quadrature, "quad(") / 10.
        return int(points)

    @_timeout(2)
    def problem6(self, s):
        """Test normal_cdf(). 5 points."""
        @_timeout(2)
        def one_test(x, n):
            return n * self._eqTest(norm.cdf(x), s.normal_cdf(x),
                                        "normal_cdf({:.4f}) failed".format(x))

        points = one_test(1, 2) + one_test(np.random.randn(), 3)
        points *= self._checkCode(s.normal_cdf, "cdf(") / 10.
        return int(points)


# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    test(solutions)
