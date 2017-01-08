# base_test_driver.py
"""Base Class for Foundations of Applied Mathematics lab test drivers.

Test driver files should be named testDriver.py and should be placed in the
same folder as the lab that it corresponds to. The file may have dependencies
on the corresponding solutions.py file so that student submissions are tested
directly against the solutions when possible, but in some cases the test
driver may be independent from the solutions file.

Test driver classes -----------------------------------------------------------

This file includes a base test driver class (BaseTestDriver) that all other
test drivers should inherit from, as it contains methods that are common to
most test drivers. In order for other test driver classes to access the base
class, test driver files must begin with the code

    import sys
    sys.path.insert(0, "../..")
    from base_test_driver import BaseTestDriver, [other imports]

The BaseTestDriver class is designed to be flexible. The test() method grades
each problem and collect feedback, but each problem can be graded individually
via the different problemX() methods. This allows the instructor to grade from
IPython, or to automate grading using Git.

See test_driver_template.py for a template for new drivers. Customize the
docstrings of the test() function and the test driver class to give specific
instructions about how the lab is to be graded.

Decorators --------------------------------------------------------------------

The @_autoclose tag makes it easy to grade a problem that produces a plot.
It should only be on a problem-grading function that uses _testDriver._grade()
or some other pausing command (like raw_input()) so that the plot is not closed
immediately after it is created.

The @_timeout tag prevents a function from running for longer than a
specificied number of seconds. Be careful not to use this wrapper in
conjunction with _testDriver._grade() or another pausing command that waits
for the grader's response. NOTE: this decorator only works on Unix machines.
"""

import signal
import numpy as np
from functools import wraps
from inspect import getsourcelines
from matplotlib import pyplot as plt

# Decorators ==================================================================

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

np.set_printoptions(precision=3, suppress=True)

