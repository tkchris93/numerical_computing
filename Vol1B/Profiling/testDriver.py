# Test Script and Class =======================================================
import numpy as np

def LU(A):
    """Returns the LU decomposition of a square matrix."""
    n = A.shape[0]
    U = np.array(np.copy(A), dtype=float)
    L = np.eye(n)
    for i in range(1,n):
        for j in range(i):
            L[i,j] = U[i,j]/U[j,j]
            for k in range(j,n):
                U[i,k] -= L[i,j] * U[j,k]
    return L,U
    

def test(student_module):
    """Test script. Import the student's solutions file as a module.
        
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
    tester.test_all(student_module, total=40)
    return tester.score, tester.feedback


class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""
    
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""
        
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        if isinstance(error, BaseException):
            return str(type(error)).lstrip("<type 'exceptions.").rstrip("'>")
        else:
            return str(error)
        
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
                self.feedback += "\n%s"%comments
                # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n%s"%message
        return credit
    
    # Main routine -----------------------------------------------------------
    def problem1(self, s):
        """Test Problem 1. X points."""
        print "\n\nTest the compare_timings function by comparing 2 adding functions.\n\n"         
        
        def add_small(b):
            for i in xrange(100):
                b += 1
            return b
            
        def add_large(c):
            for i in xrange(30000000):
                c += 1
            return c
            
        comparison = s.compare_timings(add_small, add_large, 5)
        print comparison        
        points = self._grade(10)
        return points 
        
    def problem2(self, s):
        """Test Problem 2."""
        
        #First check that their optimized LU still works
        B = np.array([[-2,-2,8,-4],[-3,4,-9,-1],[9,1,-3,8],[-1,-9,-1,-1]])

        L, U = s.LU(B.copy()) 
        L2, U2 = s.LU_opt(B.copy())
        assert (np.allclose(L,L2) and np.allclose(U,U2)), "LU and LU_opt don't give the same output."
            
            
        print "\n\nObjective: optimize LU decomposition by not recomputing values."
        print "Inspect the student's code before grading.\n\n"
        A = np.random.rand(100,100)*20        
        print s.compare_LU(A)
        points = self._grade(5)
        return points
    
    def problem3(self, s):
        """Test Problem 3."""
        print "\n\nObjective: demonstrate difference between np.sum and mysum."
        print "Inspect the student's code before grading.\n\n"
        
        x = np.random.rand(50000) #array of length 50000 to sum
        assert (np.allclose(s.mysum(x),np.sum(x))), "mysum doesn't return the same output as np.sum."
        print s.compare_sum(x)
        points = self._grade(5)
        return points
        
    def problem4(self, s):
        """Test Problem 4"""
        print "\n\nFibonacci number generator"
        print "Inspect the student's code before grading.\n\n"
        
        print "Should print a generator object:"
        print s.fib(10)
        
        print "\nShould print the Fibonacci numbers:"
        for n in s.fib(10):
            print n
        
        points = self._grade(5)
        return points
        
    def problem5(self, s):
        """Test Problem 5."""
        print "\n\nObjective: improve the function foo."
        print "Inspect the student's improved implementation before grading.\n\n"
        
        print s.compare_foo(2000000) #two million is a good test size
        
        points = self._grade(5)
        return points
        
    def problem6(self, s):
        """Test problem 6."""
        print "\n\nObjective: improve a matrix power function by using Numba."
        print "Inspect student's code before grading.\n\n"
        A = np.random.rand(20,20)
        print s.compare_matpow(A, 10)
        
        points = self._grade(5)
        return points
        
    def problem7(self, s):
        """This problem keeps crashing. Not going to test it."""
        print "\n\nObjective: improve a tridiag function by using Numba, then compare it to a NumPy version"
        print "Inspect student's code before grading.\n\n"
        print s.compare_tridiag()
        
        points = self._grade(5)
        return points
        
    def problem8(self, s):
        """Test Problem 8"""
        print "\n\nImprove a function from a previous lab."
        print "Definitely inspect student's code on this one.\n\n"
        print s.compare_old()
        
        points = self._grade(5)
        return points
    
        
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
        test_one(self.problem1, 1, 10)   # Problem 1: 5 points.
        test_one(self.problem2, 2, 5)   # Problem 2: 5 points.
        test_one(self.problem3, 3, 5)   # Problem 3: 5 points.
        test_one(self.problem4, 4, 5)   # Problem 4: 5 points.
        test_one(self.problem5, 5, 5)   # Problem 5: 5 points.
        test_one(self.problem6, 6, 5)   # Problem 6: 5 points.
        #Dropped this problem
        #test_one(self.problem7, 7, 5)   # Problem 7: 5 points.
        test_one(self.problem8, 8, 5)   # Problem 8: 5 points.
        
        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: %d/%d = %s%%"%(self.score, total, percentage)
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"
          
        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t%s'%comments

# Possible Helper Functions -----------------------------------------------

def _eqTest(self, correct, student, message):
    """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
    if correct == student:
        return 1
    else:
        self.feedback += "\n%s"%message
        self.feedback += "\n\tCorrect response: %s"%correct
        self.feedback += "\n\tStudent response: %s"%student
        return 0

def _strTest(self, correct, student, message):
    """Test to see if 'correct' and 'student' have the same string
        representation. Report the given 'message' if they are not.
        """
    if str(correct) == str(student):
        return 1
    else:
        self.feedback += "\n%s"%message
        self.feedback += "\n\tCorrect response: %s"%correct
        self.feedback += "\n\tStudent response: %s"%student
        return 0

def _evalTest(self, expression, correct, message):
    """Test a boolean 'expression' to see if it is 'correct'.
        Report the given 'message' if it is not.
        """
    if expression is correct:
        return 1
    else:
        self.feedback += "\n%s"%message
        return 0






    


