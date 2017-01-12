# test_driver.py
"""Volume 1A: QR 2 (Least Squares and Computing Eigenvalues). Test Driver."""

import sys
sys.path.insert(1, "../..")
from base_test_driver import BaseTestDriver, _timeout, _autoclose

import numpy as np
from scipy import linalg as la


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1
     5 points for problem 2
     5 points for problem 3
     5 points for problem 4
    10 points for problem 5
    10 points for problem 6

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
                            (self.problem5, "Problem 5", 10),
                            (self.problem6, "Problem 6", 10)    ]
        self._feedback_newlines = True

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

         5 points for problem 1
         5 points for problem 2
         5 points for problem 3
         5 points for problem 4
        10 points for problem 5
        10 points for problem 6

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)


    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test least_squares(). 5 points."""

        @_timeout(2)
        def _test(m,n,p):
            """Do an mxn test case worth p points."""
            A = np.random.random((m,n))
            b = np.random.random(m)
            return p * self._eqTest(la.lstsq(A,b)[0], s.least_squares(A,b),
                        "least_squares(A, b) failed for A.shape = {}, "
                        "b.shape = {}".format(A.shape, b.shape))

        points = _test(5, 2, 1) + _test(10, 8, 2) + _test(100, 50, 2)
        return int(points * self._checkCode(s.least_squares, "lstsq("))

    @_autoclose
    def problem2(self, s):
        """Test line_fit(). 5 points."""

        s.line_fit()
        print("""\nSpecifications:
        1. Scatter plot of year versus price index      (2 points)
        2. Positive-slope regression line               (3 points)
        (Title and legend unnecessary)""")
        points = self._grade(5, "line_fit() plot incorrect")
        return int(points * self._checkCode(s.line_fit, "lstsq("))

    @_autoclose
    def problem3(self, s):
        """Test polynomial_fit(). 5 points."""

        s.polynomial_fit()
        print("""\nSpecifications:
        1. 4 subplots, clearly labeled                  (1 point)
        2. Scatter plot of data on each subplot         (1 point)
        3. 1st polynomial isn't a great fit             (1 point)
        4. 2nd, 3rd, and 4th polynomials are good fits  (2 points)
        (Title and legend unnecessary)""")
        points = self._grade(5, "polynomial_fit() plot incorrect")
        return int(points * self._checkCode(s.polynomial_fit, "polyfit("))

    @_autoclose
    def problem4(self, s):
        """Test ellipse_fit(). 5 points."""

        s.ellipse_fit()
        print("""\nSpecifications:
        1. Scatter plot of data points                  (2 points)
        2. Best-fit ellipse                             (3 points)
        (Title and legend unnecessary)""")
        return self._grade(5, "ellipse_fit() plot incorrect")

    def problem5(self, s):
        """Test power_method(). 10 points."""

        @_timeout(2)
        def _test(n):
            """Do an nxn test worth 5 points."""
            A = np.random.random((n,n))
            eigs, vecs = la.eig(A)
            loc = np.argmax(eigs)
            eig, vec = eigs[loc], vecs[:,loc]
            try:
                stueig, stuvec = s.power_method(A, 20, 1e-12)
            except(TypeError, ValueError):
                raise ValueError("power_method() failed to return two objects")
            pts = 2 * self._eqTest(eig, stueig,
                            "power_method() failed (dominant eigenvalue)")
            pts += 3 * self._eqTest(np.round(A.dot(stuvec), 12),
                                    np.round(stueig * stuvec, 12),
                                    "power_method() failed (Ax != eig * x")
            return pts

        points = _test(4) + _test(10)
        return int(points * self._checkCode(s.power_method, "eig("))

    def problem6(self, s):
        """Test qr_algorithm(). 10 points."""

        @_timeout(2)
        def _test(n):
            """Do an nxn test worth 5 points."""
            A = np.random.randint(1,5,(n,n))
            A += A.T                            # Test symmetric matrices only.
            eigs = np.sort(la.eig(A)[0])
            stueigs = np.sort(s.qr_algorithm(A, 200, 1e-16))
            return 5 * self._eqTest(eigs, stueigs,
                                "qr_algorithm(A) failed for A =\n{}".format(A))

        points = _test(4) + _test(5)
        return int(points * self._checkCode(s.qr_algorithm, "eig("))

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
