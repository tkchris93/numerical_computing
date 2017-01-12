# test_driver.py
"""Volume 2 Lab 16: Simplex. Test Driver."""

import sys
sys.path.insert(1, "../..")
from base_test_driver import BaseTestDriver, _timeout

import numpy as np
from solutions import SimplexSolver, prob7


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

    30 points for the Simplex Solver (example problem)
    10 points for problem 7: Product Mix.

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.total = 40
        self.problems = [   (self.problem6, '1-6', 30),
                            (self.problem7, '7',   10)  ]

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

        30 points for the Simplex Solver (example problem)
        10 points for problem 7: Product Mix.

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Helper functions --------------------------------------------------------
    def _dicTest(self, correct, student):
        """Test to see if the dictionaries 'correct' and 'student' have the
        same string representation. Report the given 'message' if they are not.
        """
        assert isinstance(correct, dict), "Expected a dictionary"
        if not isinstance(student, dict):
            self.feedback += "\nExpected a dictionary"
            return 0

        points = 0
        success = True
        for key in correct:
            if key in student:
                points += 1
                if correct[key] == student[key]:
                    points += 1
                else:
                    success = False
            else:
                success = False
        if not success:
            self.feedback += "\n{}".format("Incorrect Dictionary")
            self.feedback += "\n\tCorrect response: {}".format(correct)
            self.feedback += "\n\tStudent response: {}".format(student)
        return points

    # Problems ----------------------------------------------------------------
    def test_simplex(self, s, c, b, A, simple=False):
        """Test the student's SimplexSolver class on the linear program
                maximize    c^t x
                subject to  Ax <= b
        If simple=True, the amount of points earned is 15. If simple=False,
        the amount of points earned is
            15 + number of basic variables + number of nonbasic variables
        """
        points = 0
        key = SimplexSolver(c, A, b)
        student = s.SimplexSolver(c, A, b)
        sol1, sol2 = key.solve(), student.solve()

        # Test the primal objective.
        points += 15 * self._eqTest(sol1[0], sol2[0],
                                            "Incorrect primal objective")
        if simple is False:
            # Test the basic and nonbasic variable dictionaries.
            points += self._dicTest(sol1[1], sol2[1])
            points += self._dicTest(sol1[2], sol2[2])

        return points

    @_timeout(3)
    def problem6(self, s):
        """Test the SimplexSolver class. 30 points."""
        points = 0

        # Test SimplexSolver on a system that is infeasible at the origin.
        c = np.array([3., 2.])
        b = np.array([2., 5., -7.])
        A = np.array([[1., -1.],
                      [3.,  1.],
                      [4.,  3.]])
        try:
            self.test_simplex(s, c, b, A, simple=True)
        except ValueError as e:
            points += 5
        else:
            self.feedback += "\nExpected ValueError for infeasible system"

        # Test SimplexSolver on a valid, closed system.
        b = np.array([2., 5., 7.])
        points += self.test_simplex(s, c, b, A, simple=False)

        return points

    @_timeout(3)
    def problem7(self, s):
        """Test prob7(). 10 points."""

        sol1, sol2 = prob7(), s.prob7()
        c = np.load('productMix.npz')['p']
        sol1, sol2 = c.dot(sol1), c.dot(sol2)

        # primal = 7453.59649123
        # assert np.allclose(sol1, primal)

        return 10 * self._eqTest(sol1, sol2, "Incorrect maximizer")

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
