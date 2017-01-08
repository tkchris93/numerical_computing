# test_driver.py
"""Volume 2A: Markov Chains. Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout

import numpy as np
from os import remove as rm
from solutions import SentenceGenerator


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for random_chain()
     5 points for forecast()
     5 points for four_state_forecast()
    10 points for steady_state()
    15 points for the SentenceGenerator class.

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
                            (self.problem3, "Problem 3",  5),
                            (self.problem4, "Problem 4", 10),
                            (self.problem6, "SentenceGenerator", 15)    ]

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

         5 points for random_chain()
         5 points for forecast()
         5 points for four_state_forecast()
        10 points for steady_state()
        15 points for the SentenceGenerator class.

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def random_chain(n):
        A = np.random.random((n,n))
        return A / A.sum(axis=0)

    # Problems ----------------------------------------------------------------
    @_timeout(2)
    def problem1(self, s):
        """Test random_chain(). 5 points."""
        def test_chain(m):
            for column in m.T:
                if not np.allclose(column.sum(), 1.):
                    self.feedback += "\nInvalid Markov chain."
                    self.feedback += "\n\tColumn doesn't sum to one:\n\t"
                    self.feedback += str(column)
                    return 0
            return 1
        points  =   test_chain(s.random_chain(  3))
        points += 2*test_chain(s.random_chain( 10))
        points += 2*test_chain(s.random_chain(100))
        return points

    @_timeout(2)
    def problem2(self, s):
        """Test forecast(). 5 points."""
        points = 0

        # Check that forecast() accepts an integer argument.
        try:
            s.forecast(10)
            points += 2
        except TypeError:
            raise NotImplementedError("Problem 2 Incomplete")

        # Check that forecast(n) returns a list of the appropriate length.
        points += 3*self._eqTest(10, len(s.forecast(10)),
                                "forecast(n) should return a list of length n")
        return points

    @_timeout(2)
    def problem3(self, s):
        """Test four_state_forecast(). 5 points."""
        def _test_one(n):
            """Check that four_state_forecast returns a list of length n."""
            return self._eqTest(n, len(s.four_state_forecast(n)),
                     "four_state_forecast(n) should return a list of length n")

        return _test_one(5) + 2*_test_one(10) + 2*_test_one(100)

    @_timeout(2)
    def problem4(self, s):
        """Test steady_state(). 10 points."""

        # Test that Ax = x.
        def _test_one(n):
            """Check that steady_state() actually returns a steady state."""
            A = self.random_chain(n)
            x = s.steady_state(A, tol=1e-8, N=50)
            return self._eqTest(A.dot(x), x, "Ax != x")

        points = 2*_test_one(100) + 3*_test_one(50) + 3*_test_one(20)

        # Provide a matrix that won't converge.
        A = np.array([[0,0,1],[0,1,0],[1,0,0]])
        try:
            s.steady_state(A, tol=1e-14, N=50)
        except ValueError:
            points += 2
        except Exception as e:
            self.feedback += "\nExpected a ValueError for A =\n{}".format(A)
            self.feedback += "\n\t(got {} instead)".format(self._errType(e))
        else:
            self.feedback += "\nValueError not raised for A =\n{}".format(A)

        return points

    def problem6(self, s):
        """Test the SentenceGenerator class. 15 points."""

        with open("__test1__.txt", 'w') as f:
            f.write("a b c d e f g h i j k l m n o p q r s t u v w x y z")
        with open("__test2__.txt", 'w') as f:
            f.write("I am Sam Sam I am.\n"
                    "Do you like green eggs and ham?\n"
                    "I do not like them, Sam I am.\n"
                    "I do not like green eggs and ham.")
        with open("__test3__.txt", 'w') as f:
            f.write("Love is patient Love is kind\n"
                    "It does not envy It does not boast\n"
                    "It is not proud It is not rude\n"
                    "It is not self-seeking It is not easily angered\n"
                    "It keeps no record of wrongs\n"
                    "Love does not delight in evil\n"
                    "but rejoices with the truth\n"
                    "It always protects always trusts\n"
                    "always hopes always perseveres\n"
                    "Love never fails")

        def test_sentences(filename, num_sentences):

            filename = "__{}__.txt".format(filename)
            print("\n{}\nSource file:".format('-'*80))
            with open(filename, 'r') as training_set:
                print(training_set.read().strip())

            print("\nCorrect example sentence:")
            correct = SentenceGenerator(filename)
            print(correct.babble())

            print("\nStudent sentences:")
            student = s.SentenceGenerator(filename)
            for _ in xrange(num_sentences):
                print(student.babble())

            return self._grade(5)

        points  = test_sentences("test1", 2)
        points += test_sentences("test2", 3)
        points += test_sentences("test3", 5)

        for i in xrange(1,4):
            rm("__test{}__.txt".format(i))

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
