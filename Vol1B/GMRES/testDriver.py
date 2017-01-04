#solutions.py
"""
Vol I Lab __: GMRES
January 8, 2016
"""
import numpy as np
import numpy.linalg as la
from matplotlib import pyplot as plt
import time

#Problem 1: Implement the following function
def gmres(A, b, x0, k=100, tol=1e-8):
    '''Calculate approximate solution of Ax=b using GMRES algorithm.
    
    INPUTS:
    A    - Callable function that calculates Ax for any input vector x.
    b    - A NumPy array of length m.
    x0   - An arbitrary initial guess.
    k    - Maximum number of iterations of the GMRES algorithm. Defaults to 100.
    tol  - Stop iterating if the residual is less than 'tol'. Defaults to 1e-8.
    
    RETURN:
    Return (y, res) where 'y' is an approximate solution to Ax=b and 'res' 
    is the residual.
    '''
    #initialize stuff
    Q = np.empty((b.size, k + 1))
    H = np.zeros((k + 1, k))
    r0 = b - A(x0)
    beta = la.norm(r0, 2)
    be1 = np.zeros(k + 1)
    be1[0] = beta
    
    Q[:,0] = r0/beta
    
    # arnoldi iteration
    for j in xrange(k):
        Q[:,j+1] = A(Q[:,j])
        for i in xrange(j+1):
            H[i,j] = np.inner(Q[:,i],Q[:,j+1])
            Q[:,j+1] -= H[i,j] * Q[:,i]
        H[j+1,j] = la.norm(Q[:,j+1],2)
        if H[j+1,j] > tol:  # Don't divide by 0
            Q[:,j+1] /= H[j+1,j]
            
        # least squares bit       
        y, r = la.lstsq(H[:j+2,:j+1], be1[:j+2])[:2]
        
        #residual is root of what lstsq returns
        res = np.sqrt(r[0])
        
        if res < tol:
            return Q[:,:j+1].dot(y) + x0, res
            
    return Q[:,:j+1].dot(y) + x0, res
    
    
#Problem 2: Implement the following two functions
def plot_gmres(A, b, x0, tol=1e-8):
    '''Use the GMRES algorithm to approximate the solution to Ax=b.  Plot the
    eigenvalues of A and the convergence of the algorithm.
    
    INPUTS:
    A   - A 2-D NumPy array of shape mxm.
    b   - A 1-D NumPy array of length m.
    x0  - An arbitrary initial guess.
    tol - Stop iterating and create the desired plots when the residual is
          less than 'tol'. Defaults to 1e-8.
    
    OUTPUT:
    Follow the GMRES algorithm until the residual is less than tol, for a 
    maximum of m iterations. Then create the two following plots (subplots
    of a single figure):
     
    1. Plot the eigenvalues of A in the complex plane.
    
    2. Plot the convergence of the GMRES algorithm by plotting the
    iteration number on the x-axis and the residual on the y-axis.
    Use a log scale on the y-axis.
    '''
    k = b.size
    Q = np.empty((k, k + 1))
    H = np.zeros((k+1, k))
    
    Amul = lambda x: np.dot(A, x)
    r0 = b - Amul(x0)
    beta = la.norm(r0, 2)
    Q[:,0] = r0 / beta
    be1 = np.zeros(k+1)
    be1[0] = beta
    
    residuals = []
    
    # arnoldi iteration
    for j in xrange(k-1):
        Q[:,j+1] = Amul(Q[:,j])
        for i in xrange(j+1):
            H[i,j] = np.inner(Q[:,i],Q[:,j+1])
            Q[:,j+1] -= H[i,j] * Q[:,i]
        H[j+1,j] = la.norm(Q[:,j+1],2)
        if H[j+1,j] > tol:  # Don't divide by 0
            Q[:,j+1] /= H[j+1,j]

        # least squares bit       
        y, r = la.lstsq(H[:j+2,:j+1], be1[:j+2])[:2]
        
        #compute residual and add to list
        res = np.sqrt(r[0])
        residuals.append(res)
        
        if res < tol or H[j+1,j] < tol:
            break
    
    eigs = la.eig(A)[0]
    l = len(residuals)
    x = np.linspace(0, l-1, l)
    
    plt.subplot(1,2,1)
    plt.scatter(np.real(eigs),np.imag(eigs))
    plt.xlim([-5,5])
    plt.ylim([-2,2])
    
    plt.subplot(1,2,2)
    plt.yscale('log')
    plt.plot(x,residuals)
    
    plt.show()

    
