# test_driver_template.py
"""For new test drivers, copy the following template class.

Test driver files should be named test_driver.py and placed in the folder with
the corresponding solutions file. See base_test_driver.py for more information.
"""

# import sys
# sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver #, _timeout, _autoclose

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
        self.problems = [   (self.problem1, "Problem 1",  5),
                            (self.problem2, "Problem 2", 35)    ]
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

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        return 0

    def problem2(self, s):
        return 0

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
