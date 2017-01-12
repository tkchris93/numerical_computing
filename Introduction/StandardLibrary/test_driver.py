# test_driver.py
"""Introductory Labs: The Standard Library. Test Driver."""

import sys
sys.path.insert(1, "../..")
from base_test_driver import BaseTestDriver, _timeout

from subprocess import call
from numpy.random import randint
from solutions import prob1, prob2, prob3


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1
    10 points for problem 2
    10 points for problem 3
    15 points for problem 4

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.total = 40
        self.problems = [   (self.problem1, "Problem 1",  5),
                            (self.problem2, "Problem 2", 10),
                            (self.problem3, "Problem 3", 10),
                            (self.problem4, "Problem 4", 15)    ]

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

         5 points for problem 1
        10 points for problem 2
        10 points for problem 3
        15 points for problem 4

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Problems ----------------------------------------------------------------
    @_timeout(5)
    def problem1(self, s):
        """Test prob1() (built-in functions). 5 points."""

        l = list(randint(-50,50,10))
        correct, student = prob1(l), s.prob1(l)
        if student is None:
            raise NotImplementedError("Problem 1 Incomplete")

        points  = 1*self._eqTest(correct[0], student[0], "Incorrect maximum")
        points += 2*self._eqTest(correct[1], student[1], "Incorrect minimum")
        points += 2*self._eqTest(correct[2], student[2], "Incorrect average")

        return points

    def problem2(self, s):
        """Test prob2() (mutable vs. immutable objects). 10 points."""

        print("\nCorrect output:");   prob2()
        print("\nStudent output:"); s.prob2()
        return self._grade(10, "Incorrect response(s)"
                     "\n(Hint: 3 are immutable and 2 are mutable)")

    @_timeout(5)
    def problem3(self, s):
        """Test prob3() (make and use the calculator module). 10 points."""

        points  = 5*self._eqTest(prob3(5,12), s.prob3(5,12),
                                "Incorrect hypotenuse length")
        a, b = randint(1,50,2)
        points += 5*self._eqTest(prob3(a,b), s.prob3(a,b),
                                "Incorrect hypotenuse length")
        return points

    def problem4(self, s):
        """Test prob4() (using another module). 15 points."""

        # TODO: Automate this problem a little in the same way that
        # the Exceptions lab automates arithmagic() with stdin.

        print("\n------- Testing Problem 4: Play 'Shut the Box' twice -------")
        call(["python", s.__file__, "TA"])
        call(["python", s.__file__])
        return self._grade(15, "'Shut the box' does not match specifications")

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
