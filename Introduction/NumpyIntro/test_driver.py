# test_driver.py
"""Introductory Labs: Intro to NumPy. Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout

from solutions import *


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1
     5 points for problem 2
     5 points for problem 3
     5 points for problem 4
     5 points for problem 5
     5 points for problem 6
    10 points for problem 7

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.problems = [   (self.problem1, "Problem 1",  5),
                            (self.problem2, "Problem 2",  5),
                            (self.problem3, "Problem 3",  5),
                            (self.problem4, "Problem 4",  5),
                            (self.problem5, "Problem 5",  5),
                            (self.problem6, "Problem 6",  5),
                            (self.problem7, "Problem 7", 10)    ]

    # Helper Functions --------------------------------------------------------
    def _addFeedback(self, correct, student, message):
        """Add a message to the feedback, plus a description of the correct
        answer versus the student's answer.
        """
        self.feedback += "\n{}".format(message)
        self.feedback += "\n\tCorrect response:\n{}".format(correct)
        self.feedback += "\n\tStudent response:\n{}".format(student)

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test prob1(). 5 points."""
        points  = 5*self._eqTest(prob1(), s.prob1(), "prob1() failed")
        points *= self._checkCode(s.prob1, "58,")
        return int(points)

    def problem2(self, s):
        """Test prob2(). 5 points."""
        points  = 5*self._eqTest(prob2(), s.prob2(), "prob2() failed")
        points *= self._checkCode(s.prob2, "0,")
        return int(points)

    def problem3(self, s):
        """Test prob3(). 5 points."""

        points = 0
        sol, stu = prob3(), s.prob3()

        # Make sure the data type is np.int64 (2 points)
        if stu.dtype == np.int64:
            points += 1
        else:
            self.feedback += "\nprob3() failed to change array data type"

        # Check for correct matrix multiplication (4 points).
        points += 4*self._eqTest(stu, sol, "prob3() failed")

        # Check code quality.
        points *= self._checkCode(s.prob3, "48,")
        return int(points)

    def problem4(self, s):
        """Test prob4(). 5 points."""

        def test_single(A):
            pts = 0
            out = "prob4(array({})) ".format(A)
            B = A.copy()
            sol, stu = prob4(A.copy()), s.prob4(B)

            # Make sure a copy was made (1 point).
            if stu is not B:
                pts += 1
            else:
                self.feedback += "\n{}failed to copy the array".format(out)

            # Make sure the answer was correct (1 point).
            pts += self._eqTest(sol,stu,"{}failed".format(out))
            return pts

        points  = test_single(np.array([-3,-1,3]))
        points += test_single(np.random.randint(-50,50,10))
        A = np.random.randint(-50,50,10)
        points += self._eqTest(prob4(A),s.prob4(A),
                               "prob4(array({})) failed".format(A))
        return points

    def problem5(self, s):
        """Test prob5(). 5 points."""
        return 5*self._eqTest(prob5(), s.prob5(), "prob5() failed")

    def problem6(self, s):
        """Test prob5(). 5 points."""

        points = 0
        out = "prob6() failed"

        A = np.array([[1,1,0],[0,1,0],[1,1,1]])
        points += self._eqTest(prob6(A.copy()), s.prob6(A.copy()), out)

        A = np.random.random((5,3))
        points += 2*self._eqTest(prob6(A.copy()), s.prob6(A.copy()), out)

        A = np.random.randint(1,9,(2,4))
        points += 2*self._eqTest(prob6(A.copy()), s.prob6(A.copy()), out)

        return points

    def problem7(self, s):
        """Test prob7(). 10 points."""
        points  = 10*self._eqTest(prob7(), s.prob7(), "prob7() failed")
        points *= self._checkCode(s.prob7, "70600674")
        return int(points)

# Main Routine ================================================================

def test(student_module, total=40):
    """Grade a student's entire solutions file.

     5 points for problem 1
     5 points for problem 2
     5 points for problem 3
     5 points for problem 4
     5 points for problem 5
     5 points for problem 6
    10 points for problem 7

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
