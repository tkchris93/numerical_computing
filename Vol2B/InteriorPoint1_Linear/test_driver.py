# test_driver.py
"""Volume 2B: Interior Point 1. Test Driver."""

import sys
sys.path.insert(1, "../..")
from base_test_driver import BaseTestDriver, _timeout, _autoclose

import numpy as np
from solutions import randomLP


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

    30 points for problems 1-4
    10 points for problem 5

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.total = 40
        self.problems = [   (self.problem4, "Problems 1-4", 30),
                            (self.problem5, "Problem 5", 10)    ]

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

        30 points for problem 1-4
        10 points for problem 5

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Problems ----------------------------------------------------------------
    @_timeout(5)
    def problem4(self, s):
        """Test interiorPoint(). 30 points."""

        def _test(m,n):
            """Do a single mxn test case."""
            A, b, c, x = s.randomLP(m,n)
            point, value = s.interiorPoint(A=A, b=b, c=c)
            return np.allclose(x, point[:n])

        points = 0
        # Do 200 square tests and 100 rectangular tests.
        for _ in xrange(200):
            m = np.random.randint(3,10)
            points += _test(m,m)
        for _ in xrange(100):
            n = np.random.randint(3,10)
            m = np.random.randint(n,20)
            points += _test(m,n)

        self.feedback += "\nPassed {}/300 tests".format(points)
        return points // 10

    @_autoclose
    def problem5(self, s):
        """Test leastAbsoluteDeviations(). 10 points."""
        s.leastAbsoluteDeviations()
        return self._grade(10)

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