def make_plots(m=200):
    '''Create the matrix An defined in problem 2 in the manual 
    for n = -4, -2, -0, 2, 4.  Call plot_gmres on each, with b 
    a vector of ones, and an initial guess x0 a vector of zeros.
    Print a statement explaining how the convergence relates to 
    the eigenvalues.
    '''
    for n in (-4, -2, 0, 2, 4):
        P = np.random.normal(0, .5/np.sqrt(m), (m,m))
        An = n*np.eye(m) + P
        b = np.ones(m)
        x0 = 0 * b
        plot_gmres(An, b, x0)
    
    print "The algorithm converges more slowly when the eigenvalues are clustered around the origin."
    
    
#Problem 3: Implement the following two functions
def gmres_k(Amul, b, x0, k=5, tol=1E-8, restarts=50):
    '''Use the GMRES(k) algorithm to approximate the solution to Ax=b.
    
    INPUTS:
    A   - A Callable function that calculates Ax for any vector x.
    b   - A NumPy array.
    x0  - An arbitrary initial guess.
    k   - Maximum number of iterations of the GMRES algorithm before
        restarting. Defaults to 5.
    tol - Stop iterating if the residual is less than 'tol'. Defaults
        to 1E-8.
    restarts - Maximum number of restarts. Defaults to 50.
    
    OUTPUT:
    Return (y, res) where 'y' is an approximate solution to Ax=b and 'res'
    is the residual.
    '''
    r = 0
    
    while r <= restarts:
        # Perform GMRES
        y, res = gmres(Amul, b, x0, k, tol)
        if res < tol:
            return y, res
        else:
            # Update guess
            x0 = y
            r += 1
            
    return y, res
    
    
def time_gmres(s,m=200):
    '''Time the gmres and gmres_k functions on each of the matrices
    from problem 2.  Let x0 be a vector of zeros or anything you like.
    The results might be more dramatic with an x0 of larger magnitude.
    Print your results.  What do you observe?
    Inputs:
    s - student module
    m - matrix size
    '''
    for n in (-4, -2, 0, 2, 4):
        P = np.random.normal(0, .5/np.sqrt(m), (m,m))
        An = n*np.eye(m) + P
        b = np.ones(m)
        Amul = lambda x: np.dot(An, x)
        x0 = 0 * b
        
        t1 = time.clock()
        y1, res = s.gmres(Amul, b, x0)
        t2 = time.clock()

        y2, res = s.gmres_k(Amul, b, x0)
        t3 = time.clock()
        
        print "n =",
        print n,
        print ":"
        
        print "GMRES:   ",
        print t2 - t1
        
        print "GMRES(k):",
        print t3 - t2
        print
    

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
        
    def _evalTest(self, expression, message):
        """Test a boolean 'expression' to see if it is 'correct'.
        Report the given 'message' if it is not.
        """
        if expression:
            return 1
        else:
            self.feedback += "\n%s"%message
            return 0
        
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
        print "Testing 1"
        points = 0
        
        #test case 1
        a = np.array([[1,0,0],[0,2,0],[0,0,3]])
        A = lambda x: a.dot(x)
        b = np.array([1, 4, 6])
        x0 = np.zeros(b.size)
        tol = 1e-8
        x = np.array([1.,2.,2.])
        x_student, res = s.gmres(A, b, x0,tol=tol)
        print x_student.shape
        p = self._evalTest(np.allclose(x,x_student,2e-4,2e-4),"Incorrect output for example problem")
        points += p*10
        
        P = np.random.normal(0, .5/np.sqrt(50), (50,50))
        a = 4*np.eye(50) + P
        A = lambda x: a.dot(x)
        b = np.ones(50)
        x0 = np.zeros(b.size)
        tol = 1e-8
        x, res = gmres(A,b,x0)
        x_student, res_student = s.gmres(A,b,x0,tol=tol)
        print x_student.shape
        p = self._evalTest(np.allclose(x,x_student,2e-4,2e-4),"Incorrect output when testing on A = 4I + P")
        points += p*6
        p = self._evalTest((res_student<=tol),"res didn't converge to less than tol when it should have")
        points += 4*p
        return points
        
        
    def problem2(self, s):
        """Test Problem 2."""
        print "Testing 2"
        s.problem2()
        plt.show()
        points = self._grade(10)
        return points
        
    def problem3(self,s):
        """Test Problem 3."""
        print "Testing 3"
        time_gmres(s)
        points = self._grade(10)
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
        test_one(self.problem1, 1, 20)   
        test_one(self.problem2, 2, 10)  
        test_one(self.problem3, 3, 10)
        
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






    


