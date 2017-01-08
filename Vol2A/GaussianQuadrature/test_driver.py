# test_driver.py
"""Volume 2A: Gaussian Quadrature. Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _autoclose, _timeout

import numpy as np
from math import sqrt, pi
from scipy.stats import norm
from scipy.integrate import quad

from solutions import construct_jacobi


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1
     5 points for problem 2
     5 points for problem 3
     5 points for problem 4
    15 points for problem 5
     5 points for problem 6

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.total = 40
        self.problems = [   (self.problem1, "Problem 1",  5),
                            (self.problem2, "Problem 2",  5),
                            (self.problem3, "Problem 3",  5),
                            (self.problem4, "Problem 4",  5),
                            (self.problem5, "Problem 5", 15),
                            (self.problem6, "Problem 6",  5)    ]

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
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
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

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

        points *= self._checkCode(s.gaussian_quadrature, "quad(")
        return int(points)

    @_timeout(2)
    def problem6(self, s):
        """Test normal_cdf(). 5 points."""
        @_timeout(2)
        def one_test(x, n):
            return n * self._eqTest(norm.cdf(x), s.normal_cdf(x),
                                        "normal_cdf({:.4f}) failed".format(x))

        points = one_test(1, 2) + one_test(np.random.randn(), 3)
        points *= self._checkCode(s.normal_cdf, "cdf(")
        return int(points)

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
