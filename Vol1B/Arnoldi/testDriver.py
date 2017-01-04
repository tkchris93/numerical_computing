import numpy as np
from numpy.random import rand
from scipy.linalg import eig
from cmath import sqrt
from scipy import sparse as ss
from scipy.sparse.linalg import eigsh

# arnoldi iteration
def arnoldi(b, Amul, k, tol=1E-8):
    """Perform 'k' steps of the Arnoldi Iteration for
    sparse array 'A' and starting point 'b'with multiplicaiton
    function 'Amul'. Stop if the projection of a vector
    orthogonal to the current subspace has norm less than 'tol'."""
    # Some initialization steps.
    # Initialize to complex arrays to avoid some errors.
    Q = np.empty((b.size, k+1), order='F', dtype=np.complex128)
    H = np.zeros((k+1, k), order='F', dtype=np.complex128)
    ritz_vals = []
    # Set q_0 equal to b.
    Q[:,0] = b
    # Normalize q_0.
    Q[:,0] /= sqrt(np.inner(b.conjugate(), b))
    # Perform actual iteration.
    for j in xrange(k):
        # Compute A.dot(q_j).
        Q[:,j+1] = Amul(Q[:,j])
        # Modified Graham Schmidt
        for i in xrange(j+1):
            # Set values of $H$
            H[i,j] = np.inner(Q[:,i].conjugate(), Q[:,j+1])
            Q[:,j+1] -= H[i,j] * Q[:,i]
        # Set subdiagonal element of H.
        H[j+1,j] = sqrt(np.inner(Q[:,j+1].conjugate(), Q[:,j+1]))
        # Stop if ||q_{j+1}|| is too small.
        if abs(H[j+1, j]) < tol:
            # Here I'll copy the array to avoid excess memory usage.
            return np.array(H[:j+1,:j+1], order='F'), Q[:,:j+1]
        # Normalize q_{j+1}
        Q[:,j+1] /= H[j+1, j]
    return H[:-1], Q
    
def ritz(Amul, dim, k, iters):
    b = np.random.rand(dim)
    H,Q = arnoldi(b, Amul, iters)
    ritz_vals = eig(H[:k,:k])[0]
    return np.sort(ritz_vals)

# Test Script and Class =======================================================

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
    tester.test_all(student_module)
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
        
    def _evalTest(self, expression, message):
        """Test a boolean 'expression' to see if it is 'correct'.
            Report the given 'message' if it is not.
            """
        if expression:
            return 1
        else:
            self.feedback += "\n%s"%message
            return 0
    
    # Main routine -----------------------------------------------------------
    def problem1(self, s):
        """Test Problem 1. 20 points."""
        print "\nTesting Problem 1"
        points = 0
        
        m = 7
        A = np.random.rand(m,m)
        b = np.random.rand(m)
        k = 6
        H,Q = arnoldi(b.copy(),A.dot,k)
        H_student, Q_student = s.arnoldi(b.copy(),A.dot,k)
        p = self._evalTest(H.shape==H_student.shape, "shape of H is incorrect; should be {} for dim={}, k={}"\
            .format(H.shape, m, k))
        points += p*5
        p = self._evalTest(Q.shape==Q_student.shape, "shape of Q is incorrect; should be {} for dim={}, k={}"\
            .format(Q.shape, m, k))
        points += p*5
        p = self._evalTest(np.allclose(H,H_student), "arnoldi returns incorrect H")
        points += p*5
        p = self._evalTest(np.allclose(Q,Q_student), "arnoldi returns incorrect Q")
        points += p*5
        return points 
        
    def problem2(self,s):
        """Test Problem 2. 10 points"""
        print "\nTesting Problem 2"
        
        m = [10, 10, 15]
        A = [np.random.rand(m[i],m[i]) for i in xrange(3)]
        iters = [8,8,12]
        k = [3, 3, 3]
        for i in xrange(3):
            eigvals = eig(A[i])[0][:k[i]]
            ritzvals = s.ritz(A[i].dot, m[i], k[i], iters[i])
            print "\neigenvalues: ",eigvals
            print "ritz values: ",ritzvals
            assert eigvals.size==k[i], "number of ritz values returned should equal k"
            assert np.allclose(eigvals[0], ritzvals[0],5e-2,5e-2), \
                "largest ritz value does not converge to largest eigenvalue for a random matrix"
        points = 15
        return points
    
    def problem3(self, s):
        """Test Problem 3, 5 points"""
        print "\nTesting Problem 3"
        eigvals = np.round(s.fft_eigs(dim=2**20, k=4))
        print "eigenvalues of the Fourier Transform:\n",eigvals
        print "Should be +- 1024 and +- 1024i"
        points = self._grade(10)
        return points
        
    def problem4(self, s):
        """Test Problem 4, 5 points"""
        A = np.random.rand(60,60)
        n = 5
        s.plot_ritz(A,n,40)
        points = self._grade(5)
        return points
        
    def test_all(self, student_module, total=50):
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
        test_one(self.problem1, 1, 20)   # Problem 1: 15 points.
        test_one(self.problem2, 2, 15)
        test_one(self.problem3, 3, 10)
        test_one(self.problem4, 4, 5)
        
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






    


