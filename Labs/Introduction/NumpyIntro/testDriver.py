# solutions.py
"""Introductory Labs: Intro to NumPy. Solutions file."""

# Decorators ==================================================================


from functools import wraps

# Test Driver =================================================================

import numpy as np
from solutions import *

def test(student_module):
    """Test script. Import the student's solutions file as a module.

     5 points for problem 1
     5 points for problem 2
    10 points for problem 3
    10 points for problem 4
    10 points for problem 5

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
    """Class for testing a student's work. See test.__doc__ for more info."""

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine -----------------------------------------------------------
    def test_all(self, student_module, total=40):
        """Grade the provided module on each problem and compile feedback."""
        # Reset feedback and score.
        self.feedback = ""
        self.score = 0

        def test_one(problem, number, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\nProblem %d (%d points):"%(number, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += %d"%points
            except BaseException as e:
                self.feedback += "\n%s: %s"%(self._errType(e),e)

        # Grade each problem.
        test_one(self.problem1, 1, 5)   # Problem 1:  5 points.
        test_one(self.problem2, 2, 5)   # Problem 2:  5 points.
        test_one(self.problem3, 3, 10)  # Problem 3: 10 points.
        test_one(self.problem4, 4, 10)  # Problem 4: 10 points.
        test_one(self.problem5, 5, 10)  # Problem 5: 10 points.


        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: %d/%d = %s%%"%(
                                    self.score, total, percentage)
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t%s'%comments

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        if isinstance(error, BaseException):
            return str(type(error)).lstrip("<type 'exceptions.").rstrip("'>")
        else:
            return str(error)

    def _arrTest(self, correct, student, message):
        """Test to see if the arrays 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if allclose(correct, student):
            return 1
        else:
            self.feedback += "\n\t%s"%message
            self.feedback += "\nCorrect response:\narray(%s)"%correct
            self.feedback += "\nStudent response:\narray(%s)"%student
            return 0

    def _eqTest(self, correct, student, message, tol):
        """Test to see if 'correct' and 'student' are within a tolerance of
        each other. Report the given 'message' if they are not.
        """
        if abs(correct - student) < tol:
            return 1
        else:
            self.feedback += "\n%s"%message
            self.feedback += "\n\tCorrect response: %s"%correct
            self.feedback += "\n\tStudent response: %s"%student
            return 0

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score."""
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of %d: "%points))
            except:
                credit = -1
        if credit != points:
            # Add comments (optionally),
            comments = raw_input("Comments: ")
            if len(comments) > 0:
                self.feedback += "\n\t%s"%comments
            # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n\t%s"%message
        return credit

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test 'product'. 5 points."""
        if not hasattr(s, "product"):
            raise NotImplementedError("Problem 1 Incomplete")
        return 5*self._arrTest(product, s.product, "Incorrect product.")

    def problem2(self, s):
        """Test nonnegative(). 5 points."""
        if not hasattr(s, "nonnegative"):
            raise NotImplementedError("Problem 2 Incomplete")

        first = np.array([-3,-1,3])
        points = 2*self._arrTest(nonnegative(first.copy()),
                                s.nonnegative(first.copy()),
                                "nonnegative(array(%s)) failed"%first)

        second = np.random.randint(-50,50,10)
        points += 3*self._arrTest(nonnegative(second.copy()),
                                s.nonnegative(second.copy()),
                                "nonnegative(array(%s)) failed"%second)
        return points

    def problem3(self, s):
        """Test normal_var(). 10 points."""
        if not hasattr(s, "normal_var"):
            raise NotImplementedError("Problem 3 Incomplete")

        points  = 4*self._eqTest(normal_var(100), s.normal_var(100),
                                    "normal_var(100) failed", tol=.01)
        points += 6*self._eqTest(normal_var(1000), s.normal_var(1000),
                                    "normal_var(1000) failed", tol=.0005)
        return points

    @_autoclose
    def problem4(self, s):
        """Test laplace_plot(). 10 points."""
        if not hasattr(s, "laplace_plot"):
            raise NotImplementedError("Problem 4 Incomplete")

        print("\nGenerating laplace plot...")
        s.laplace_plot()
        return self._grade(10, "Incorrect plot.")

    @_autoclose
    def problem5(self, s):
        """Test blue_shift_plot(). 10 points."""
        if not hasattr(s, "blue_shift_plot"):
            raise NotImplementedError("Problem 5 Incomplete")

        print("\nGenerating blue shift plot...")
        s.blue_shift_plot()
        return self._grade(10, "Incorrect plot.")

# END OF FILE =================================================================
