# test_driver.py
"""Volume 2B: Interior Point 2 (Quadratic Optimization). Test Driver."""

import sys
sys.path.insert(1, "../..")
from base_test_driver import BaseTestDriver, _timeout, _autoclose

import numpy as np
from solutions import portfolio


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

    20 points for problems 1-2
    10 points for problem 3
    10 points for problem 4

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.total = 40
        self.problems = [   (self.problem2, "Problems 1-2", 20),
                            (self.problem3, "Problem 3", 10),
                            (self.problem4, "Problem 4", 10)    ]

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

        20 points for problems 1-2
        10 points for problem 3
        10 points for problem 4

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Helper functions --------------------------------------------------------
    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if not isinstance(student, np.ndarray):
            raise TypeError("Failed to return a NumPy array")
        return BaseTestDriver._eqTest(self, correct, student, message)

    # Problems ----------------------------------------------------------------
    @_timeout(5)
    def problem2(self, s):
        """Test qInteriorPoint(). 20 points."""

        Q = np.array([[1,-1.],[-1,2]])
        c = np.array([-2,-6.])
        A = np.array([[-1, -1], [1, -2.], [-2, -1], [1, 0], [0,1]])
        b = np.array([-2, -2, -3., 0, 0])
        x0 = np.array([.5, .5])
        y0 = np.ones(5)
        m0 = np.ones(5)
        point, value = s.qInteriorPoint(Q=Q, c=c, A=A, b=b, guess=(x0,y0,m0))
        return 20 * self._eqTest(np.array([2/3., 4/3.]), point,
                            "qInteriorPoint() failed for the QP in Problem 2")

    @_autoclose
    def problem3(self, s):
        """Test the circus tent problem. 10 points."""
        s.circus(n=15)
        return self._grade(10, "Incorrect circus tent graph with n=15")

    @_timeout(5)
    def problem4(self, s):
        """Test the portfolio optimization problem. 10 points."""

        try:
            s1, s2 = s.portfolio(filename="portfolio.txt")
            s1, s2 = np.ravel(s1), np.ravel(s2)
        except ValueError as e:
            if str(e) == "too many values to unpack":
                raise ValueError("Failed to return two NumPy arrays")
            else: raise
        except TypeError as e:
            if "is not iterable" in str(e):
                raise TypeError("Failed to return two NumPy arrays")
            else: raise
        c1, c2 = portfolio(filename="portfolio.txt")

        points  = 5 * self._eqTest(c1, s1,
                              "Incorrect percentages (with short selling)")
        points += 5 * self._eqTest(c2, s2,
                              "Incorrect percentages (with short selling)")
        return points

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
