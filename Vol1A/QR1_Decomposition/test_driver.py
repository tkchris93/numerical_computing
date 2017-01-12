# test_driver.py
"""Volume 1A: QR 1 (Decomposition). Test Driver."""

import sys
sys.path.insert(1, "../..")
from base_test_driver import BaseTestDriver, _timeout

import numpy as np
from scipy import linalg as la


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

    10 points for problem 1
     5 points for problem 2
     5 points for problem 3
    10 points for problem 4
    10 points for problem 5

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.total = 40
        self.problems = [   (self.problem1, "Problem 1", 10),
                            (self.problem2, "Problem 2",  5),
                            (self.problem3, "Problem 3",  5),
                            (self.problem4, "Problem 4", 10),
                            (self.problem5, "Problem 5", 10)    ]
        self._feedback_newlines = True

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

        10 points for problem 1
         5 points for problem 2
         5 points for problem 3
        10 points for problem 4
        10 points for problem 5

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _qrTestCase(m, n):
        """Generate an nonsingular mxn matrix."""
        A = np.random.randint(1,10,(m,n)).astype(np.float)
        if np.linalg.matrix_rank(A) != n:
            return TestDriver._qrTestCase(m,n)
        return A[:,la.qr(A, pivoting=True)[-1]]

    @_timeout(2)
    def _qrTest(self, m, n, func):
        """Do an mxn test of a QR factorization via func() worth 5 points."""
        A = self._qrTestCase(m,n)
        stu = func(A.copy())
        try:
            Q,R = stu
        except(TypeError, ValueError):
            raise ValueError("{} failed to return 2 arrays".format(
                                                                func.__name__))
        pts = 5
        if not all(np.allclose(*x) for x in [(A, Q.dot(R)), (np.triu(R), R),
                                        (np.eye(Q.shape[1]), np.dot(Q.T, Q))]):
            pts = 3
            self.feedback += "\n\n{}\nA =\n{}".format('- '*20, A)
            if not np.allclose(np.triu(R), R):
                self.feedback += "\nR not upper triangular:\n{}".format(R)
                pts -= 1
            if not np.allclose(np.eye(Q.shape[1]), np.dot(Q.T, Q)):
                self.feedback += "\nQ not orthonormal:\n{}".format(Q)
                pts -= 2
            pts += 2*self._eqTest(A, Q.dot(R), "A != QR")
        return pts

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test qr_gram_schmidt(). 10 points."""
        points = sum([self._qrTest(4, 4, s.qr_gram_schmidt),
                      self._qrTest(8, 6, s.qr_gram_schmidt)])
        return int(points * self._checkCode(s.qr_gram_schmidt, "qr("))

    def problem2(self, s):
        """Test abs_det(). 5 points."""

        @_timeout(2)
        def _test(n,p):
            """Do an nxn test case worth p points."""
            A = self._qrTestCase(n,n)
            return p * self._eqTest(abs(la.det(A)), s.abs_det(A),
                            "abs_det(A) failed for A =\n{}".format(A))

        points = _test(2, 1) + _test(5, 2) + _test(10, 2)
        return int(points * self._checkCode(s.abs_det, "det("))

    def problem3(self, s):
        """Test solve(). 5 points."""

        @_timeout(2)
        def _test(n,p):
            """Do an nxn test case worth p points."""
            A = self._qrTestCase(n,n)
            b = np.random.randint(1,10,n)
            return p * self._eqTest(la.solve(A, b), s.solve(A, b),
                        "solve(A, b) failed for A =\n{}\nb=\n{}".format(A,b))

        points = _test(2, 1) + _test(5, 2) + _test(10, 2)
        return int(points * self._checkCode(s.abs_det, "solve("))

    def problem4(self, s):
        """Test qr_householder(). 10 points."""
        points =  sum([self._qrTest( 5, 5, s.qr_householder),
                       self._qrTest(10, 6, s.qr_householder)])
        return int(points * self._checkCode(s.qr_householder, "qr("))

    def problem5(self, s):
        """Test hessenberg(). 10 points."""

        @_timeout(2)
        def _test(n):
            """Do an nxn test worth 5 points."""
            A = self._qrTestCase(n,n)
            stu = s.hessenberg(A.copy())
            try:
                H,Q = stu
            except(TypeError, ValueError):
                raise ValueError("hessenberg() failed to return two arrays")

            pts = 5
            if not all(np.allclose(*x) for x in [(np.triu(H, -1), H),
                                        (np.eye(Q.shape[1]), np.dot(Q.T, Q)),
                                                (A, np.dot(Q, H.dot(Q.T)))]):
                pts = 3
                self.feedback += "\n\n{}\nA =\n{}".format('- '*20, A)
                if not np.allclose(np.triu(H, -1), H):
                    self.feedback += "\nH not upper Hessenberg:\n{}".format(H)
                    pts -= 1
                if not np.allclose(np.eye(Q.shape[1]), np.dot(Q.T, Q)):
                    self.feedback += "\nQ not orthonormal:\n{}".format(Q)
                    pts -= 2
                pts += 2*self._eqTest(A, np.dot(Q, H.dot(Q.T)), "A != QHQ^T")
            return pts

        points = _test(4) + _test(10)
        return int(points * self._checkCode(s.hessenberg, "hessenberg("))

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
