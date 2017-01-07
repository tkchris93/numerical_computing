# solutions.py
"""Volume 2B: Optimization with SciPy. Test driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _autoclose

import numpy as np
from scipy import optimize as opt
from matplotlib import pyplot as plt


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
                            (self.problem4, "Problem 4", 10)  ]

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test Problem 1. 10 points."""

        print("Student Response:")
        s.prob1()
        print("""\nCorrect Response:
            The Powell algorithm takes the least number of iterations (19).
            COBYLA fails to find the correct minimum.
            """)

        print("Least number of iterations\t"),
        points = self._grade(5, "Incorrect for which method takes least iters")
        print("The algorithms that fail\t"),
        points += self._grade(5, "Incorrect for which fails to find the min")

        return points

    def problem2(self, s):
        """Test Problem 2. 10 points."""

        points = 5*self._eqTest(prob2(verbose=False), s.prob2(),
                                        "Incorrect minimum function value.")
        print("""\nCorrect Response:
            .2 is too small a stepsize to escape the basin of a local min.
            """)
        points += self._grade(5, "Incorrect reason why stepsize=0.2 fails")

        return points

    def problem3(self, s):
        """Test Problem 3. 10 points."""

        def f(X):
            """The nonlinear system described in the problem."""
            x,y,z = X
            return np.array([   -x + y + z,
                                1 + x**3 -y**2 + z**3,
                                -2 -x**2 + y**2 + z**2  ])
        ans = s.prob3()
        if ans is None:
            self.feedback += "\nFailed to return a value."
            return 0
        return 10*self._eqTest(np.zeros(3), f(ans),
                                "Returned value is not a root of the system"
                                "\n(check by computing f(result), as below)")

    @_autoclose
    def problem4(self, s):
        """Test Problem 4. 10 points."""

        points  = 5*self._eqTest(prob4(display=False), s.prob4(),
                                                    "Incorrect return values")
        points += self._grade(5, "Incorrect figure")
        return points

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
