import numpy as np
import scipy.sparse as spar
import scipy.linalg as la
from scipy.sparse import linalg as sla
import pdb

def to_matrix(filename,n):
    '''
    Return the nxn adjacency matrix described by datafile.
    INPUTS:
    datafile (.txt file): A .txt file describing a directed graph. Lines
        describing edges should have the form '<from node>\t<to node>\n'.
        The file may also include comments.
    n (int): The number of nodes in the graph described by datafile
    RETURN:
        Return a SciPy sparse `dok_matrix'.
    '''
    adj = spar.dok_matrix((n,n))
    with open(filename, 'r') as myfile:
        for line in myfile:
            line = line.strip().split()
            try:
                x,y = int(line[0]),int(line[1])
                adj[x,y] = 1
            except:
                continue
    return adj

def calculateK(A,N):
    '''
    Compute the matrix K as described in the lab.
    Input:
        A (array): adjacency matrix of an array
        N (int): the datasize of the array
    Return:
        K (array)
    '''
    n = A.shape[0]
    D = np.zeros(n)
    for row in range(n):
        D[row] = A[row].sum()
    for i in range(n):
        if D[i] == 0:
            D[i] = n
            A[i] = np.ones(n)
    K = (A.T/D)
    return K[:N,:N]

def iter_solve(adj, N=None, d=.85, tol=1E-5):
    '''
    Return the page ranks of the network described by `adj`.
    Iterate through the PageRank algorithm until the error is less than `tol'.
    Inputs:
    adj - A NumPy array representing the adjacency matrix of a directed graph
    N (int) - Restrict the computation to the first `N` nodes of the graph.
            Defaults to N=None; in this case, the entire matrix is used.
    d     - The damping factor, a float between 0 and 1.
            Defaults to .85.
    tol  - Stop iterating when the change in approximations to the solution is
        less than `tol'. Defaults to 1E-5.
    Returns:
    The approximation to the steady state.
    '''
    if N is None:
        N = adj.shape[1]
    pt = np.ones((N,1))/N    
    K = calculateK(adj,N)
    pt1 = d*np.dot(K,pt) + ((1.-d)/N)*np.ones((N,1))
    while la.norm(pt1-pt) > tol:
        pt = pt1
        pt1 = d*np.dot(K,pt) + ((1.-d)/N)*np.ones((N,1))
    return pt1

def eig_solve( adj, N=None, d=.85):
    '''
    Return the page ranks of the network described by `adj`. Use the
    eigenvalue solver in \li{scipy.linalg} to calculate the steady state
    of the PageRank algorithm
    Inputs:
    adj - A NumPy array representing the adjacency matrix of a directed graph
    N - Restrict the computation to the first `N` nodes of the graph.
            Defaults to N=None; in this case, the entire matrix is used.
    d     - The damping factor, a float between 0 and 1.
            Defaults to .85.
    Returns:
    Use the eigenvalue solver in \li{scipy.linalg} to calculate the steady
    state of the PageRank algorithm.
    '''
    if N is None:
        N = adj.shape[1]
    K = calculateK(adj,N)
    B = d*K + ((1.-d)/N)*np.ones((N,N))
    evalues,evectors = la.eig(B)
    pt = (evectors[:,0].real)
    pt = pt*1/pt.sum()
    return pt
            



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
            
    def _evalTest(self, expression, message):
        """Test a boolean 'expression' to see if it is 'correct'.
            Report the given 'message' if it is not.
            """
        if expression:
            return 1
        else:
            self.feedback += "\n%s"%message
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
                self.feedback += "\n%s"%comments
                # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n%s"%message
        return credit
    
    # Main routine -----------------------------------------------------------
    def problem1(self, s):
        """Test Problem 1. 10 points."""
        print "Testing Problem 1: adjacency matrix"
        adj = to_matrix('datafile_test.txt',10).todense()
        adj_student = s.to_matrix('datafile_test.txt', 10).todense()
        p = self._evalTest(np.allclose(adj,adj_student), "Incorrect adjacency matrix")
        # Test problem 1 here.
        points = p*10
        return points 
        
    def problem2(self, s):
        """Test Problem 2."""
        print "Testing Problem 2"
        points = 0
        print "adjacency"
        #pdb.set_trace()
        adj = np.asarray(to_matrix('datafile_test.txt',10).todense())
        print "K"
        K = calculateK(adj, 10)
        print "calculating student K"
        K_student = s.calculateK(adj,10)
        print "checking"
        if np.allclose(K,K_student):
            points = 10
        elif np.allclose(K,K_student.T):
            points = 5
            self.feedback += "\nK is the transpose of what it should be"
        else:
            self.feedback += "\nIncorrect K matrix"
        return points
        
    def problem3(self,s):
        print "Testing Problem 3"
        points = 0
        adj = np.asarray(to_matrix('datafile_test.txt', 10).todense())
        ranks = np.array(iter_solve(adj,d=.85)).squeeze()
        ranks_s = np.array(s.iter_solve(adj,d=.85)).squeeze()
        print "my ranks:",ranks
        print "student ranks:",ranks_s
        p = self._evalTest(np.allclose(ranks, ranks_s,1e-3,1e-3), "incorrect steady state")
        points = 10*p
        return points
        
    def problem4(self, s):
        print "Testing Problem 4"
        points = 0
        adj = np.asarray(to_matrix('datafile_test.txt', 10).todense())
        ranks = np.array(eig_solve(adj)).squeeze()
        ranks_s = np.array(s.eig_solve(adj)).squeeze()
        print "my ranks:",ranks
        print "student ranks:",ranks_s
        p = self._evalTest(np.allclose(ranks, ranks_s,1e-3,1e-3), "incorrect steady state")
        points = 10*p
        return points
        
    def problem5(self, s):
        print "Testing Problem 5"
        team_ranks, teams = s.problem5()
        print teams[:10]
        print teams[-10:]
        points = self._grade(10)
        return points
        
    def problem6(self,s):
        print "Extra credit problem"
        s.problem6()
        points = self._grade(20)
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
        test_one(self.problem1, 1, 10)   
        test_one(self.problem2, 2, 10)   
        test_one(self.problem3, 3, 10)
        test_one(self.problem4, 4, 10)
        test_one(self.problem5, 5, 10)
        test_one(self.problem6, 6, 0)
        
        
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






    


