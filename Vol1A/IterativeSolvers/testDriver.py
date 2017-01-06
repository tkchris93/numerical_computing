# testDriver.py
"""Volume 1A: Iterative Methods. Test driver"""

# Decorators ==================================================================

import signal
from functools import wraps
from matplotlib import pyplot as plt
from scipy import sparse

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
    def test_all(self, student_module, total=45):
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
        test_one(self.problem1, "Problem 1", 5)   # Problem 1: 5 points.
        test_one(self.problem2, "Problem 2", 5)   # Problem 2:  5 points.
        test_one(self.problem3, "Problem 3", 5)   # Problem 3:  5 points.
        test_one(self.problem4, "Problem 4", 5)   # Problem 4: 5 points.
        test_one(self.problem5, "Problem 5", 5)   # Problem 5: 5 points.
        test_one(self.problem6, "Problem 6", 5)   # Problem 6: 5 points.
        test_one(self.problem7, "Problem 7", 5)   # Problem 7: 5 points.
        test_one(self.problem8, "Problem 8", 5)   # Problem 8: 5 points.
        test_one(self.problem9, "Problem 9", 5)   # Problem 9: 5 points.


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
    def _printCode(f):
        """Print a function's source code."""
        print "".join(getsourcelines(f)[0][len(f.__doc__.splitlines())+1 :])

    def _checkCode(self, func, keyword):
        """Check a function's source code for a key word. If the word is found,
        print the code to the screen and prompt the grader to check the code.
        Use this function to detect cheating. Returns a score out of 10.
        """
        code = getsourcelines(func)[0][len(func.__doc__.splitlines())+1 :]
        if any([keyword in line for line in code]):
            print("\nStudent {}() code:\n{}\nCheating? [OK=10, Bad=0]".format(
                                                func.__name__, "".join(code)))
            return self._grade(10)
        return 10

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        # if np.allclose(correct, student):
        # if str(correct) == str(student):
        # if correct is student:            # etc.
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
    def problem1(self, s):
        """Test Problem 1. 5 points."""

        @_timeout(2)
        def _test(n):

            points = 0
            A = diag_dom(n)
            b = np.random.rand(n)
            #s.jacobi_sol = jacobi_method(A,b)
            #sol = la.solve(A,b)


            #return 5*self._eqTest((sol), (s.jacobi_sol), "jacobi_method() failed")
            points += 3*self._eqTest(np.round(la.solve(A,b)[0],4), np.round(s.jacobi_method(A,b)[0],4), "jacobi_method() failed")
            points += 2*self._eqTest(np.round(la.solve(A,b)[1],3), np.round(s.jacobi_method(A,b)[1],3), "jacobi_method() failed")

            return points


        points = _test(5) + _test(10) + _test(50) + _test(100)

        return int(points * self._checkCode(s.jacobi_method, "solve(") / 40.)


    @_autoclose
    def problem2(self, s):
        """Test prob2(). 5 points."""
        A = np.array([[2,0,-1],[-1,3,2],[0,1,3]])
        b = np.array([3,3,-1])
        (s.jacobi_method(A,b,plot=True))
        (s.gauss_seidel(A,b,plot=True))

        print("""\nSpecifications:
        1. Plots Absolute error of Approximation versus number of iterations.              (1 point)
        2. Two lines, clearly marked:                               (2 points)
            - Guass (faster)
            - Jacobi Method (slower)
        3. The difference between each line is apparent.            (2 points)
        (Plot could be loglog or linlin as long as it is clear)
        (Title and axis labels unnecessary)""")
        return self._grade(5, "prob2() does not match specifications")

    def problem3(self, s):
        """Test Problem 3. X points."""
        points = 0

        @_timeout(2)
        def _test(n):
            results = []
            A = diag_dom(n)
            b = np.random.rand(n)
            s.jacobi_sol = gauss_seidel(A,b)
            sol = la.solve(A,b)
            return 5*self._eqTest(s.gauss_seidel(A,b), sol, "gauss_seidel() failed")

        points = _test(5) + _test(10) + _test(50) + _test(100)
        return int(points * self._checkCode(s.gauss_seidel, "solve(") / 40.)

    @_autoclose
    def problem4(self, s):
        """Test prob4(). 10 points."""
        (s.prob4)()
        print("""\nSpecifications:
        1. Two lines: Gauss-Seidel, and la.solve(), Gauss should surpass la.solve further down
        2. All lines are quadratically increasing (at different rates)
        3. A legend with good labels is included
        (Titles unnecessary)
        (NumPy lines may be bumpy in the log-log plot)""")
        return self._grade(5, "prob4() does not match specifications")

    def problem5(self, s):
        """Test Problem 5. X points."""
        points = 0

        @_timeout(2)
        def _test(n):
            results = []
            A = diag_dom(n)
            b = np.random.rand(n)
            #s.jacobi_sol = sparse_gauss_seidel(sparse.csr(A),b)
            sol = la.solve(A,b)
            return 5*self._eqTest(s.sparse_gauss_seidel(sparse.csr_matrix(A),b), sol, "sparse_gauss_seidel() failed")

        points = _test(5) + _test(10) + _test(50) + _test(100)
        return int(points * self._checkCode(s.sparse_gauss_seidel, "solve(") / 40.)

    def problem6(self, s):
        """Test Problem 5. X points."""
        points = 0

        @_timeout(2)
        def _test(n):
            results = []
            A = diag_dom(n)
            b = np.random.rand(n)
            #s.jacobi_sol = sparse_sor(sparse.csr(A),b,0.8,maxiters=300)
            sol = la.solve(A,b)
            return 5*self._eqTest(s.sparse_sor(sparse.csr_matrix(A),b,0.8,maxiters=300), sol, "sparse_sor() failed")

        points = _test(5) + _test(10) + _test(50) + _test(100)
        return int(points * self._checkCode(sparse_sor, "solve(") / 40.)

    def problem7(self, s):
        """Test Problem 5. X points."""
        points = 0
        #print finite_difference(20)[0]
        A1, b1 = finite_difference(20)
        A2, b2 = s.finite_difference(20)

        if np.allclose(b1,b2):
            points +=5
        else:
            comment = "b not returned correctly" + "\n" + "Student: \n" + str(b2) + "\n\nExpected: \n" + str(b1)
            self.feedback += "\n{}".format(comment)

        return points

    @_autoclose
    def problem8(self, s):
        """Test prob8(). 5 points."""

        print("Running prob8()...(30 second time limit)")
        _timeout(90)
        (s.compare_omega())
        print("""\nSpecifications:
        1. Two lines: Gauss-Seidel, and la.solve(), Gauss should surpass la.solve further down
        2. All lines are quadratically increasing (at different rates)
        3. A legend with good labels is included
        (Titles unnecessary)
        (NumPy lines may be bumpy in the log-log plot)""")
        return self._grade(5, "prob4() does not match specifications")

    @_autoclose
    def problem9(self, s):
        """Test prob4(). 5 points."""

        print("Running prob9()...(30 second time limit)")
        _timeout(30)
        s.hot_plate(150)
        print("""\nSpecifications:
        1. Two lines: Gauss-Seidel, and la.solve(), Gauss should surpass la.solve further down
        2. All lines are quadratically increasing (at different rates)
        3. A legend with good labels is included
        (Titles unnecessary)
        (NumPy lines may be bumpy in the log-log plot)""")
        return self._grade(5, "prob4() does not match specifications")

# Validation ==================================================================
if __name__ == '__main__':
    """Validate the test driver by testing the solutions file."""
    import solutions
    # If you really like using IPython for validation, include these lines:
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    # reload(solutions)
    test(solutions)
