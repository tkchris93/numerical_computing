# testDriver.py
"""Volume II: Markov Chains. Test driver."""

# Wrappers ====================================================================

import signal
from functools import wraps

def _timeout(seconds):
    """Decorator for preventing a function from running for too long.

    Inputs:
        seconds (int): The number of seconds allowed.

    Notes:
        This decorator uses signal.SIGALRM, which is only available on Unix.
    """
    assert isinstance(seconds, int), "@timeout(sec) requires an int"

    class TimeoutError(Exception):
        pass

    def _handler(signum, frame):
        """Handle the alarm by raising a custom exception."""
        raise TimeoutError("Timeout after {0} seconds".format(seconds))

    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handler)
            signal.alarm(seconds)               # Set the alarm.
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)                 # Turn the alarm off.
            return result
        return wraps(func)(wrapper)
    return decorator

# Test Script and Class =======================================================

import numpy as np
from os import remove as rm
from solutions import SentenceGenerator

def test(student_module):
    """Grade a student's entire solutions file.

     5 points for random_chain()
     5 points for forecast()
     5 points for four_state_forecast()
    10 points for steady_state()
    15 points for the SentenceGenerator class.

    Inputs:
        student_module: the imported module for the student's file.

    Returns:
        score (int): the student's score, out of 40.
        feedback (str): a printout of test results for the student.
    """

    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

class _testDriver(object):
    """Class for testing a student's work.

    Attributes:
        Score (int)
        Feedback (str)
    """

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine ------------------------------------------------------------
    def test_all(self, student_module, total=40):
        """Grade the provided module on each problem and compile feedback."""
        # Reset feedback and score.
        self.feedback = ""
        self.score = 0

        def test_one(problem, label, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\n{} ({} points):".format(label, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += {}".format(points)
            except BaseException as e:
                self.feedback += "\n{}: {}".format(self._errType(e), e)

        # Grade each problem.
        test_one(self.problem1, "Problem 1",                 5)
        test_one(self.problem2, "Problem 2",                 5)
        test_one(self.problem3, "Problem 3",                 5)
        test_one(self.problem4, "Problem 4",                10)
        test_one(self.problem6, "SentenceGenerator class",  15)

        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: {}/{} = {}%".format(
                                    self.score, total, round(percentage, 2))
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t{}'.format(comments)

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        return str(type(error).__name__)

    @staticmethod
    def random_chain(n):
        A = np.random.random((n,n))
        return A / A.sum(axis=0)

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if np.allclose(correct, student):
            return 1
        else:
            self.feedback += "\n{}".format(message)
            self.feedback += "\n\tCorrect response: {}".format(correct)
            self.feedback += "\n\tStudent response: {}".format(student)
            return 0

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score.
        If full points are not earned, get feedback on the problem.
        """
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of {}: ".format(points)))
            except:
                credit = -1
        if credit != points:
            # Add comments (optionally),
            comments = raw_input("Comments: ")
            if len(comments) > 0:
                self.feedback += "\n{}".format(comments)
            # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n{}".format(message)
        return credit

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
    """Validate the test driver by testing the solutions file."""
    import solutions
    test(solutions)
