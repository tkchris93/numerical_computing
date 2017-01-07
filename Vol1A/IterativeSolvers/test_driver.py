# test_driver.py
"""Volume 1A: Iterative Solvers. Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout, _autoclose

import numpy as np
from scipy import sparse
from scipy import linalg as la
from solutions import *


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

    5 points for problem 1
    5 points for problem 2
    5 points for problem 3
    5 points for problem 4
    5 points for problem 5
    5 points for problem 6
    5 points for problem 7
    5 points for problem 8
    5 points for problem 9

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        # self._feedback_newlines = True
        self.problems = [   (self.problem1, "Problem 1", 5),
                            (self.problem2, "Problem 2", 5),
                            (self.problem3, "Problem 3", 5),
                            (self.problem4, "Problem 4", 5),
                            (self.problem5, "Problem 5", 5),
                            (self.problem6, "Problem 6", 5),
                            (self.problem7, "Problem 7", 5),
                            (self.problem8, "Problem 8", 5),
                            (self.problem9, "Problem 9", 5)     ]

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test Problem 1. 5 points."""

        @_timeout(2)
        def _test(n):

            points = 0
            A = diag_dom(n)
            b = np.random.rand(n)
            #s.jacobi_sol = jacobi_method(A,b)
            #sol = la.solve(A,b)

            #return 5*self._eqTest((sol), (s.jacobi_sol), "jacobi_method() failed")
            points += 3*self._eqTest(np.round(la.solve(A,b)[0],4), np.round(s.jacobi_method(A,b)[0],4), "jacobi_method() failed")
            points += 2*self._eqTest(np.round(la.solve(A,b)[1],3), np.round(s.jacobi_method(A,b)[1],3), "jacobi_method() failed")

            return points


        points = (_test(5) + _test(10) + _test(50) + _test(100)) / 4.

        return int(points * self._checkCode(s.jacobi_method, "solve("))

    @_autoclose
    def problem2(self, s):
        """Test jacobi_method() and gauss_seidel() plots. 5 points."""
        A = np.array([[2,0,-1],[-1,3,2],[0,1,3]])
        b = np.array([3,3,-1])
        s.jacobi_method(A,b,plot=True)
        s.gauss_seidel(A,b,plot=True)

        print("""\nSpecifications:
        1. Absolute error of Approximation versus number of iterations.              (1 point)
        2. Two lines, clearly marked:                               (2 points)
            - Guass (faster)
            - Jacobi Method (slower)
        3. The difference between each line is apparent.            (2 points)
        (Plot could be loglog or linlin as long as it is clear)
        (Title and axis labels unnecessary)""")
        return self._grade(5, "prob2() does not match specifications")

    def problem3(self, s):
        """Test Problem 3. X points."""
        points = 0

        @_timeout(2)
        def _test(n):
            results = []
            A = diag_dom(n)
            b = np.random.rand(n)
            s.jacobi_sol = gauss_seidel(A,b)
            sol = la.solve(A,b)
            return 5*self._eqTest(s.gauss_seidel(A,b), sol, "gauss_seidel() failed")

        points = (_test(5) + _test(10) + _test(50) + _test(100)) / 4.
        return int(points * self._checkCode(s.gauss_seidel, "solve("))

    @_autoclose
    def problem4(self, s):
        """Test prob4(). 10 points."""
        s.prob4()
        print("""\nSpecifications:
        1. Two lines: Gauss-Seidel, and la.solve(), Gauss should surpass la.solve further down
        2. All lines are quadratically increasing (at different rates)
        3. A legend with good labels is included
        (Titles unnecessary)
        (NumPy lines may be bumpy in the log-log plot)""")
        return self._grade(5, "prob4() does not match specifications")

    def problem5(self, s):
        """Test sparse_gauss_seidel(). 5 points."""
        points = 0

        @_timeout(2)
        def _test(n):
            results = []
            A = diag_dom(n)
            b = np.random.rand(n)
            #s.jacobi_sol = sparse_gauss_seidel(sparse.csr(A),b)
            sol = la.solve(A,b)
            return 5*self._eqTest(s.sparse_gauss_seidel(sparse.csr_matrix(A),b), sol, "sparse_gauss_seidel() failed")

        points = (_test(5) + _test(10) + _test(50) + _test(100)) / 4.
        return int(points * self._checkCode(s.sparse_gauss_seidel, "solve("))

    def problem6(self, s):
        """Test sparse_sor(). 5 points."""
        points = 0

        @_timeout(2)
        def _test(n):
            results = []
            A = diag_dom(n)
            b = np.random.rand(n)
            #s.jacobi_sol = sparse_sor(sparse.csr(A),b,0.8,maxiters=300)
            sol = la.solve(A,b)
            return 5*self._eqTest(s.sparse_sor(sparse.csr_matrix(A),b,0.8,maxiters=300), sol, "sparse_sor() failed")

        points = (_test(5) + _test(10) + _test(50) + _test(100)) / 4.
        return int(points * self._checkCode(sparse_sor, "solve("))

    def problem7(self, s):
        """Test finite_difference(). 5 points."""
        points = 0
        #print finite_difference(20)[0]
        A1, b1 = finite_difference(20)
        A2, b2 = s.finite_difference(20)

        if np.allclose(b1,b2):
            points +=5
        else:
            comment = "b not returned correctly" + "\n" + "Student: \n" + str(b2) + "\n\nExpected: \n" + str(b1)
            self.feedback += "\n{}".format(comment)

        return points

    @_autoclose
    def problem8(self, s):
        """Test prob8(). 5 points."""

        print("Running prob8()...(30 second time limit)")
        _timeout(90)(s.compare_omega)()
        # print("""\nSpecifications: # TODO
        # """)
        return self._grade(5, "prob8() does not match specifications")

    @_autoclose
    def problem9(self, s):
        """Test prob4(). 5 points."""

        print("Running prob9()...(30 second time limit)")
        _timeout(30)(s.hot_plate)(150)
        # print("""\nSpecifications: # TODO
        # """)
        return self._grade(5, "prob9() does not match specifications")

# Main Routine ================================================================

def test(student_module, total=45):
    """Grade a student's entire solutions file.

    5 points for problem 1
    5 points for problem 2
    5 points for problem 3
    5 points for problem 4
    5 points for problem 5
    5 points for problem 6
    5 points for problem 7
    5 points for problem 8
    5 points for problem 9

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
