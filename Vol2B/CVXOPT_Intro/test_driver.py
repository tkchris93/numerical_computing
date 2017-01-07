# test_driver.py
"""Volume 2B: Intro to CVXOPT. Solutions File."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver

# Get problems, NumPy, and CVXOPT
from solutions import *
solvers.options["show_progress"] = False



class TestDriver(BaseTestDriver):
    """Class for testing a student's work.


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
                            (self.problem6, "Problem 6", 15)    ]

    # Helper functions --------------------------------------------------------
    @staticmethod
    def _test_case(m,n):
        """Generate random matrices for l1Min and l2Min."""
        A = np.random.random((m,n)) * 5
        b = np.random.random(m) * 5
        return A, b

    def _test_opt_tuple(self, correct, student):
        """Test a 5-point problem with solutions 'correct' and submission
        'student', both of which are a tuple: (optimizer, optimal value).
        """
        ans_1, ans_2 = correct

        # Attempt to unpack the student's solutions values.
        try:
            stu_1, stu_2 = student
        except (TypeError, ValueError) as e:
            e.message = "failed to return 2 values"
            raise e

        points  = 3*self._eqTest(ans_1, stu_1, "Incorrect optimizer")
        points += 2*self._eqTest(ans_2, stu_2, "Incorrect optimial value")
        return points

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test prob1(). 5 points."""
        return self._test_opt_tuple(prob1(), s.prob1())

    def problem2(self, s):
        """Test l1Min(). 5 points."""
        def _test(m, n):
            A,b = self._test_case(m, n)
            points = self._test_opt_tuple(l1Min(A,b), s.l1Min(A,b))
            if points != 5:
                self.feedback += "\n\tFor A =\n{},\n\nb =\n{}\n".format(A,b)
            return points

        return (2*_test(5, 5) + 3*_test(5,10)) // 5

    def problem3(self, s):
        """Test prob3(). 5 points."""
        return self._test_opt_tuple(prob3(), s.prob3())

    def problem4(self, s):
        """Test prob4(). 5 points."""
        return self._test_opt_tuple(prob4(), s.prob4())

    def problem5(self, s):
        """Test l2Min(). 5 points."""
        def _test(m, n):
            A,b = self._test_case(m, n)
            points = self._test_opt_tuple(l2Min(A,b), s.l2Min(A,b))
            if points != 5:
                self.feedback += "\n\tA =\n{},\n\n\tb =\n{}\n".format(A,b)
            return points

        return (2*_test(5, 5) + 3*_test(5,10)) // 5

    def problem6(self, s):
        """Test prob6(). 15 points."""
        return 3 * self._test_opt_tuple(prob6(), s.prob6())

# Main Routine ================================================================

def test(student_module, total=40):
    """Grade a student's entire solutions file.


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

