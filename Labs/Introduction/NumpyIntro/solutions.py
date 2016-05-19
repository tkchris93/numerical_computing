# solutions.py
"""NumPy and SciPy Arrays solutions file."""

import numpy as np
from matplotlib import pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


def prob1():
    A = np.array([[3,-1,4],[1,5,-9]])
    B = np.array([[2,6,-5,3],[5,-8,9,7],[9,-3,-2,-3]])
    print A
    print B
    return A.dot(B)

def prob2():
    A = np.array([[3,1,4],[1,5,9],[-5,3,1]])
    A2 = np.dot(A, A)
    return -np.dot(A, A2) + 9*A2 - 15*A

def prob3():
    A = np.triu(np.ones((7,7)))
    B = np.full_like(A, 5) - np.tril(np.full_like(A, 6))
    return np.dot(np.dot(A, B), A).astype(np.int64)

def prob4(A):
    """Make a copy of 'A' and change all negative entries
    of the copy to 0. Return the copy.

    Example:
        >>> A = np.array([-3,-1,3])
        >>> prob4(A)
        array([0, 0, 3])
    """
    B = A.copy()
    B[A < 0] = 0
    return B

def prob5():
    A = np.arange(6).reshape((3,2)).T
    m, n = A.shape
    B = np.tril(np.full((3,3), 3, dtype=np.float64))
    C = -2*np.eye(3)
    O = np.zeros_like(A)
    return np.vstack((  np.hstack((np.zeros((n,n)), A.T,     np.eye(n))),
                        np.hstack((A,               np.zeros((m,m)), O)),
                        np.hstack((B,               O.T,             C))  ))

def prob6(A):
    """Divide each row of 'A' by the row sum and return the resulting array.

    Example:
        >>> A = np.array([[1,1,0],[0,1,0],[1,1,1]])
        >>> prob6(A)
        array([[ 0.5       ,  0.5       ,  0.        ],
               [ 0.        ,  1.        ,  0.        ],
               [ 0.33333333,  0.33333333,  0.33333333]])
    """
    return A / A.sum(axis=1)[:,np.newaxis].astype(np.float64)


def jacobi(n=100, tol=1e-8):
    """Solve Laplace's Equation using the Jacobi method and array slicing."""
    # Initialize the plate.
    U = np.zeros((n,n))

    # Set boundary conditions.
    U[:, 0] = 100                   # West boundary condition.
    U[:,-1] = 100                   # East boundary condition.
    U[ 0,:] = 0                     # North boundary condition.
    U[-1,:] = 0                     # South boundary condition.

    # Make a copy and initialize a difference variable.
    V = np.copy(U)
    diff = tol

    # Perform the iteration.
    while diff >= tol:
        V[1:-1,1:-1] = (U[:-2,1:-1] + U[2:,1:-1] + U[1:-1,:-2] + U[1:-1,2:])/4.
        diff = np.max(np.abs(U-V))
        U[1:-1,1:-1] = V[1:-1,1:-1]

    # Visualize the results.
    plt.imshow(U)
    plt.show()
    
    # x, y = np.linspace(0, 1, n), np.linspace(0, 1, n)
    # X, Y = np.meshgrid(x, y)
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.plot_surface (X, Y, U, rstride=5)
    # plt.show()


    
# END OF SOLUTIONS ============================================================

from functools import wraps
from numpy.random import randint

# Test script
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

def _autoclose(func):
    """Decorator for closing figures automatically during grading."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            plt.ion()
            return func(*args, **kwargs)
        finally:
            plt.close('all')
            plt.ioff()
    return wrapper

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
        if np.allclose(correct, student):
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
        
        second = randint(-50,50,10)
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
