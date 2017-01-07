# test_driver.py
"""Volume 2B: Optimization with SciPy. Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout, _autoclose

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
        self.total = 40
        self.problems = [   (self.problem1, "Problem 1",  5),
                            (self.problem2, "Problem 2",  5),
                            (self.problem3, "Problem 3", 10),
                            (self.problem4, "Problem 4", 10),
                            (self.problem5, "Problem 5", 10)    ]

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

        10 points for problem 1
        10 points for problem 2
        10 points for problem 3
        10 points for problem 4

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test prob1(). 5 points."""

        print("Correct Response:{}".format(' -'*10))
        prob1()
        print("\nStudent Response:{}".format(' -'*10))
        s.prob1()

        return self._grade(5, "prob1() incorrect")

    @_autoclose
    def problem2(self, s):
        """Test prob2(). 5 points."""
        s.prob2()
        print("""\nSpecifications:
            1. One line is jagged (the initial guess)           (2 points)
            3. The other line is straight (the minimizer)       (3 points)
            """)
        return self._grade(5, "prob2() incorrect")

    @_autoclose
    def problem3(self, s):
        """Test prob3() (basin hopping). 10 points."""

        print("\nCorrect Response:")
        print(".2 is too small a stepsize to escape the basin of a local min.")
        print("\nStudent Response:{}\n".format(' -'*10))
        points = 3*self._eqTest(prob3(grading=True), s.prob3(),
                                        "Incorrect minimum function value.")
        points += self._grade(2, "Incorrect reason why stepsize=0.2 fails")
        print("""\nSpecifications:
            1. 3-d wireframe plot
            2. Two different minima
            """)
        points += self._grade(5, "Incorrect plot")

        return points

    @_timeout(2)
    def problem4(self, s):
        """Test Problem 3. 10 points."""

        def f(X):
            """The nonlinear system described in the problem."""
            x,y,z = X
            return np.array([   -x + y + z,
                                1 + x**3 -y**2 + z**3,
                                -2 -x**2 + y**2 + z**2  ])
        ans = s.prob4()
        return 10 * self._eqTest(np.zeros(3), f(ans),
                                "Returned value is not a root of the system"
                                "\n(check by computing f(result), as below)")

    @_autoclose
    def problem5(self, s):
        """Test prob5(). 10 points."""

        points = 5*self._eqTest(prob5(grading=True), s.prob5(),
                                                    "Incorrect fit parameters")
        print("""\nSpecifications:
              1. Data and curve plotted together            (2 points)
              2. Curve matches data, especially toward
                    the right end of the domain.            (3 points)
              """)
        points += self._grade(5, "Incorrect plot")
        return points

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
