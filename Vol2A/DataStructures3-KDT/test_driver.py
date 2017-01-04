# test_driver.py
"""Volume 2A: Nearest Neighbor Search. Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout

import inspect
import numpy as np
from scipy.spatial import KDTree
from solutions import metric, postal_problem


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1
     5 points for problem 2
    10 points for problem 3
    10 points for problem 4
    20 points for problem 5
    10 points for problem 6

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.problems = [   (self.problem1, "Problem 1", 5),
                            (self.problem2, "Problem 2", 5),
                            (self.problem5, "Problems 4 and 5", 30),
                            (self.problem6, "Problem 6", 10)            ]


    # Helper Functions --------------------------------------------------------
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
        p1 = self._eqTest(point, spoint,
            "\n\t"+func.__name__+"() failed: incorrect nearest neighbor")
        p2 = self._eqTest(dist, sdist,
            "\n\t"+func.__name__+"() failed: incorrect minimum distance")
        return p1 + p2

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test metric(). 5 Points."""

        # Test with good inputs (4 points)
        x = np.array([1, 2])
        y = np.array([2, 2])
        points = self._eqTest(metric(x,y), s.metric(x,y),
                                            "\n\tmetric() failed.")

        x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        y = np.array([2, 6, 4, 8, 0, 2, 4, 7, 5, 11])
        points += self._eqTest(metric(x,y), s.metric(x,y),
                                            "\n\tmetric() failed.")

        x = (np.random.random(100)-.5)*200
        y = (np.random.random(100)-.5)*200
        points += self._eqTest(metric(x,y), s.metric(x,y),
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
        points += 3 * self.neighbor(10, 100, s.exhaustive_search) / 2.

        # Check that scipy.spatial.KDTree is not used.
        points *= self._checkCode(s.exhaustive_search, "KDTree")
        return int(points)

    # TODO: OUT OF DATE
    def problem3(self, s):
        """Test the KDTNode class. 10 points."""
        points = 0

        # KDTNode.__init__() (can only hold np.ndarrays; 2 points)
        try:
            s.KDTNode("This is not a numpy array")
            self.feedback += "\n\tKDTNode(x) failed to raise a TypeError "
            self.feedback += "for x not a numpy array (np.ndarray)"
        except:
            points += 2

        # KDTNode.__sub__() (euclidean distance; 2 points)
        x = np.random.random(10); y = np.random.random(10)
        A =   KDTNode(x); B =   KDTNode(y)
        C = s.KDTNode(x); D = s.KDTNode(y)
        points += 2*self._eqTest(A-B, C-D, "\n\tKDTNode.__sub__ failed")

        # KDTNode.__eq__() (1 Point)
        D = s.KDTNode(1.5*x)
        if not (C == D):
            points += 1
        else:
            self.feedback += "\n\tKDTNode.__eq__() failed on nonequal"

        # KDTNode.__lt__() and KDTNode.__gt__() (5 points)
        x = s.KDTNode(np.array([3,1,0,5], dtype=np.int)); x.axis = 0
        y = s.KDTNode(np.array([1,2,4,3], dtype=np.int)); y.axis = 1
        if x < y: points += 1
        else: self.feedback += "\n\tKDTNode.__lt__() failed"
        if y < x: points += 1
        else: self.feedback += "\n\tKDTNode.__lt__() failed"

        x.axis = 2; y.axis = 3
        if x > y: points += 1
        else: self.feedback += "\n\tKDTNode.__gt__() failed"
        if y > x: points += 2
        else: self.feedback += "\n\tKDTNode.__gt__() failed"

        return points

    def problem5(self, s):
        """Test nearest_neighbor(). 30 points."""
        points = 0

        points  = self.neighbor( 10,  10, s.nearest_neighbor)*3
        points += self.neighbor(100,  10, s.nearest_neighbor)*3
        points += self.neighbor( 10, 100, s.nearest_neighbor)*3
        points += self.neighbor(100, 100, s.nearest_neighbor)*3
        points += self.neighbor(100, 100, s.nearest_neighbor)*3

        # Check that scipy.spatial.KDTree is not used.
        points *= self._checkCode(s.nearest_neighbor, "KDTree")
        return int(points)

    def problem6(self, s):
        """Test postal_problem(). 10 points."""

        print("Correct responses:")
        postal_problem(grading=True)
        print("\nStudent responses:")
        x = s.postal_problem()
        if x is not None:
            print x

        return self._grade(10)

# Main Routine ================================================================

def test(student_module, total=60):
    """Grade a student's entire solutions file.

     5 points for problem 1
     5 points for problem 2
    10 points for problem 3
    10 points for problem 4
    20 points for problem 5
    10 points for problem 6

    Inputs:
        student_module: the imported module for the student's file.
        total (int): the total possible score.

    Returns:
        score (int): the student's score, out of 'total'.
        feedback (str): a printout of results for the student.
    """
    tester = TestDriver()
    tester.test_all(student_module, total)
    return tester.score, tester.feedback

# Validation ==================================================================

if __name__ == '__main__':
    import solutions
    test(solutions)
