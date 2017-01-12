# test_driver.py
"""Volume 2A: Data Structures 2 (Trees). Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout, _autoclose

from time import time
from numpy.random import choice
from solutions import iterative_search, SinglyLinkedList, BST


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1
    15 points for problem 2
    30 points for problem 3
    10 points for problem 4

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # File to pull info from for testing problem 4.
    data_file = "english.txt"

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.total = 60
        self.problems = [   (self.problem1, "Problem 1",  5),
                            (self.problem2, "Problem 2", 15),
                            (self.problem3, "Problem 3", 30),
                            (self.problem4, "Problem 4", 10)    ]
        self._feedback_newlines = True

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

         5 points for problem 1
        15 points for problem 2
        30 points for problem 3
        10 points for problem 4

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test recursive_search(). 5 points."""
        points = 0

        lls = SinglyLinkedList()
        # Check recursive_search() on empty list (1 point)
        try:
            s.recursive_search(lls, 1)
            self.feedback += "\n\trecursive_search() failed on empty list"
        except ValueError:
            points += 1

        # Check recursive_search() for items in list (3 points)
        lls.append(1)
        lls.append('a')
        lls.append(2)
        points += self._strTest(iterative_search(lls,1),
                               s.recursive_search(lls, 1),
                               "recursive_search(x) failed for x in list")
        points += self._strTest(iterative_search(lls, 'a'),
                               s.recursive_search(lls, 'a'),
                               "recursive_search(x) failed for x in list")
        points += self._strTest(iterative_search(lls, 2),
                               s.recursive_search(lls, 2),
                               "recursive_search(x) failed for x in list")

        # Check recursive_search() for items not in list (1 point)
        try:
            s.recursive_search(lls, 3)
            self.feedback += "\n\trecursive_search(x) failed for x not in list"
        except ValueError:
            points += 1

        # Check that recursion is used somewhere.
        print("Check student code for recursion:\n")
        self._printCode(s.recursive_search)
        points *= self._grade(1, "recursive_search() must use recursion!")
        return points

    @_timeout(5)
    def problem2(self, s):
        """Test BST.insert(). 15 Points."""
        points = 0

        # Empty tree (0 pts)
        tree1, tree2 = BST(), s.BST()
        self._strTest(tree1, tree2, "BST() failed initially!")

        # Inserting root (2 pts)
        tree1.insert(4); tree2.insert(4)
        points += 2*self._strTest(tree1, tree2, "BST.insert(4) failed "
                                 "on root insertion.\n\tPrevious tree:\n[]")

        def test_insert(value, solTree, stuTree):
            oldTree = "\n\tPrevious tree:\n{}".format(solTree)
            solTree.insert(value); stuTree.insert(value)
            p = self._strTest(tree1, tree2,
                        "BST.insert({}) failed{}".format(value, oldTree))
            return p, solTree, stuTree

        # Inserting nonroot (9 pts)
        for i in [2, 1, 3, 10, 5, 6, 9, 7, 11]:
            p, tree1, tree2 = test_insert(i, tree1, tree2)
            points += p
            if p == 0:
                break

        if points >= 11:
            # Inserting already existing value (4 pts)
            def test_duplicate(value, stuTree):
                try:
                    stuTree.insert(value)
                    self.feedback += "\n\tBST.insert({}) failed ".format(value)
                    self.feedback += "for {} already in tree".format(value)
                    return 0
                except ValueError:
                    return 1

            points +=   test_duplicate(4, tree2)
            points +=   test_duplicate(1, tree2)
            points += 2*test_duplicate(7, tree2)

        else:
            self.feedback += "\nAll BST.remove() tests are likely to fail"
            self.feedback += " unless all BST.insert() tests pass!"

        return points

    @_timeout(5)
    def problem3(self, s):
        """Test BST.remove(). 30 points."""

        def load_trees(entries):
            solutions_tree, student_tree = BST(), s.BST()
            for i in entries:
                solutions_tree.insert(i)
                student_tree.insert(i)
            if str(solutions_tree) != str(student_tree):
                raise NotImplementedError("BST.remove() cannot be tested "
                                          "until BST.insert() is correct")
            return solutions_tree, student_tree

        def test_remove(value, solTree, stuTree):
            oldTree = "\n\tPrevious tree:\n{}".format(solTree)
            try:
                solTree.remove(value); stuTree.remove(value)
                p = self._strTest(solTree, stuTree,
                        "BST.remove({}) failed{}".format(value, oldTree))
            except Exception as e:
                self.feedback += "\n\t{} while removing {}".format(
                                                    self._objType(e), value)
                self.feedback += ": {}{}".format(e, oldTree)
                p = 0
            finally:
                return p, solTree, stuTree

        def remove_many(data, targets):
            pts = 0
            tree1, tree2 = load_trees(data)
            for i in targets:
                p, tree1, tree2 = test_remove(i, tree1, tree2)
                if p == 0:
                    break
                pts += p
            return pts

        points = 0
        tree2 = s.BST()
        items = [4, 2, 1, 3, 10, 5, 6, 9, 7, 11, 15, 14, 16, 12]

        # Remove from empty tree (1 points).
        try:
            tree2.remove(5)
            self.feedback += "\n\tBST.remove() failed on empty tree"
        except ValueError:
            points += 1

        # Remove leaf (5 points).
        points += remove_many(items, [1, 7, 12, 16, 14])

        # Remove non-root with 1 child (5 points).
        points += remove_many(items, [9, 6, 5, 11, 14])

        # Remove non-root with 2 children (5 points).
        points += remove_many(items, [2, 15, 10, 11, 12])

        # Remove root with one child (5 points).
        points += remove_many([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5])

        # Remove root with two children (5 points).
        points += remove_many([2, 1, 7, 6, 5, 4, 3], [2, 3, 4, 5, 6])

        # Remove root with no children (2 points).
        points += 2*remove_many([10], [10])

        # Remove nonexistent (2 points)
        tree1, tree2 = load_trees(items)

        def error_test(tre, val):
            try:
                tre.remove(val)
                self.feedback += "\nBST.remove({}) failed to raise".format(val)
                self.feedback += " ValueError for {} not in tree".format(val)
                self.feedback += "\n\tPrevious tree:\n{}".format(tree1)
                return 0
            except ValueError:
                return 1

        points += error_test(tree2, 0) + error_test(tree2, 12.5)
        return points

    @_autoclose
    def problem4(self, s):
        """Test prob4(). 10 points."""

        print("Running prob4()...")
        sys.stdout.flush()
        s.prob4()
        return self._grade(10)

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
