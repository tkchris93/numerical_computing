# solutions.py
"""Volume 1, Lab 16: Importance Sampling and Monte Carlo Simulations.
Solutions file. Written by Tanner Christensen, Winter 2016.
"""

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def prob1(n):
    """Approximate the probability that a random draw from the standard
    normal distribution will be greater than 3."""
    h = lambda x : x > 3
    X = np.random.randn(n)
    return 1/n * np.sum(h(X))

def prob2():
    """Answer the following question using importance sampling: 
            A tech support hotline receives an average of 2 calls per 
            minute. What is the probability that they will have to wait 
            at least 10 minutes to receive 9 calls?
    Returns:
        IS (array) - an array of estimates using 
            [5000, 10000, 15000, ..., 500000] as number of 
            sample points."""
    h = lambda y : y > 10
    f = lambda y : stats.gamma(a=9,scale=0.5).pdf(y)
    g = lambda y : stats.norm(loc=12,scale=2).pdf(y)
    num_samples = np.arange(5000,505000,5000)
    IS = []
    for n in num_samples:
        Y = np.random.normal(12,2,n)
        approx = 1./n*np.sum(h(Y)*f(Y)/g(Y))
        IS.append(approx)
    IS = np.array(IS)
    return IS

def prob3():
    """Plot the errors of Monte Carlo Simulation vs Importance Sampling
    for the prob2()."""
    h = lambda x : x > 10
    MC_estimates = []
    for N in xrange(5000,505000,5000):
        X = np.random.gamma(9,scale=0.5,size=N)
        MC = 1./N*np.sum(h(X))
        MC_estimates.append(MC)
    MC_estimates = np.array(MC_estimates)

    IS_estimates = prob2()
    
    actual = 1 - stats.gamma(a=9,scale=0.5).cdf(10)

    MC_errors = np.abs(MC_estimates - actual)
    IS_errors = np.abs(IS_estimates - actual)
    
    x = np.arange(5000,505000,5000)
    plt.plot(x, MC_errors, color='r', label="Monte Carlo")
    plt.plot(x, IS_errors, color='b', label="Importance Sampling")
    plt.legend()
    plt.show()
    
def prob4():
    """Approximate the probability that a random draw from the
    multivariate standard normal distribution will be less than -1 in 
    the x-direction and greater than 1 in the y-direction."""
    h = lambda y : y[0] < -1 and y[1] > 1
    f = lambda y : stats.multivariate_normal(np.zeros(2), np.eye(2)).pdf(y)
    g = lambda y : stats.multivariate_normal(np.array([-1,1]), np.eye(2)).pdf(y)
    
    n = 10**4
    Y = np.random.multivariate_normal(np.array([-1,1]), np.eye(2), size=n)
    hh = np.apply_along_axis(h, 1, Y)
    ff = np.apply_along_axis(f, 1, Y)
    gg = np.apply_along_axis(g, 1, Y)
    approx = 1./n*np.sum(hh*ff/gg)

    return approx


#Test Script and Class =======================================================

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
        """Test Problem 1. X points."""
        estimate1 = s.prob1(50000)
        estimate2 = s.prob1(5000000)
        print "Problem 1: (should approach 0.0013499 for large n)"
        print "Estimate for n = 50000: {}".format(estimate1)
        print "Estimate for n = 5000000: {}".format(estimate2)
        points = self._grade(10)
        # Test problem 1 here.
        return points 
        
    def problem2(self, s):
        vals = s.prob2()
        x = np.linspace(5000,50000,np.size(vals))
        plt.plot(x,vals)
        plt.title("Estimate for probability of waiting 10 minutes")
        plt.xlabel('# Sample Points')
        plt.ylabel('Probability')
        plt.show()
        print "Final estimate: {} (should approach .00208)".format(vals[-1])
        
        points = self._grade(10)
        return points
        
    
    def problem3(self, s):
        plt.ylim([0,0.0012])
        s.prob3()
        points = self._grade(10)
        return points
        
    def problem4(self, s):
        estimate = s.prob4()
        print "Estimate for problem 4: {}".format(estimate)
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
        test_one(self.problem1, 1, 10)   # Problem 1: 10 points.
        test_one(self.problem2, 2, 10)   # Problem 2: 10 points.
        test_one(self.problem3, 3, 10)   # Problem 3: 10 points
        test_one(self.problem4, 4, 10)   # Problem 4: 10 points
        
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






    


