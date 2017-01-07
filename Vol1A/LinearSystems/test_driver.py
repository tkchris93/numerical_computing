# test_driver.py
"""Volume 1A: Linear Systems. Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout, _autoclose

import numpy as np
from scipy import sparse
from scipy.linalg import lu_factor, solve
from inspect import getsourcelines
from solutions import ref, lu, prob5


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1
    10 points for problem 2
    10 points for problem 3
     5 points for problem 4
     5 points for problem 5
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
                            (self.problem2, "Problem 2", 10),
                            (self.problem3, "Problem 3", 10),
                            (self.problem4, "Problem 4",  5),
                            (self.problem5, "Problem 5",  5),
                            (self.problem6, "Problem 6",  5)    ]
        self._feedback_newlines = True

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

         5 points for problem 1
        10 points for problem 2
        10 points for problem 3
         5 points for problem 4
         5 points for problem 5
         5 points for problem 6

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _luTestCase(n):
        """Generate an nxn matrix that does not require pivoting with the
        Gaussian elimination or the LU Decomposition.
        """
        A = np.random.randint(0,10,(n,n))
        _, piv = lu_factor(A)
        P = np.eye(n)
        for i,j in enumerate(piv):
            P[i], P[j] = P[j].copy(), P[i].copy()
        return P.dot(A).astype(np.float)

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test ref(). 5 points."""

        @_timeout(2)
        def _test(n, p):
            """Do an nxn test case worth p points."""
            A = self._luTestCase(n)
            return p * self._eqTest(ref(A), s.ref(A), "ref() failed.")

        points = _test(3, 1) + _test(4, 2) + _test(5, 2)
        return int(points * self._checkCode(s.ref, "lu_factor"))

    def problem2(self, s):
        """Test lu(). 10 points."""

        @_timeout(2)
        def _test(n):
            """Do an nxn test case worth 5 points."""
            A = self._luTestCase(n)
            L1, U1 = lu(A)
            if not np.allclose(L1.dot(U1), A):
                return _test(n)
            stu = s.lu(A.copy())
            try:
                L2, U2 = stu
            except(TypeError, ValueError):
                raise ValueError("lu() failed to return two arrays")

            pts = 5
            if not all(np.allclose(*x) for x in [(np.tril(L2), L2),
                   (np.triu(U2), U2), (L1, L2), (U1, U2), (A, L2.dot(U2))]):
                pts = 2
                self.feedback += "\n\n{}\nA =\n{}".format('- '*20, A)
                if not np.allclose(np.tril(L2), L2):
                    self.feedback += "\nL not lower triangular:\n{}".format(L2)
                    pts -= 1
                if not np.allclose(np.triu(U2), U2):
                    self.feedback += "\nU not upper triangular:\n{}".format(U2)
                    pts -= 1
                pts += self._eqTest(L1, L2, "lu() failed (L incorrect)")
                pts += self._eqTest(U1, U2, "lu() failed (U incorrect)")
                pts += self._eqTest(A, L2.dot(U2), "lu() failed (A != LU)")
            return pts

        points = _test(4) + _test(6)
        return int(points * self._checkCode(s.lu, "lu_factor"))


    def problem3(self, s):
        """Test solve(). 10 points."""

        @_timeout(2)
        def _test(n, p):
            """Do an nxn test case worth p points."""
            A = self._luTestCase(n)
            b = np.random.randint(0, 10, n).astype(np.float)
            stu = s.solve(A, b)
            if not np.allclose(b, A.dot(stu)):
                self.feedback += "\n\n{}\nA =\n{}\nb =\n{}".format('- '*20,A,b)
                return p * self._eqTest(solve(A,b), stu, "solve() failed")
            else:
                return p

        points = _test(3, 3) + _test(4, 3) + _test(5, 4)
        return int(points * self._checkCode(s.solve, "solve("))

    @_autoclose
    def problem4(self, s):
        """Test prob4(). 5 points."""

        print("Running prob4()...(60 second time limit)")
        _timeout(60)(s.prob4)()
        print("""\nSpecifications:
        1. Plots system size n versus execution times.              (1 point)
        2. Four lines, clearly marked:                              (2 points)
            - la.inv()                          (slowest)
            - la.solve()                        (in the middle)
            - la.lu_factor() and la.lu_solve()  (in the middle)
            - la.lu_solve() alone               (fastest)
        3. The difference between each line is apparent.            (2 points)
        (Plot could be loglog or linlin as long as it is clear)
        (Title and axis labels unnecessary)""")
        return self._grade(5, "prob4() does not match specifications")

    @_timeout(3)
    def problem5(self, s):
        """Test prob5(). 5 points."""

        def _test(n, p):
            """Do an nxn test case with p points."""
            stu = prob5(n)
            if not sparse.issparse(stu):
                self.feedback += "\n\tFailed to return a scipy.sparse matrix"
                return 0
            else:
                if type(stu) is not sparse.dia.dia_matrix:
                    self.feedback += "\n\tReturn type should be sparse "
                    self.feedback += "diagonal matrix"
                    stu = sparse.dia_matrix(stu)
                sol = prob5(n)
                if not self._eqTest(stu.offsets,sol.offsets,"prob5({}) failed "
                        "(comparing indices of nonzero diagonals".format(n)):
                    p -= 1
                return p*self._eqTest(stu.data, sol.data, "prob5({}) failed "
                        "(comparing nonzero diagonals)".format(n))

        return _test(100, 2) + _test(100000, 3)

    @_autoclose
    def problem6(self, s):
        """Test prob6(). 5 points."""

        print("\nRunning prob5()...(60 second time limit)")
        _timeout(60)(s.prob6)()
        print("""\nSpecifications:
        1. Plots system size n versus execution times.              (1 point)
        2. Two lines, clearly marked:                               (2 points)
            - scipy.sparse.linalg.spsolve()     (faster)
            - scipy.linalg.solve()              (slower)
        3. The difference between each line is apparent.            (2 points)
        (Plot could be loglog or linlin as long as it is clear)
        (Title and axis labels unnecessary)""")
        return self._grade(5, "prob6() does not match specifications")

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
