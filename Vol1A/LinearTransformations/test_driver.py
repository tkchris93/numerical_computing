# test_driver.py
"""Volume 1A: Linear Transformations. Test driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout, _autoclose

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
    data_file = "horse.npy"

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.problems = [   (self.problem1, "Problem 1", 10),
                            (self.problem2, "Problem 2", 10),
                            (self.problem3, "Problem 3", 10),
                            (self.problem4, "Problem 4", 10)    ]

    # Helper Functions --------------------------------------------------------
    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if np.allclose(correct, student):
            return 1
        else:
            self.feedback += "\n{}".format(message)
            return 0

    # Problems ----------------------------------------------------------------
    @_timeout(5)
    def problem1(self, s):
        """Test stretch(), shear(), reflect(), and rotate(). 10 points."""
        points = 0
        data = np.load(self.data_file)

        # stretch() (2 points).
        a, b = np.random.randint(1,11,2)
        points += 2 * self._eqTest(stretch(data, a, b), s.stretch(data, a, b),
                                                            "stretch() failed")

        # shear() (2 points).
        a, b = np.random.randint(1,11,2)
        points += 2 * self._eqTest(shear(data, a, b), s.shear(data, a, b),
                                                            "shear() failed")

        # reflect() (3 points).
        a, b = np.random.randint(1,11,2)
        points += 3 * self._eqTest(reflect(data, a, b), s.reflect(data, a, b),
                                                            "reflect() failed")

        # rotate() (3 points).
        theta = np.random.uniform(.1, 2*np.pi-.1)
        points += 3 * self._eqTest(rotate(data, theta), s.rotate(data, theta),
                                                            "rotate() failed")
        return points

    @_autoclose
    def problem2(self, s):
        """Test solar_system(). 10 points."""

        s.solar_system(np.pi, 1, 13)
        print("""\nSpecifications:
        1. Blue semicircle from 0 to pi
        2. Green line rotates around blue line 6 times
        (Title and legend unnecessary)
        (Aspect ratio may be stretched)""")
        return self._grade(10, "solar_system() does not match specifications")

    @_autoclose
    def problem3(self, s):
        """Test prob3(). 10 points."""

        print("Running prob3()...(60 second time limit)")
        _timeout(60)(s.prob3)()
        print("""\nSpecifications:
        1. Two plots: matrix-vector times, matrix-matrix times
        2. Both plots are quadratically increasing
        3. Matrix-matrix times are much greater than matrix-vector times
        (Titles and legend unnecessary)""")
        return self._grade(10, "prob3() does not match specifications")

    @_autoclose
    def problem4(self, s):
        """Test prob4(). 10 points."""

        print("Running prob4()...(60 second time limit)")
        _timeout(60)(s.prob4)()
        print("""\nSpecifications:
        1. Two plots: lin-lin scale, log-log scale
        2. All lines are quadratically increasing (at different rates)
        3. NumPy times are significantly lower than list times
        4. A legend with good labels is included
        (Titles unnecessary)
        (NumPy lines may be bumpy in the log-log plot)""")
        return self._grade(10, "prob4() does not match specifications")

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
    # To use IPython for validation, include these lines:
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    # reload(solutions)
    test(solutions)
