# test_driver.py
"""Vol1A: Image Segmentation. Test driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout

import numpy as np
from solutions import *


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

    10 points for problem 1
    10 points for problem 2
    10 points for problem 3
    10 points for problem 4

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        # self._feedback_newlines = True
        self.problems = [   (self.problem1, "Problem 1", 10),
                            (self.problem2, "Problem 2", 10),
                            (self.problem3, "Problem 3", 10),
                            (self.problem4, "Problem 4", 10)    ]

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test laplacian(). 10 points."""
        @_timeout(2)
        def test():
            points = 0
            A1 = np.array([[0,1,0,0,1,1], [1,0,1,0,1,0], [0,1,0,1,0,0], [0,0,1,0,1,1], [1,1,0,1,0,0], [1,0,0,1,0,0]])
            A2 = np.array([[0,3,0,0,0,0], [3,0,0,0,0,0], [0,0,0,1,0,0], [0,0,1,0,2,.5], [0,0,0,2,0,1], [0,0,0,.5,1,0]])

            points += 5*self._eqTest(laplacian(A1), s.laplacian(A1), 'Laplacian function incorrect for 9.1')
            points += 5*self._eqTest(laplacian(A2), s.laplacian(A2), 'Laplacian function incorrect for 9.2')

            return points

        return int(test())

    def problem2(self, s):
        """Test n_components(). 10 points."""
        points = 0
        @_timeout(2)
        def test():
            A1 = np.array([[0,1,0,0,1,1], [1,0,1,0,1,0], [0,1,0,1,0,0], [0,0,1,0,1,1], [1,1,0,1,0,0], [1,0,0,1,0,0]])
            A2 = np.array([[0,3,0,0,0,0], [3,0,0,0,0,0], [0,0,0,1,0,0], [0,0,1,0,2,.5], [0,0,0,2,0,1], [0,0,0,.5,1,0]])
            points = 0
            points += 5*self._eqTest(n_components(A1), s.n_components(A1), 'n_components function incorrect for 9.1')
            points += 5*self._eqTest(n_components(A2), s.n_components(A2), 'n_components function incorrect for 9.2')

            return points
        return int(test())

    def problem3(self, s):
        """Test adjacency(). 10 points."""
        @_timeout(5)
        def test():
            points = 0
            radius, sigma_I, sigma_d = 5.0, .02, 3.0
            filename = "dream.png"

            W, D = adjacency(filename, radius, sigma_I, sigma_d)

            Wstu, Dstu = s.adjacency(filename, radius, sigma_I, sigma_d)

            points += 5*self._eqTest(W.shape, Wstu.shape, 'Weighted adjacency matrix incorrect')
            points += 5*self._eqTest(D, Dstu, 'Main diagonal of the degree matrix incorrect')

            return points

        return int(test())

    def problem4(self, s):
        """Test segment(). 10 points."""
        points = 0
        @_timeout(5)
        def test():
            points = 0
            filename = "dream.png"

            pos, neg = segment(filename)
            posStu, negStu = s.segment(filename)

            points += 5*self._eqTest(pos, posStu, 'Positive of image incorrect')
            points += 5*self._eqTest(neg, negStu, 'Negative of image incorrect')

            return points
        return int(test())


# Main Routine ================================================================

def test(student_module, total=40):
    """Grade a student's entire solutions file.

    10 points for problem 1
    10 points for problem 2
    10 points for problem 3
    10 points for problem 4

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
