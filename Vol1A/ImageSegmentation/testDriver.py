# testDriver.py
"""Vol1A: Image Segmentation. Test Driver"""

# Decorators ==================================================================

import signal
from functools import wraps
from matplotlib import pyplot as plt

def _autoclose(func):
    """Decorator for closing figures automatically."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            plt.ion()
            return func(*args, **kwargs)
        finally:
            plt.close('all')
            plt.ioff()
    return wrapper

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
        message = "Timeout after {} seconds".format(seconds)
        print(message)
        raise TimeoutError(message)


    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handler)
            signal.alarm(seconds)               # Set the alarm.
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)                 # Turn the alarm off.
        return wrapper
    return decorator

# Test Driver =================================================================

from inspect import getsourcelines
import numpy as np
from scipy import sparse
from scipy.linalg import lu_factor, solve
from inspect import getsourcelines
from solutions import *
# from solutions import [functions / classes that are needed for testing]

def test(student_module):
    """Grade a student's entire solutions file.

        X points for problem 1
        X points for problem 2
        ...

        Inputs:
        student_module: the imported module for the student's file.

        Returns:
        score (int): the student's score, out of TOTAL.
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
        test_one(self.problem1, "Problem 1", 10)   # Problem 1: X points.
        test_one(self.problem2, "Problem 2", 10)   # Problem 2: X points.
        test_one(self.problem3, "Problem 3", 10)   # Problem 1: X points.
        test_one(self.problem4, "Problem 4", 10)   # Problem 1: X points.


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

    def _eqTest(self, correct, student, message, compare=True):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if np.allclose(correct, student):
            return 1
        else:
            self.feedback += "\n{}".format(message)
            if compare:
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

    def problem1(self, s):
        """Test Problem 1. 10 points."""
        @_timeout(2)
        def test():
            points = 0
            A1 = np.array([[0,1,0,0,1,1], [1,0,1,0,1,0], [0,1,0,1,0,0], [0,0,1,0,1,1], [1,1,0,1,0,0], [1,0,0,1,0,0]])
            A2 = np.array([[0,3,0,0,0,0], [3,0,0,0,0,0], [0,0,0,1,0,0], [0,0,1,0,2,.5], [0,0,0,2,0,1], [0,0,0,.5,1,0]])

            points += 5*self._eqTest(laplacian(A1), s.laplacian(A1), 'Laplacian function incorrect for 9.1')
            points += 5*self._eqTest(laplacian(A2), s.laplacian(A2), 'Laplacian function incorrect for 9.2')

            return points

        return int(test())

    def problem2(self, s):
        """Test Problem 2. 10 points."""
        points = 0
        @_timeout(2)
        def test():
            A1 = np.array([[0,1,0,0,1,1], [1,0,1,0,1,0], [0,1,0,1,0,0], [0,0,1,0,1,1], [1,1,0,1,0,0], [1,0,0,1,0,0]])
            A2 = np.array([[0,3,0,0,0,0], [3,0,0,0,0,0], [0,0,0,1,0,0], [0,0,1,0,2,.5], [0,0,0,2,0,1], [0,0,0,.5,1,0]])
            points = 0
            points += 5*self._eqTest(n_components(A1), s.n_components(A1), 'n_components function incorrect for 9.1')
            points += 5*self._eqTest(n_components(A2), s.n_components(A2), 'n_components function incorrect for 9.2')

            return points
        return int(test())

    def problem3(self, s):
        """Test Problem 3. 10 points."""
        @_timeout(5)
        def test():
            points = 0
            radius, sigma_I, sigma_d = 5.0, .02, 3.0
            filename = "dream.png"

            W, D = adjacency(filename, radius, sigma_I, sigma_d)

            Wstu, Dstu = s.adjacency(filename, radius, sigma_I, sigma_d)

            points += 5*self._eqTest(W.shape, Wstu.shape, 'Weighted adjacency matrix incorrect')
            points += 5*self._eqTest(D, Dstu, 'Main diagonal of the degree matrix incorrect')

            return points

        return int(test())

    def problem4(self, s):
        """Test Problem 4. 10 points."""
        points = 0
        @_timeout(5)
        def test():
            points = 0
            filename = "dream.png"

            pos, neg = segment(filename)
            posStu, negStu = s.segment(filename)

            points += 5*self._eqTest(pos, posStu, 'Positive of image incorrect')
            points += 5*self._eqTest(neg, negStu, 'Negative of image incorrect')

            return points
        # Test problem 2 here.
        return int(test())


# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    # If you really like using IPython for validation, include these lines:
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    # reload(solutions)
    test(solutions)
