# test_driver.py
"""Volume 1B: Monte Carlo 1 (Integration). Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout, _autoclose

import numpy as np
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
                            # (self.problem2, "Problem 2", 10),
                            (self.problem3, "Problem 3", 15),
                            (self.problem4, "Problem 4",  5)    ]

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
        """Test Problem 1. 10 points."""
        print "Volume should be approximately 4.189"
        print "With 10^5 points:", s.prob1()
        print "With 10^2 points:", s.prob1(100)
        return self._grade(10)

    def problem3(self, s):

        # TODO: Split this into the 1-d and n-d cases.

        f1 = lambda x: 0.5*x**2
        f2 = lambda x: np.exp(-0.5*np.dot(x,x))/((2*np.pi)**(0.5*x.size))
        f3 = lambda x: np.cos(x[0]*x[1]) + np.sin(x[2]*x[3])

        min1 = np.array([0.])
        min2 = np.array([-2.,-2.])
        min3 = np.array([-np.pi/2,0.]*2)

        max1 = np.array([0.5])
        max2 = np.array([2.,2.])
        max3 = np.array([0,np.pi/2]*2)

        msg1 = "Incorrect result on a function with input dimension 1."
        msg2 = "Incorrect result integrating the multivariate normal distribution."
        msg3 = "Incorrect result on a function with input dimension 4."

        funcs = [f1, f2, f3]
        mins = [min1, min2, min3]
        maxs = [max1, max2, max3]
        msgs = [msg1, msg2, msg3]

        points = 0
        for i in xrange(3):
            val = mc_int(funcs[i], mins[i], maxs[i])
            s_val = s.mc_int(funcs[i], mins[i], maxs[i])
            print val, s_val
            rel_error = np.abs(val - s_val)/val
            if rel_error > 0.1:
                self.feedback += "\n%s"%msgs[i]
            else:
                points += 5

        return points

    def problem4(self, s):
        """Test prob4(). 5 points."""
        # TODO: lower the error tolerance, like in problem3()?
        return 5 * self._eqTest(prob4(), s.prob4(), "prob4() incorrect", False)

    @_autoclose
    def problem5(self, s):
        """Test prob5(). 5 points."""
        s.prob5()
        return self._grade(5)

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
