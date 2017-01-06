# test_driver.py

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout, _autoclose

import numpy as np
from scipy.misc import imread
from scipy import linalg as la
from solutions import truncated_svd, lowest_rank_approx


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

    10 points for problem 1
    10 points for problem 2
     5 points for problem 3
     5 points for problem 4
    10 points for problem 5

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.problems = [   (self.problem1, "Problem 1", 10),
                            (self.problem2, "Problem 2", 10),
                            (self.problem3, "Problem 3",  5),
                            (self.problem4, "Problem 4",  5),
                            (self.problem5, "Problem 5", 10)    ]

    # Helper functions --------------------------------------------------------
    @staticmethod
    def _test_case(m, n):
        A = np.random.randint(1, 10, (m,n)).astype(np.float)
        if np.linalg.matrix_rank(A) != min(m,n):
            return TestDriver._test_case(m, n)
        return A

    # Problems ----------------------------------------------------------------
    # TODO: This problem would test a true SVD or a compact SVD correctly,
    # but it may fail for the truncated SVD where information is lost.
    @_timeout(2)
    def problem1(self, s):
        """Test truncated_svd(). 10 points."""

        def _test(m, n, r):
            """Do an mxn test case, truncating to rank r."""

            # Generate a full-rank test matrix.
            A = self._test_case(m, n)

            # Run student code.
            stu = s.truncated_svd(A.copy(), r)
            try:
                U, sig, Vh = stu
            except(TypeError, ValueError):
                raise ValueError("truncated_svd() failed to return 3 arrays")

            S = np.diag(sig)

            # Check shapes (1 points)
            pts  = self._eqTest((m,r), U.shape, "U incorrect shape") / 3.
            pts += self._eqTest(r, sig.size, "'s' incorrect size") / 3.
            pts += self._eqTest((r,n), Vh.shape, "Vh incorrect shape") / 3.

            # Check factorization properties (3 points)
            failures = np.array([not np.allclose(*x) for x in [
                                    (np.eye(Vh.shape[0]), np.dot(Vh, Vh.T)),
                                        (np.eye(U.shape[1]), np.dot(U.T, U)),
                                            # (A, U.dot(S).dot(Vh))
                                            ]])

            if pts == 1 and any(failures):
                self.feedback += "\n\n{}\nA =\n{}".format('- '*20, A)
                # if failures[2]:      # A = U S Vh        (1 point)
                    # pts += self._eqTest(A, U.dot(S).dot(Vh).real,"A != U S Vh")
                pts += 1 #
                pts += 2
                if failures[1]:      # U orthonormal     (1 point)
                    self.feedback += "\nU not orthonormal:\n{}".format(U)
                    pts -= 1
                if failures[0]:      # Vh orthonormal    (1 point)
                    self.feedback += "\nVh not orthonormal:\n{}".format(Vh)
                    pts -= 1
            else:
                pts += 3

            # Check singular values are sorted (1 point).
            pts += self._eqTest(np.sort(sig)[::-1], sig,
                                                "Singular values not sorted")

            return pts

        self._feedback_newlines = True
        points = _test(5, 5, 3) + _test(10, 5, 5)
        self._feedback_newlines = False
        return int(points * self._checkCode(s.truncated_svd, "svd("))

    @_autoclose
    def problem2(self, s):
        """Test visualize_svd(). 10 points."""
        s.visualize_svd()
        print("""\nSpecifications:
        Four plots,
        1.1) Should look like 3:00 on a clock
        1.2) Looks like Mr. Pacman but backwards, 7:50 on a clock
        2.1) Looks like 1.2, but compressed
        2.2) Looks like 1.1, but comressed and shifted up to a slight angle

        (Aspect ratio may be stretched)""")
        return self._grade(10)

    @_timeout(2)
    def problem3(self, s):
        """Test svd_approx(). 5 points."""

        def _test(m, n, r):
            A = self._test_case(m, n)

            # Check that ||A - Ahat||_2 = sig[r].
            _, sig, _ = la.svd(A)
            stu_error = la.norm(A - s.svd_approx(A.copy(), r), ord=2)

            return self._eqTest(sig[r], stu_error, "svd_approx() failed "
                            "with k = {} (showing ||A - Ahat||_2)".format(r))

        points = 2*_test(6, 6, 4) + 3*_test(12, 12, 8)
        return points

    @_timeout(2)
    def problem4(self, s):
        """Test lowest_rank_approx(). 5 points."""

        def _test(filename, err):
            image = imread(filename, flatten=True)

            # Check that ||A - Ahat||_2 = sig[r].
            _, sig, _ = la.svd(image)
            stu_error = la.norm(image - s.lowest_rank_approx(image,err), ord=2)

            return self._eqTest(sig[np.argmax(sig < err)], stu_error,
                                    "lowest_rank_approx() failed with error = "
                                    "{} (showing ||A - Ahat||_2)".format(err))

        return 2*_test("hubble.jpg", 3.5) + 3*_test("hubble.jpg", 10.)

    def problem5(self, s):
        """Test compress_image(). 10 points."""

        @_autoclose
        def _test(n):
            """Do a test case worth 5 points."""
            s.compress_image("hubble_image.jpg", n)
            print("""\nSpecifications:
            Should display the hubble image and its compressed image
            (Aspect ratio may be stretched)""")
            return self._grade(5)

        return _test(7) + _test(40)

# Main Routine ================================================================

def test(student_module, total=40):
    """Grade a student's entire solutions file.

    10 points for problem 1
    10 points for problem 2
     5 points for problem 3
     5 points for problem 4
    10 points for problem 5

    Inputs:
        student_module: the imported module for the student's file.
        total (int): the total possible score.

    Returns:
        score (int): the student's score, out of 'total'.
        feedback (str): a printout of results for the student.
    """
    tester = TestDriver()
    tester.test_all(student_module, total)
    return tester.score, tester.feedback

# Validation ==================================================================

if __name__ == '__main__':
    import solutions
    test(solutions)
