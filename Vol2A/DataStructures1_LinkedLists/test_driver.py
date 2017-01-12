# test_driver.py
"""Volume 2A: Data Structures 1 (Linked Lists). Test Driver."""

import sys
sys.path.insert(1, "../..")
from base_test_driver import BaseTestDriver, _timeout

from os import remove as rm
from collections import deque
from numpy.random import permutation, randint


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1: Node class restrictions
     5 points for problem 2: LinkedList.find()
    10 points for problem 3: LinkedList.__len__(), LinkedList.__str__()
    10 points for problem 4: LinkedList.remove()
    10 points for problem 5: LinkedList.insert()
    10 points for problem 6: Deque class
    10 points for problem 7: prob7()

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """

    # File to pull info from for testing problem 7.
    data_file = "english.txt"

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.total = 60
        self.problems = [   (self.problem1, "Problem 1",  5),
                            (self.problem2, "Problem 2",  5),
                            (self.problem3, "Problem 3", 10),
                            (self.problem4, "Problem 4", 10),
                            (self.problem5, "Problem 5", 10),
                            (self.problem6, "Problem 6", 10),
                            (self.problem7, "Problem 7", 10)    ]

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

         5 points for problem 1: Node class restrictions
         5 points for problem 2: LinkedList.find()
        10 points for problem 3: LinkedList.__len__(), LinkedList.__str__()
        10 points for problem 4: LinkedList.remove()
        10 points for problem 5: LinkedList.insert()
        10 points for problem 6: Deque class
        10 points for problem 7: prob7()

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _load_lists(s, list_type="LinkedList"):
        """Construct a random list of 5 to 10 unique integers. Fill a
        student LinkedList with the same entries, then return the lists.
        """
        int_list = [int(i) for i in randint(1,100,randint(5, 10))]
        key_list = [i for i in int_list if int_list.count(i)==1]
        if len(key_list) < 5:
            return TestDriver._load_lists(s, list_type)
        if list_type == "LinkedList":
            student_list = s.LinkedList()
        elif list_type == "Deque":
            student_list = s.Deque()
        for item in key_list:
            student_list.append(item)
        return key_list, student_list

    # Problems ----------------------------------------------------------------
    @_timeout(5)
    def problem1(self, s):
        """Test the Node class for input restrictions. 5 points."""

        def test_Node(item):
            """Attempt to instantiate a Node containing 'item'."""
            try:
                s.Node(item)                    # Should raise a TypeError
                self.feedback += "Node class failed to raise a TypeError "
                self.feedback += "with data of type {}".format(type(item))
            except TypeError:
                return 1
            except Exception as e:
                self.feedback += "\nNode.__init__() failed (expected TypeError"
                self.feedback += ", (got {} instead)".format(self._objType(e))
            return 0

        # Test that anyting other than int, long, float, or str are rejected.
        points  = test_Node(["This", "is", "a", "list"])
        points += test_Node({"This", "is", "a", "set"})
        points += test_Node(3+2j)

        # Test that int, long, float, and str are still accepted.
        s.Node("string")
        s.Node(0)
        return points + 2

    @_timeout(5)
    def problem2(self, s):
        """Test LinkedList.find(). 5 points."""
        source, _list = self._load_lists(s)

        def search_list(node, index):
            """Search '_list' for 'node', which contains source[index]."""
            assert node.value == source[index], "TEST DRIVER ERR 1"
            return self._isTest(node, _list.find(source[index]),
                "LinkedList.find() failed to locate {} in {}".format(
                                                    source[index], source))

        # Test LinkedList.find() with valid inputs (3 points).
        points  = search_list(_list.head, 0)                    # head
        points += search_list(_list.head.next.next, 2)          # middle
        points += search_list(_list.tail, -1)                   # tail

        # Test LinkedList.find() with invalid inputs (2 points).
        def test_not_found(_list_, info):
            try:
                _list_.find(-1)                     # Should raise a ValueError
                self.feedback += "\nLinkedList.find(x) failed {} ".format(info)
                self.feedback += "(failed to raise a ValueError)"
            except ValueError:
                return 1
            except Exception as e:
                self.feedback += "\nLinkedList.find(x) failed {} ".format(info)
                self.feedback += "(expected ValueError, (got {} instead)".format(self._objType(e))
            return 0

        l1, l2 = self._load_lists(s)
        points += test_not_found(l2, "for x not in the list")
        l2 = s.LinkedList()
        points += test_not_found(l2, "for empty list")

        return points

    @_timeout(5)
    def problem3(self, s):
        """Test LinkedList.__len__() and LinkedList.__str__(). 10 Points."""

        # LinkedList.__len__() (4 points) --------------------------------

        # Empty list
        l1 = [int(i) for i in randint(1, 60, randint(5, 10))]
        l2 = s.LinkedList()
        points  = self._eqTest(0, len(l2),
                    "LinkedList.__len__() failed on list {}".format(l1[:0]))

        # Single item
        l2.append(l1[0])
        points += self._eqTest(1, len(l2),
                    "LinkedList.__len__() failed on list {}".format(l1[:1]))

        # Two items
        l2.append(l1[1])
        points += self._eqTest(2, len(l2),
                    "LinkedList.__len__() failed on list {}".format(l1[:2]))

        # Many items
        for i in l1[2:]:
            l2.append(i)
        points += self._eqTest(len(l1), len(l2),
                    "LinkedList.__len__() failed on list {}".format(l1))

        # LinkedList.__str__() (6 points) --------------------------------

        # Empty list
        l1 = [int(i) for i in randint(1, 60, randint(5, 10))]
        l2 = s.LinkedList()
        points += self._strTest(l1[:0], l2, "LinkedList.__str__() failed")

        # Single item (int)
        l2.append(l1[0])
        points += self._strTest(l1[:1], l2, "LinkedList.__str__() failed")

        # Two items (int)
        l2.append(l1[1])
        points += self._strTest(l1[:2], l2, "LinkedList.__str__() failed")

        # Many items (int)
        for i in l1[2:]:
            l2.append(i)
        points += self._strTest(l1, l2, "LinkedList.__str__() failed")

        # Single item (str)
        l1 = [str(i) for i in permutation(["a", "b", "c", "d", "e", "f"])]
        l2 = s.LinkedList()
        l2.append(l1[0])
        points += self._strTest(l1[:1], l2, "LinkedList.__str__() failed")

        # Many items (str)
        for i in l1[1:]:
            l2.append(i)
        points += self._strTest(l1, l2, "LinkedList.__str__() failed")

        return points

    @_timeout(5)
    def problem4(self, s):
        """Test LinkedList.remove(). 10 points."""
        points = 0

        def test_remove(item, solList, stuList):
            """Attempt to remove 'item' from the solution and student lists."""
            old = "\n\tPrevious list:    {}".format(solList)
            p = 1
            try:
                solList.remove(item); stuList.remove(item)
                if 0 == self._strTest(solList, stuList,
                    "LinkedList.remove({}) failed{}".format(item, old)):
                    p = 0
                elif 0 == self._eqTest(len(solList), len(stuList),
                    "LinkedList.__len__() failed on list {}".format(solList)):
                    p = 0
            except Exception as e:
                self.feedback += "\n{} while removing {}: {}{}".format(
                                            self._objType(e), item, e, old)
            finally:
                return p, solList, stuList

        def remove_many(indices):
            """Remove the entries at 'indices' until a problem arises."""
            pts = 0
            l1, l2 = self._load_lists(s)
            for i in indices:
                p, l1, l2 = test_remove(l1[i], l1, l2)
                pts += p
                if p == 0:
                    return pts
            return pts

        # Make sure LinkedList.append() still works.
        l1, l2 = self._load_lists(s)
        if 0 == self._strTest(l1, l2, "LinkedList.append() failed!!"):
            raise NotImplementedError("Ungradable until LinkedList.append()"
                                            " and LinkedList.__str__() work")

        # Remove head, tail (4 points, 2 rounds of 2 points each)
        points += remove_many([0,-1])
        points += remove_many([0,-1])

        # Remove from middle (4 points, 2 rounds of 2 points each)
        points += remove_many([1,2])
        points += remove_many([1,2])

        # Remove only value (2 points)
        for i in xrange(2):
            l1 = [randint(20)]
            l2 = s.LinkedList()
            l2.append(l1[0])
            p, l1, l2 = test_remove(l1[0], l1, l2)
            points += p

        return points

    @_timeout(5)
    def problem5(self, s):
        """Test LinkedList.insert(). 10 points."""
        points = 0

        def test_insert(item, place, solList, stuList):
            """Attempt to insert 'item' to the solution and student lists at
            location 'place'.
            """
            p = 1
            old = "\n\tPrevious list:    {}".format(solList)
            try:
                index = solList.index(place)
                solList.insert(index, item); stuList.insert(item, place)
                if 0 == self._strTest(solList, stuList,
                    "LinkedList.insert({}, {}) failed{}".format(
                                                        item, place, old)):
                    p = 0
                elif 0 == self._eqTest(len(solList), len(stuList),
                    "LinkedList.__len__() failed on list {}".format(solList)):
                    p = 0
            except Exception as e:
                self.feedback += "\n{} while inserting {}: {}{}".format(
                                            self._objType(e), item, e, old)
            finally:
                return p, solList, stuList

        def insert_many(indices):
            """Insert entris at 'indices' until a problem arises."""
            pts = 0
            l1, l2 = self._load_lists(s)
            for i,j in indices:
                p, l1, l2 = test_insert(i, l1[j], l1, l2)
                pts += p
                if p == 0:
                    return pts
            return pts

        # Make sure LinkedList.append() still works.
        l1, l2 = self._load_lists(s)
        if 0 == self._strTest(l1, l2, "LinkedList.append() failed!!"):
            raise NotImplementedError("Ungradable until LinkedList.append()"
                                            " and LinkedList.__str__() work")

        # Insert before head (2 points).
        points += insert_many([(-1,0), (-2,0)])

        # Insert to middle (8 points).
        points += insert_many([(-2,1), (-1,3)])
        points += insert_many([(-2,1), (-1,3)])
        points += insert_many([(-2,1), (-1,3)])
        points += insert_many([(-2,1), (-1,3)])

        return points

    @_timeout(5)
    def problem6(self, s):
        """Test the Deque class. 10 points."""
        if not issubclass(s.Deque, s.LinkedList):
            raise NotImplementedError("Deque must inherit from LinkedList!")
        points = 0

        def test_disabled(func):
            l2 = s.Deque()
            try:
                eval("l2.{}('x','k','c',_='d')".format(func))
                self.feedback += "\nDeque.{}() not disabled ".format(func)
                self.feedback += "correctly (no exception raised)"
            except NotImplementedError:
                return 1
            except Exception as e:
                self.feedback += "\nDeque.{}() not disabled ".format(func)
                self.feedback += "correctly\n\t(expected NotImplementedError, "
                self.feedback += "got {} instead)".format(self._objType(e))
                self.feedback += "\n\tError message: {}".format(e)
            return 0

        def test_append(item, solDeque, stuDeque, func="append"):
            old = "\n\tPrevious deque:   {}".format(list(solDeque))
            p = 1
            try:
                eval("solDeque.{}(item)".format(func))
                eval("stuDeque.{}(item)".format(func))
                if 0 == self._strTest(list(solDeque), stuDeque,
                    "Deque.{}({}) failed{}".format(func, item, old)):
                    p = 0
            except Exception as e:
                self.feedback += "\n{} while {}ing {}: {}{}".format(
                                        self._objType(e), func, item, e, old)
            finally:
                return p, solDeque, stuDeque

        def test_pop(solDeque, stuDeque, func="pop"):
            old = "\n\tPrevious deque:   {}".format(list(solDeque))
            p = 1
            try:
                eval("solDeque.{}()".format(func))
                eval("stuDeque.{}()".format(func))
                if 0 == self._strTest(list(solDeque), stuDeque,
                    "Deque.{}() failed{}".format(func, old)):
                    p = 0
            except Exception as e:
                self.feedback += "\n{} while {}ing: {}{}".format(
                                        self._objType(e), func, e, old)
            finally:
                return p, solDeque, stuDeque

        def append_many(func):
            items = self._load_lists(s)[0]
            l1 = deque()
            l2 = s.Deque()
            pts = 0
            for i in items:
                p, l1, l2 = test_append(i, l1, l2, func)
                pts += p
                if p == 0:
                    break
            return pts == len(items)

        def pop_many(func):
            l1, l2 = self._load_lists(s, list_type="Deque")
            num_items = len(l1)
            l1 = deque(l1)
            pts = 0
            for _ in xrange(num_items):
                p, l1, l2 = test_pop(l1, l2, func)
                pts += p
                if p == 0:
                    break
            return pts == num_items

        # Test that Deque.remove() and Deque.insert() are disabled (2 points).
        points += test_disabled("remove")
        points += test_disabled("insert")

        # Test Deque.append() and Deque.appendleft() (2 points each).
        points += 2*append_many("append")
        points += 2*append_many("appendleft")

        # Test Deque.pop() and Deque.popleft() (2 points each).
        points += 2*pop_many("pop")
        points += 2*pop_many("popleft")

        return points

    @_timeout(5)
    def problem7(self, s):
        """Test prob7(), the file reversal problem."""

        # Get a subset of the data to work with
        with open(self.data_file, 'r') as f:
            data = f.readlines()
        words = [str(i) for i in permutation(data)[:10]]
        with open("__temp__.txt", 'w') as f:
            f.writelines(words)

        # Run the student's function and test the results.
        s.prob7(infile='__temp__.txt', outfile='__ans__.txt')
        with open('__ans__.txt', 'r') as f:
            data = f.readlines()
        rm("__temp__.txt"); rm("__ans__.txt")
        good = '\n'+"\n".join([i.rstrip('\n') for i in list(reversed(words))])
        student = '\n'+"\n".join([i.rstrip('\n') for i in data])
        return 10*self._strTest(good, student,
                                "prob7() failed\n\tOriginal file:\n" +
                                "\n".join([i.rstrip('\n') for i in words]))

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
