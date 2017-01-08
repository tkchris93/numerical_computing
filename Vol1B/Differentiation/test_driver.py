# test_driver.py
"""Volume 1B: Numerical Differentiation. Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout

import numpy as np
from solutions import *

class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1
     5 points for problem 2
    10 points for problem 3
     5 points for problem 4
    10 points for problem 5
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
                            (self.problem3, "Problem 3", 10),
                            (self.problem4, "Problem 4",  5),
                            (self.problem5, "Problem 5", 10),
                            (self.problem6, "Problem 6",  5)    ]

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

         5 points for problem 1
         5 points for problem 2
        10 points for problem 3
         5 points for problem 4
        10 points for problem 5
         5 points for problem 6

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Problems ----------------------------------------------------------------
    @_timeout(2)
    def problem1(self, s):
        """Test centered_difference_quotient(). 5 Points."""

        def _test(func, label):
            pts = np.linspace(-5, 5, 40)
            return self._eqTest(centered_difference_quotient(func, pts),
                                    s.centered_difference_quotient(func, pts),
                                        "centered_difference_quotient() failed"
                                        "for f(x) = {}".format(label), False)

        points  = _test(lambda x: 2*np.sin(x), "sin(x)")
        points += 2 * _test(lambda x: 2*np.abs(4 - x**2), "2 |4 - x^2|")
        points += 2 * _test(lambda x: np.exp(x)/(.5*x**2 + 1),
                                                        "e^x / ((x^2)/2 + 1)")
        return points

    @_timeout(2)
    def problem2(self, s):
        """Test calculate_errors(). 5 points."""

        def _test(func, df, label):
            """Check that |s.centered_difference_quotient() - df(pts)| = err"""
            pts = np.linspace(-5, 5, 40)
            return self._eqTest(calculate_errors(func, df, pts),
                np.abs(s.centered_difference_quotient(func, pts) - df(pts)),
                                        "centered_difference_quotient() failed"
                                        "for f(x) = {}".format(label), False)

        points  = 2 * _test(lambda x: 2*np.sin(x),
                            lambda x: 2*np.cos(x), "sin(x)")
        points += 3 * _test(lambda x: x**5 - x**4 + x**3 - x**2 + x - 1,
                            lambda x: 5*x**4 - 4*x**3 + 3*x**2 - 2*x + 1,
                            "x^5 - x^4 + x^3 - x^2 + x - 1")
        return points

    @_timeout(2)
    def problem3(self, s):
        """Test prob3(). 10 points."""
        ans_1, ans_2 = prob3()

        # Attempt to unpack the student's solutions values.
        try:
            stu_1, stu_2 = s.prob3()
        except (TypeError, ValueError) as e:
            e.message = "prob3() failed to return 2 values"
            raise e

        points  = 5 * self._eqTest(ans_1, stu_1, "Incorrect derivative")
        points += 5 * self._eqTest(ans_2, stu_2, "Incorrect errors")
        return points

    @_timeout(2)
    def problem4(self, s):
        """Test prob4(). 5 points."""
        return 5 * self._eqTest(prob4(), s.prob4(), "prob4() incorrect", False)

    @_timeout(2)
    def problem5(self, s):
        """Test jacobian(). 10 Points."""

        def _test(f, n, m, point, label):
            J1 = jacobian(f, n, m, point)
            J2 = s.jacobian(f, n, m, point)
            return self._eqTest(J1, J2, "jacobian() failed: {}".format(label))

        # Test case: f(x,y,z) = [xy, yz, x-y, 2 + z^2]
        f1 = lambda y: np.array([y[0]*y[1],
                                 y[1]*y[2],
                                 y[0] - y[1],
                                 2 + y[2]**2])
        f1_str = "f(x,y,z) = [xy, yz, x-y, 2 + z^2] at "
        points  = 2 * _test(f1, 3, 4, np.array([1, 1, 1]), f1_str+"(1, 1, 1)")
        points += 2 * _test(f1, 3, 4, np.array([-40, .5, 10]),
                                                        f1_str+"(-40, .5, 10)")

        # Test case: f(x,y,z) = [cos(y), sin(x^2) + sin(y^2), x, y e^x]
        f2 = lambda y: np.array([np.cos(y[1]),
                                 np.sin(y[0]**2) + np.sin(y[1]**2),
                                 y[0],
                                 y[1]*np.exp(y[0])])
        f2_str = "f(x,y,z) = [cos(y), sin(x^2) + sin(y^2), x, y e^x] at "
        points += 3 * _test(f2,2,4,np.array([np.pi, np.pi]), f2_str+"(pi, pi)")
        points += 3 * _test(f2,2,4,np.array([-15, 45]), f2_str+"(-15, 45)")

        return points

    @_timeout(5)
    def problem6(self, s):
        """Test findError(). 5 points."""
        return 5 * self._eqTest(findError(), s.findError(),
                                        "findError() incorrect", compare=False)

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