class BaseTestDriver(object):
    """Base Class for Foundations of Applied Mathematics student test drivers.

    Attributes:
        feedback (str): a feedback string for the student.
        total (int): the possible number of points for the assignment.
        problems (list): a list of tuples (func, label, value) with
            func (function): a function for testing a single problem. Should
                accept as input the imported student module.
            label (str): a label for the problem or code being tested.
            value (int): the amount of points that the problem is worth.
        _debug (bool): If True, exceptions raised by problemX() methods will
            be passed up to the user.
        _feedback_newlines (bool): If False, feedback appears as follows:

            <message>
                Correct Response: <correct>
                Student Response: <student>

            If True, feedback appears as follows:

            <message>
                Correct Response:
            <correct>
                Student Response:
            <student>

            Set to true for lengthy answers, such as NumPy arrays.

    Main Methods:
        __init__(): Initialize all attributes. Must be overwritten by inherited
            test driver classes.
        test_all(student_module, total=40): Test every problem listed in the
            self.problems attribute. This is the only method that needs to be
            accessed externally.
        problemX(student_module): Test problem X, returning the amount of
            points earned and adding to self.feedback (if needed) internally.

    Helper Methods:
        _errType(error): Return the type name of the exception 'error'.
        _printCode(f): Print the source code of the function 'f'.
        _checkCode(func, keyword): Check a function's source code for a key
            word to detect cheating. Return a fraction out of 1.
        _addFeedback(correct, student, message): governs how the next three
            functions format their feedback. Behavior depends on the
            _feedback_newlines attribute.
        _eqTest(correct, student, message): Compare 'correct' and 'student'
            with np.allclose(). If they are the same, return 1. Else, add the
            'message' to the feedback, along with the correct answer versus
            the student answer, and return 0.
        _isTest(correct, student, message): Same as _eqTest(), but comparing
            with the 'is' operator.
        _strTest(correct, student, message): Same as _eqTest(), but comparing
            string representations of the inputs.
        _grade(points, message=None): Prompt the grader for a score out of
            'points'. Add the 'message' to the feedback if full credit is not
            earned.

    Notes:
        This class cannot be instantiated and is meant as a base class to be
        inherited from. Derivative test driver classes must define one
        function per problem or per segment to be tested (see problemX()
        description under 'Methods'). These methods accept the student module
        as an argument and return the points earned. Derivative classes should
        then set the problems attribute so that it includes these methods.

        For example, if the lab has two problems, the first worth 5 points and
        the second worth 35 points, set

        self.problems = [(self.problem1, "Problem 1",  5),
                         (self.problem2, "Problem 2", 35)]

        in the constructor, and define the following methods:

        def problem1(self, s):
            points = 0
            # Test the first problem, out of 5 possible points. For example,
            points += 5 * self._eqTest("correct answer", s.prob1())
            return points

        def problem2(self, s):
            # Test the second problem, out of 35 possible points. For example,
            return self._grade(35, "Problem 2 failed!")
    """

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        self.feedback = ""

        # The number of points possible.
        self.total = NotImplemented

        # Each test driver should initialize self.problems differently.
        # For example, if the lab has two problems, the first worth 5 points
        # and the second worth 15 points, set
        # self.problems = [(self.problem1, "Problem 1",  5),
        #                  (self.problem2, "Problem 2", 15)]
        # where problem1() and problem2() are methods of the test driver
        # that test the corresponding problems.
        self.problems = NotImplemented

        self._debug = False
        self._feedback_newlines = False

    # Main Routines -----------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Derivative classes must implement this function as follows:

        return TestDriver().test_all(student_module)

        """
        raise NotImplementedError("main() not implemented for this class")

    def test_all(self, student_module):
        """Grade the provided module on each problem and compile feedback.

        Inputs:
            student_module (module): the student's imported file.

        Returns:
            score (int): the number of points earned.
            feedback (str): feedback for the student.
        """
        if self.total is NotImplemented:
            raise NotImplementedError("self.total not assigned")
        elif self.problems is NotImplemented:
            raise NotImplementedError("self.problems not assigned")

        # Reset feedback and initialize score.
        self.feedback = ""
        score = 0

        # Grade each problem.
        for problem in self.problems:
            try:
                func, label, value = problem
                self.feedback += "\n\n{} ({} points):".format(label, value)
                points = func(student_module)
                score += points
                self.feedback += "\nScore += {}".format(points)
            except BaseException as e:
                self.feedback += "\n{}: {}".format(self._errType(e), e)
                if self._debug:
                    raise

        # Report final score.
        percentage = (100. * score) / self.total
        self.feedback += "\n\nTotal score: {}/{} = {}%".format(
                                    score, self.total, round(percentage, 2))
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t{}'.format(comments)

        return score, self.feedback

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Return the type name of the exception 'error'."""
        return str(type(error).__name__)

    @staticmethod
    def _printCode(f):
        """Print the source code of the function 'f'."""
        print "".join(getsourcelines(f)[0][len(f.__doc__.splitlines())+1 :])

    def _checkCode(self, func, keyword):
        """Check a function's source code for a key word. If the word is found,
        print the code to the screen and prompt the grader to check the code.
        Use this function to detect cheating. Returns a score out of 1.
        """
        code = getsourcelines(func)[0][len(func.__doc__.splitlines())+1 :]
        if any([keyword in line for line in code]):
            print("\nStudent {}() code:\n{}\nCheating? [OK=10, Bad=0]".format(
                                                func.__name__, "".join(code)))
            return self._grade(10)/10.
        return 1

    def _addFeedback(self, correct, student, message, compare):
        """Add a message to the feedback, plus a description of the correct
        answer versus the student's answer (if compare=True).
        """
        self.feedback += "\n{}".format(message)
        if compare and self._feedback_newlines:
            self.feedback += "\n\tCorrect response:\n{}".format(correct)
            self.feedback += "\n\tStudent response:\n{}".format(student)
        elif compare:
            self.feedback += "\n\tCorrect response: {}".format(correct)
            self.feedback += "\n\tStudent response: {}".format(student)

    def _eqTest(self, correct, student, message, compare=True):
        """Test to see if 'correct' and 'student' have the same value."""
        if student is None:
            raise ValueError("{} (function returned None)".format(message))
        elif np.allclose(correct, student, atol=1e-4):
            return 1
        else:
            self._addFeedback(correct, student, message, compare)
            return 0

    def _isTest(self, correct, student, message, compare=True):
        """Test to see if 'correct' and 'student' are the same object."""
        if correct is student:
            return 1
        else:
            self._addFeedback(correct, student, message, compare)
            return 0

    def _strTest(self, correct, student, message, compare=True):
        """Test to see if 'correct' and 'student' have the same string
        representation.
        """
        if str(correct) == str(student):
            return 1
        else:
            self._addFeedback(correct, student, message, compare)
            return 0

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score.
        If full points are not earned, give feedback on the problem.
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

    # Magic methods -----------------------------------------------------------
    def __str__(self):
        """Current Feedback"""
        return self.feedback if self.feedback else "No Feedback"

    def __repr__(self):
        """List problems, their worth, and the corresponding test functions."""
        out = "{} class.".format(type(self).__name__)
        for problem in self.problems:
                func, label, value = problem
                out += "\n\t{}: {} points. ".format(label, value)
                out += "Test with self.{}().".format(func.__name__)
        if self.feedback:
            out += "\nCurrent Feedback:\n" + self.feedback
        return out

