# testDriver.py
"""Volume II Lab 7: Nearest Neighbor Search. Test Driver.

< IN DEVELOPMENT >

"""

import inspect
import numpy as np
from scipy.spatial import KDTree
from new_solutions import metric, postal_problem


def test(student_module):
    """Test script. You must import the students file as a module.
    
     5 points for problem 1
     5 points for problem 2
    10 points for problem 3
    10 points for problem 4
    20 points for problem 5
    10 points for problem 6
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of 80.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""
    def __init__(self):
        self.feedback = ""

    # Main routine ------------------------------------------------------------
    def test_all(self, student_module):
        self.feedback = ""
        score = 0

        try:    # Problem 1: 5 points
            self.feedback += "\n\nProblem 1 (5 points):"
            points = self.problem1(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 2: 5 points
            self.feedback += "\n\nProblem 2 (5 points):"
            points = self.problem2(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message

        try:    # Problems 4 and 5: 30 points
            self.feedback += "\n\nProblems 4 and 5 (30 points):"
            points = self.problem5(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message

        try:    # Problem 6: 10 points
            self.feedback += "\n\nProblem 6 (10 points):"
            # points = self.problem6(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        # Report final score.
        total = 50
        perc = (100. * score) / total
        self.feedback += "\n\nTotal score: %d/%d = %s%%"%(score, total, perc)
        if   perc >=  98.0: self.feedback += "\n\nExcellent!"
        elif perc >=  90.0: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print self.feedback
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t' + comments
        self.score = score
        
    # Helper functions --------------------------------------------------------
    def numTest(self, correct, student, message):
        """Test to see if correct and student are numerically close.
        If not, provide feedback. Return 1 for correct and 0 otherwise.
        """
        if np.allclose(correct, student, atol=1e-04):
            return 1
        else:
            self.feedback += message
            self.feedback += "\nCorrect response:\n" + str(correct)
            self.feedback += "\nStudent response:\n" + str(student)
            return 0

    def grade(self, points):
        """Manually grade a problem out of 'points'. Return the points earned.
        """
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of " + str(points) + ": "))
            except:
                credit = -1
        if credit != points:
            self.feedback += "\n\t" + str(raw_input("Describe problem: "))
        return credit

    def neighbor(self, m, k, func):
        """Do a single nearest neighbor search trial for mxk data,
        solved with the function 'func'.
        """
        data = np.random.random((m, k))
        target = np.random.random(k)
        tree = KDTree(data)
        dist, index = tree.query(target)
        point = tree.data[index]
        spoint, sdist = func(data, target) # func solves the problem
        p1 = self.numTest(point, spoint,
            "\n\t"+func.__name__+"() failed: incorrect nearest neighbor")
        p2 = self.numTest(dist, sdist, 
            "\n\t"+func.__name__+"() failed: incorrect minimum distance")
        return p1 + p2

    @staticmethod
    def get_code(func):
        rawcode = inspect.getsource(func).splitlines()[len(
                                            func.__doc__.splitlines())+1:]
        for line in rawcode: print line

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test metric(). 5 Points."""

        # Test with good inputs (4 points)
        x = np.array([1, 2])
        y = np.array([2, 2])
        points = self.numTest(metric(x,y), s.metric(x,y),
                                            "\n\tmetric() failed.")
        
        x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        y = np.array([2, 6, 4, 8, 0, 2, 4, 7, 5, 11])
        points += self.numTest(metric(x,y), s.metric(x,y),
                                            "\n\tmetric() failed.")
        
        x = (np.random.random(100)-.5)*200
        y = (np.random.random(100)-.5)*200
        points += self.numTest(metric(x,y), s.metric(x,y),
                                        "\n\tmetric() failed.")*2
        
        # Test with bad inputs (1 point)
        x = np.array([1, 2])
        y = np.array([1, 2, 3])
        try:
            s.metric(x, y)
            self.feedback += "\n\tmetric() failed to raise a "
            self.feedback += "ValueError for vectors of different lengths"
        except:
            points += 1

        return points

    def problem2(self, s):
        """Test exhaustive_search(). 5 points."""
    
        points  = self.neighbor(100, 10, s.exhaustive_search)
        points += self.neighbor(10, 100, s.exhaustive_search)
        points += 1

        _testDriver.get_code(s.exhaustive_search)
        print "\n(Check that scipy.spatial.KDTree is not used)"
        points *= self.grade(1)

        return points

    def problem3(self, s):
        """Test the KDTNode class. 10 points."""

        points = 0

        # Test KDTNode.__init__ (can only hold np.ndarrays; 2 points)
        try:
            s.KDTNode("This is not a numpy array")
            self.feedback += "\n\tKDTNode(x) failed to raise a TypeError "
            self.feedback += "for x not a numpy array (np.ndarray)"
        except:
            points += 2

        # Test KDTNode.__sub__ (euclidean distance; 2 points)
        x = np.random.random(10); y = np.random.random(10)
        A =   KDTNode(x); B =   KDTNode(y)
        C = s.KDTNode(x); D = s.KDTNode(y)
        points += 2*self.numTest(A-B, C-D, "\n\tKDTNode.__sub__ failed")

        # Test KDTNode.__eq__ (1 Point)
        D = s.KDTNode(1.5*x)
        if not (C == D):
            points += 1
        else:
            self.feedback += "\n\tKDTNode.__eq__ failed on nonequal"

        # Test KDTNode.__lt__ and KDTNode.__gt__ (5 points)
        x = s.KDTNode(np.array([3,1,0,5], dtype=np.int)); x.axis = 0
        y = s.KDTNode(np.array([1,2,4,3], dtype=np.int)); y.axis = 1
        if x < y: points += 1
        else: self.feedback += "\n\tKDTNode.__lt__ failed"
        if y < x: points += 1
        else: self.feedback += "\n\tKDTNode.__lt__ failed"

        x.axis = 2; y.axis = 3
        if x > y: points += 1
        else: self.feedback += "\n\tKDTNode.__gt__ failed"
        if y > x: points += 2
        else: self.feedback += "\n\tKDTNode.__gt__ failed"

        return points
    
    def problem5(self, s):
        """Test nearest_neighbor(). 30 points."""
        points = 0

        points  = self.neighbor( 10,  10, s.nearest_neighbor)*3
        points += self.neighbor(100,  10, s.nearest_neighbor)*3
        points += self.neighbor( 10, 100, s.nearest_neighbor)*3
        points += self.neighbor(100, 100, s.nearest_neighbor)*3
        points += self.neighbor(100, 100, s.nearest_neighbor)*3

        _testDriver.get_code(s.nearest_neighbor)
        print "\n(Check that scipy.spatial.KDTree is not used)"
        points *= self.grade(1)
        
        return points

    def problem6(self, s):
        """Test postal_problem(). 10 points."""

        print("Correct responses:")
        postal_problem(grading=True)
        print("\nStudent responses:")
        x = s.postal_problem()
        if x is not None:
            print x
        
        return self.grade(10)

if __name__ == '__main__':
    import new_solutions as sol
    score, feedback = test(sol)

# =============================== END OF FILE =============================== #
