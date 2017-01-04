import numpy as np

def mc_int(f, mins, maxs, numPoints=500, numIters=100):
    """Use Monte-Carlo integration to approximate the integral of f
    on the box defined by mins and maxs.
    
    Inputs:
        f (function) - The function to integrate. This function should 
            accept a 1-D NumPy array as input.
        mins (1-D np.ndarray) - Minimum bounds on integration.
        maxs (1-D np.ndarray) - Maximum bounds on integration.
        numPoints (int, optional) - The number of points to sample in 
            the Monte-Carlo method. Defaults to 500.
        numIters (int, optional) - An integer specifying the number of 
            times to run the Monte Carlo algorithm. Defaults to 100.
        
    Returns:
        estimate (int) - The average of 'numIters' runs of the 
            Monte-Carlo algorithm.
                
    Example:
        >>> f = lambda x: np.hypot(x[0], x[1]) <= 1
        >>> # Integral over the square [-1,1] x [-1,1]. Should be pi.
        >>> mc_int(f, np.array([-1,-1]), np.array([1,1]))
        3.1290400000000007
    """
    if len(mins) != len(maxs):
        raise ValueError("Dimension of mins and maxs must be the same")
    
    results = []
    for i in xrange(numIters):
        # create points
        dim = len(mins)
        side_lengths = maxs-mins
        points = np.random.rand(numPoints,dim)
        points = side_lengths*points + mins

        # calculate Volume
        V = 1
        for i in xrange(dim):
            V *= maxs[i] - mins[i]

        # apply the function f along axis=1 and sum all the results
        total = np.sum(np.apply_along_axis(f,1,points))
        results.append((V/float(numPoints))*total)
    estimate = np.average(results)
    return estimate
    
def prob4(numPoints=[500]):
    mins = -1*np.ones(4)
    maxs = np.ones(4)
    f = lambda x : np.sin(x[0])*x[1]**5 - x[1]**3 + x[2]*x[3] + x[1]*x[2]**2
    errors = []
    for n in numPoints:
        errors.append(np.abs(mc_int(f, mins, maxs, n)))
    return errors



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
    
    # Main routine -----------------------------------------------------------
    def problem1(self, s):
        """Test Problem 1. 10 points."""
        print "Volume should be approximately 4.189"
        print "With 10^5 points:", s.prob1()
        print "With 10^2 points:", s.prob1(100)
        points = self._grade(10)
        # Test problem 1 here.
        return points 
        
    def problem2(self, s):
        """Test Problem 2. 10 points."""
        print "Value should be approximately 4.502"
        print "With 10^5 points:", s.prob2()
        print "With 10^2 points:", s.prob2(100)
        points = self._grade(10)
        # Test problem 1 here.
        return points 
        
    def problem3(self, s):
        f1 = lambda x:0.5*x**2
        f2 = lambda x: np.exp(-0.5*np.dot(x,x))/((2*np.pi)**(0.5*x.size))
        f3 = lambda x: np.cos(x[0]*x[1]) + np.sin(x[2]*x[3])
        
        min1 = np.array([0.])
        min2 = np.array([-2.,-2.])
        min3 = np.array([-np.pi/2,0.]*2)
        
        max1 = np.array([0.5])
        max2 = np.array([2.,2.])
        max3 = np.array([0,np.pi/2]*2)
        
        msg1 = "Incorrect result on a function with input dimension 1."
        msg2 = "Incorrect result integrating the multivariate normal distribution."
        msg3 = "Incorrect result on a function with input dimension 4."
        
        funcs = [f1, f2, f3]
        mins = [min1, min2, min3]
        maxs = [max1, max2, max3]
        msgs = [msg1, msg2, msg3]
        
        points = 0
        for i in xrange(3):
            val = mc_int(funcs[i], mins[i], maxs[i])
            s_val = s.mc_int(funcs[i], mins[i], maxs[i])
            print val, s_val
            rel_error = np.abs(val - s_val)/val
            if rel_error > 0.1:
                self.feedback += "\n%s"%msgs[i]
            else:
                points += 5
                
        return points
        
    def problem4(self, s):
        errors = s.prob4([50, 5000])
        print errors
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
        test_one(self.problem1, 1, 10)   # Problem 1: X points.
        test_one(self.problem2, 2, 10)   # Problem 2: X points.
        test_one(self.problem3, 3, 15)
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






    


