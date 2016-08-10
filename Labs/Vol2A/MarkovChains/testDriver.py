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
from solutions import analyze_simulation, SentenceGenerator

def test(student_module):
    """Grade a student's entire solutions file.
    
    5  points for problem 1
    15 points for problems 2-4
    20 points for problems 5-6
    
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
        test_one(self.problem1, "Problem 1",     5)
        test_one(self.problem4, "Problems 2-4", 15)
        test_one(self.problem6, "Problems 5-6", 20)

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
    @_timeout(5)
    def problem1(self, s):
        """Test random_markov(). 5 points."""
        def test_chain(m):
            for column in m.T:
                if not np.allclose(column.sum(), 1.):
                    self.feedback += "\nInvalid Markov chain."
                    self.feedback += "\n\tColumn doesn't sum to one:\n\t"
                    self.feedback += str(column)
                    print column.sum()
                    return 0
            return 1
        points  =   test_chain(s.random_markov(  3))
        points += 2*test_chain(s.random_markov( 10))
        points += 2*test_chain(s.random_markov(100))
        return points

    def problem4(self, s):
        """Test forecast(), four-state-forecast(), and analyze_simulation().
        15 points.
        """
        # forecast(): 2 points.
        try:
            s.forecast(10)
        except TypeError:
            raise NotImplementedError("Problem 2 Incomplete")

        points  = 2*self._eqTest(10, len(s.forecast(10)),
                                "forecast(n) should return a list of length n")

        # four-state-forecast(): 3 points.
        points += 3*self._eqTest(20, len(s.four_state_forecast(20)),
                     "four_state_forecast(n) should return a list of length n")


        # analyze_simulation(): 10 points.
        print("Correct output:")
        analyze_simulation()

        print("\nStudent output:")
        x = s.analyze_simulation()
        if x is not None:
            print(x)

        points += self._grade(10)

        return points

    def problem6(self, s):
        """Test the SentenceGenerator class. 20 points."""

        def test_sentences(filename, num_sentences):

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

        points  = test_sentences("markov_test1.txt", 2)
        points += test_sentences("markov_test2.txt", 3)
        points += test_sentences("markov_test3.txt", 5)
        points += test_sentences("markov_test4.txt", 5)

        return points

# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    test(solutions)
