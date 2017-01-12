# test_driver.py
"""Volume 1B: Monte Carlo 2 (Importance Sampling). Test Driver."""

import sys
sys.path.insert(1, "../..")
from base_test_driver import BaseTestDriver #, _timeout, _autoclose

from solutions import *


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1
    35 points for problem 2

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.total = 40
        self.problems = [   (self.problem1, "Problem 1", 10),
                            (self.problem2, "Problem 2", 10),
                            (self.problem3, "Problem 3", 10),
                            (self.problem4, "Problem 4", 10)    ]
        # self._feedback_newlines = True

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

         5 points for problem 1
        35 points for problem 2

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Main routine -----------------------------------------------------------
    def problem1(self, s):
        """Test Problem 1. X points."""
        estimate1 = s.prob1(50000)
        estimate2 = s.prob1(5000000)
        print "Problem 1: (should approach 0.0013499 for large n)"
        print "Estimate for n = 50000: {}".format(estimate1)
        print "Estimate for n = 5000000: {}".format(estimate2)
        return self._grade(10)

    @_autoclose
    def problem2(self, s):
        vals = s.prob2()
        x = np.linspace(5000,50000,np.size(vals))
        plt.plot(x,vals)
        plt.title("Estimate for probability of waiting 10 minutes")
        plt.xlabel('# Sample Points')
        plt.ylabel('Probability')
        plt.show()
        print "Final estimate: {} (should approach .00208)".format(vals[-1])

        return self._grade(10)

    @_autoclose
    def problem3(self, s):
        plt.ylim([0,0.0012])
        s.prob3()
        return self._grade(10)

    def problem4(self, s):
        estimate = s.prob4()
        print "Estimate for problem 4: {}".format(estimate)
        return self._grade(10)

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
