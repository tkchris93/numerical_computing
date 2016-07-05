# solutions.py
"""Volume II Lab 4: Data Structures 1 (Linked Lists). Solutions file."""


# Problem 1: Modify the constructor of the Node class.
class Node(object):
    """A basic node class for storing data."""
    def __init__(self, data):
        """Store 'data' in the 'value' attribute.

        Raises:
            TypeError: if 'data' is not of type int, long, float, or str.
        """
        if type(data) not in {int, long, float, str}:
            raise TypeError("Invalid data type: {}".format(type(data)))
        self.value = data


class LinkedListNode(Node):
    """A node class for doubly-linked lists. Inherits from the 'Node' class.
    Contains references to the next and previous nodes in the linked list.
    """
    def __init__(self, data):
        """Store 'data' in the 'value' attribute and initialize
        attributes for the next and previous nodes in the list.
        """
        Node.__init__(self, data)       # Use inheritance to set self.value.
        self.next = None
        self.prev = None


class LinkedList(object):
    """Doubly-linked list data structure class.

    Attributes:
        head (LinkedListNode): the first node in the list.
        tail (LinkedListNode): the last node in the list.
    """
    def __init__(self):
        """Initialize the 'head' and 'tail' attributes by setting
        them to 'None', since the list is empty initially.
        """
        self.head = None
        self.tail = None
        self._size = 0                              # for __len__()

    def append(self, data):
        """Append a new node containing 'data' to the end of the list."""
        # Create a new node to store the input data.
        new_node = LinkedListNode(data)
        if self.head is None:
            # If the list is empty, assign the head and tail attributes to
            # new_node, since it becomes the first and last node in the list.
            self.head = new_node
            self.tail = new_node
        else:
            # If the list is not empty, place new_node after the tail.
            self.tail.next = new_node               # tail --> new_node
            new_node.prev = self.tail               # tail <-- new_node
            # Now the last node in the list is new_node, so reassign the tail.
            self.tail = new_node
        self._size += 1                             # for __len__()

    # Problem 2
    def find(self, data):
        """Return the first node in the list containing 'data'.
        If no such node exists, raise a ValueError.
        """
        current = self.head                 # Start at the head.
        while current is not None:          # Iterate through each node.
            if current.value == data:       # Check for the data.
                return current              # Return node if found; if not
            current = current.next          #  found, raise a ValueError.
        raise ValueError("{} is not in the list".format(data))

    # Problem 3
    def __len__(self):
        """Return the number of nodes in the list."""
        return self._size

    # Problem 3
    def __str__(self):
        """String representation: the same as a standard Python list."""
        # List construction method (recommended).
        current = self.head
        items = []
        while current is not None:
            items.append(current.value)
            current = current.next
        return str(items)

        # String construction method.
        current = self.head
        out = "["
        while current is not None:
            if isinstance(current.value, str):
                item = "'" + str(current.value) + "'"
            else:
                item = str(current.value)
            out += item
            current = current.next
            if current is not None:
                out += ", "
        out += "]"
        return out

    # Problem 4: Write LinkedList.remove().
    def remove(self, data):
        """Remove the first node in the list containing 'data'. Return nothing.

        Raises:
            ValueError: if the list is empty, or does not contain 'data'.
        """
        target = self.find(data)            # Raise the ValueError if needed.
        if self.head is self.tail:          # Case 1: remove only node.
            self.head = None                    # reassign the head.
            self.tail = None                    # reassign the tail.
        elif target is self.head:           # Case 1: remove the head.
            self.head = self.head.next          # reassign the head.
            self.head.prev = None               # target <-/- head
        elif target is self.tail:           # Case 2: remove the tail.
            self.tail = self.tail.prev          # reassign the tail.
            self.tail.next = None               # tail -/-> target
        else:                               # Case 3: remove from middle.
            target.prev.next = target.next      # -/-> target
            target.next.prev = target.prev      # target <-/-
        self._size -= 1                     # for __len__()

    # Problem 5
    def insert(self, data, place):
        """Insert a node containing 'data' immediately before the first node
        in the list containing 'place'. Return nothing.

        Raises:
            ValueError: if the list is empty, or does not contain 'place'.
        """
        after = self.find(place)            # Raise the ValueError if needed.
        new_node = LinkedListNode(data)      # Make the new node.
        if after is self.head:              # Case 1: insert before the head.
            new_node.next = self.head           # new --> head
            self.head.prev = new_node           # new <-- head
            self.head = new_node                # reassign the head.
        else:                               # Case 2: insert to middle.
            after.prev.next = new_node          # before --> new
            new_node.prev = after.prev          # before <-- new
            new_node.next = after               # new --> after
            after.prev = new_node               # new <-- after
        self._size += 1                     # for __len__()


# Problem 6
class Deque(LinkedList):
    """Deque doubly-linked list data structure class.

    Attributes:
        head (LinkedListNode): the first node in the list.
        tail (LinkedListNode): the last node in the list.
    """
    def pop(self):
        """Remove the last node in the list and return its value."""
        if self.tail is None:               # Case 1: Empty list.
            raise ValueError("The list is empty")
        else:                               # Case 2: Nonempty list.
            data = self.tail.value
            LinkedList.remove(self, data)
            return data

    def popleft(self):
        """Remove the first node in the list and return its value."""
        if self.head is None:               # Case 1: Empty list.
            raise ValueError("The list is empty")
        else:                               # Case 2: Nonempty list.
            data = self.head.value
            LinkedList.remove(self, data)
            return data

    def appendleft(self, data):
        """Place a new node containing 'data' at the beginning of the list."""
        if self.head is None:               # Case 1: Empty list.
            LinkedList.append(self, data)
        else:                               # Case 2: Nonempty list.
            LinkedList.insert(self, data, self.head.value)

    def remove(*args, **kwargs):
        raise NotImplementedError("Use pop() or popleft() for removal")

    def insert(*args, **kwargs):
        raise NotImplementedError("Use append() or appendleft() for insertion")


# Problem 7
def prob7(infile, outfile):
    """Reverse the file 'infile' by line and write the results to 'outfile'."""
    with open(infile, 'r') as f:            # Read the lines in as a list.
        lines = f.readlines()
    deque = Deque()                         # Instantiate a deque.
    for line in lines:                      # Add each line to the deque.
        deque.append(line)
    with open(outfile, 'w') as f:           # Write to the outfile in reverse.
        while deque.head is not None:
            f.write(str(deque.pop()))


# Additional Material =========================================================

class SortedList(LinkedList):
    """Sorted doubly-linked list data structure class.
    Inherits from the 'LinkedList' class.

    Attributes:
        head (LinkedListNode): the first node in the list.
        tail (LinkedListNode): the last node in the list.
    """

    def add(self, data):
        """Create a new Node containing 'data' and insert it at the
        appropriate location to preserve list sorting.
        """
        if self.head is None:               # Case 1: Empty list.
            LinkedList.append(self, data)
        elif self.tail.value <= data:       # Case 2: Append after the tail.
            LinkedList.append(self, data)
        else:                               # Case 3: Insert to middle.
            current = self.head
            while current.value < data:         # Find insertion location.
                current = current.next
            LinkedList.insert(self, data, current.value)

    def append(*args, **kwargs):
        raise NotImplementedError("append() is disabled (use add())")

    def insert(*args, **kwargs):
        raise NotImplementedError("insert() is disabled (use add())")

# END OF SOLUTIONS ========================================================== #

from os import remove as rm
from numpy.random import permutation, randint

def test(student_module):
    """Test script. You must import the student's 'solutions.py' as a module.

     5 points for problem 1: Node class restrictions
     5 points for problem 2: LinkedList.find()
    10 points for problem 3: LinkedList.__len__(), LinkedList.__str__()
    10 points for problem 4: LinkedList.remove()
    10 points for problem 5: LinkedList.insert()
    15 points for problem 6: SortedList, sort_file()
    15 points for problem 7: Deque, reverse_file()

    Inputs:
        student_module: the imported module for the student's file.
        late (bool): if True, half credit is awarded.

    Returns:
        score (int): the student's score, out of 70.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback


class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""

    # File to pull info from for testing problems 6 and 7.
    data_file = "English.txt"

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine -----------------------------------------------------------
    def test_all(self, student_module, total=70):
        """Grade the provided module on each problem and compile feedback."""
        # Reset feedback and score.
        self.feedback = ""
        self.score = 0

        def test_one(problem, number, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\nProblem {} ({} points):".format(
                                                                number, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += {}".format(points)
            except BaseException as e:
                self.feedback += "\n{}: {}".format(self._errType(e),e)

        # Grade each problem.
        test_one(self.problem1, 1, 5)   # Problem 1:  5 points.
        test_one(self.problem2, 2, 5)   # Problem 2:  5 points.
        test_one(self.problem3, 3, 10)  # Problem 3: 10 points.
        test_one(self.problem4, 4, 10)  # Problem 4: 10 points.
        test_one(self.problem5, 5, 10)  # Problem 5: 10 points.
        test_one(self.problem6, 6, 15)  # Problem 6: 15 points.
        test_one(self.problem7, 7, 15)  # Problem 7: 15 points.

        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: {}/{} = {}%".format(
                                    self.score, total, round(percentage, 2))
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t{}'.format(comments)

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        if isinstance(error, BaseException):
            return str(type(error)).lstrip("<type 'exceptions.").rstrip("'>")
        else:
            return str(error)

    @staticmethod
    def _load_lists(s, list_type="LinkedList"):
        """Construct a random list of 5 to 10 unique integers. Fill a
        student LinkedList with the same entries, then return the lists.
        """
        int_list = [int(i) for i in randint(1,100,randint(5, 10))]
        driver_list = [i for i in int_list if int_list.count(i)==1]
        if len(driver_list) < 5:
            return _testDriver._load_lists(s, list_type)
        if list_type == "SortedList":
            student_list = s.SortedList()
            for item in driver_list:
                student_list.add(item)
        else:
            if list_type == "Deque":
                student_list = s.Deque()
            else:
                student_list = s.LinkedList()
            for item in driver_list:
                student_list.append(item)
        return driver_list, student_list

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' have the same
        numerical value. Report the given 'message' if they are not.
        """
        if correct == student:
            return 1
        else:
            self.feedback += "\n{}".format(message)
            self.feedback += "\n\tCorrect response: {}".format(correct)
            self.feedback += "\n\tStudent response: {}".format(student)
            return 0

    def _isTest(self, correct, student, message):
        """Test to see if the nodes 'correct' and 'student' are the same
        object. Report the given 'message' if they are not.
        """
        if correct is student:
            return 1
        else:
            self.feedback += "\n{}".format(message)
            self.feedback += "\n\tCorrect response: {}".format(correct.value)
            self.feedback += "\n\tStudent response: {}".format(student.value)
            return 0

    def _strTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' have the same string
        representation. Report the given 'message' if they are not.
        """
        if str(correct) == str(student):
            return 1
        else:
            self.feedback += "\n{}".format(message)
            self.feedback += "\n\tCorrect response: {}".format(correct)
            self.feedback += "\n\tStudent response: {}".format(student)
            return 0

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score."""
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of {}: ".format(points)))
            except:
                credit = -1
        if credit != points:
            # Add comments (optionally),
            comments = raw_input("Comments: ")
            if len(comments) > 0:
                self.feedback += "\n{}".format(comments)
            # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n{}".format(message)
        return credit

    # Problems ----------------------------------------------------------------
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
                self.feedback += "\nNode.__init__ failed (expected TypeError, "
                self.feedback += "(got {} instead)".format(self._errType(e))
            return 0

        # Test that anyting other than int, long, float, or str are rejected.
        points  = test_Node(["This", "is", "a", "list"])
        points += test_Node({"This", "is", "a", "set"})
        points += test_Node(3+2j)

        # Test that int, long, float, and str are still accepted.
        s.Node("string"); s.Node(0)
        return points + 2

    def problem2(self, s):
        """Test LinkedList.find(). 5 points."""
        if not hasattr(s.LinkedList, "find"):
            raise NotImplementedError("Problem 2 Incomplete")

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
                self.feedback += "(expected ValueError, (got {} instead)".format(self._errType(e))
            return 0

        l1, l2 = self._load_lists(s)
        points += test_not_found(l2, "for x not in the list")
        l2 = LinkedList()
        points += test_not_found(l2, "for empty list")

        return points

    def problem3(self, s):
        """Test LinkedList.__len__() and LinkedList.__str__(). 10 Points."""
        if not hasattr(s.LinkedList, "__len__"):
            raise NotImplementedError("Problem 3 Incomplete")

        # Test LinkedList.__len__() (4 points) --------------------------------

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

        # Test LinkedList.__str__() (6 points) --------------------------------

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

    def problem4(self, s):
        """Test LinkedList.remove(). 10 points."""
        if not hasattr(s.LinkedList, "remove"):
            raise NotImplementedError("Problem 4 Incomplete")
        points = 0

        def test_remove(item, solList, stuList):
            """Attempt to remove 'item' from the solution and student lists.
            Report then pass along any formal Exceptions.
            """
            old = "\nPrevious list: {}\n".format(solList)
            try:
                solList.remove(item); stuList.remove(item)
                if 0 == self._strTest(solList, stuList,
                    "LinkedList.remove({}) failed{}".format(item, old)):
                    raise AssertionError("Incorrect list")
                elif 0 == self._eqTest(len(solList), len(stuList),
                    "LinkeList.__len__() failed on list {}".format(solList)):
                    return 0, solList, stuList
                else:
                    return 1, solList, stuList
            except AssertionError:
                raise
            except Exception as e:
                self.feedback += "\n{} while removing {}: {}{}".format(
                                            self._errType(e), item, e, old)
                raise

        # Make sure LinkedList.append() still works.
        l1, l2 = self._load_lists(s)
        if 0 == self._strTest(l1, l2, "LinkedList.append() failed!!"):
            raise AssertionError("Ungradable until LinkedList.append() works")

        # Remove head, tail (4 points, 2 rounds of 2 points each)
        for i in xrange(2):
            l1, l2 = self._load_lists(s)
            try:
                p, l1, l2 = test_remove(l1[0],  l1, l2); points += p # head
                p, l1, l2 = test_remove(l1[-1], l1, l2); points += p # tail
            except: pass

        # Remove from middle (4 points)
        for i in xrange(2):
            l1, l2 = self._load_lists(s)
            try:
                p, l1, l2 = test_remove(l1[1], l1, l2); points += p
                p, l1, l2 = test_remove(l1[2], l1, l2); points += p
            except: pass

        # Remove only value (2 points)
        for i in xrange(2):
            l1 = [randint(20)]
            l2 = s.LinkedList()
            l2.append(l1[0])
            try:
                p, l1, l2 = test_remove(l1[0], l1, l2); points += p
            except: pass

        return points

    def problem5(self, s):
        """Test LinkedList.insert(). 10 points."""
        if not hasattr(s.LinkedList, "insert"):
            raise NotImplementedError("Problem 5 Incomplete")
        points = 0

        def test_insert(item, place, solList, stuList):
            """Attempt to insert 'item' to the solution and student lists at
            location 'place'. Report then pass along any formal Exceptions.
            """
            old = "\nPrevious list: {}\n".format(solList)
            try:
                index = solList.index(place)
                solList.insert(index, item); stuList.insert(item, place)
                if 0 == self._strTest(solList, stuList,
                    "LinkedList.insert({}, {}) failed{}".format(
                                                        item, place, old)):
                    raise AssertionError("Incorrect list")
                elif 0 == self._eqTest(len(solList), len(stuList),
                    "LinkeList.__len__() failed on list {}".format(solList)):
                    return 0, solList, stuList
                else:
                    return 1, solList, stuList
            except AssertionError:
                raise
            except Exception as e:
                self.feedback += "\n{} while inserting {}: {}{}".format(
                                            self._errType(e), item, e, old)
                raise

        # Make sure LinkedList.append() still works.
        l1, l2 = self._load_lists(s)
        if 0 == self._strTest(l1, l2, "LinkedList.append() failed!!"):
            raise AssertionError("Ungradable until LinkedList.append() works")

        # Insert before head (2 points)
        l1, l2 = self._load_lists(s)
        try:
            p, l1, l2 = test_insert(-1, l1[0], l1, l2); points += p
            p, l1, l2 = test_insert(-2, l1[0], l1, l2); points += p
        except: pass

        # Insert to middle (8 points)
        for i in xrange(4):
            l1, l2 = self._load_lists(s)
            try:
                p, l1, l2 = test_insert(-2, l1[1], l1, l2); points += p
                p, l1, l2 = test_insert(-1, l1[3], l1, l2); points += p
            except: pass

        return points

    def problem6(self, s):
        """Test the SortedList class and sort_file(). 15 points."""
        if not hasattr(s, "SortedList") or not hasattr(s, "sort_file"):
            raise NotImplementedError("Problem 6 Incomplete")
        if not issubclass(s.SortedList, s.LinkedList):
            raise AssertionError("SortedList must inherit from LinkedList!")
        points = 0

        def test_disabled(func):
            l2 = SortedList()
            try:
                statement = "l2.{}('a','b','c',_='d')".format(func)
                eval(statement)
                self.feedback += "\nSortedList.{}() not disabled ".format(func)
                self.feedback += "correctly (no exception raised)"
            except NotImplementedError:
                return 1
            except Exception as e:
                self.feedback += "\nSortedList.{}() not disabled ".format(func)
                self.feedback += "correctly (expected NotImplementedError, "
                self.feedback += "got {} instead)".format(self._errType(e))
                self.feedback += "\n\tError message: {}".format(e)
            return 0

        # Test that SortedList.append() and SortedList.insert() are disabled
        # (2 points)
        points += test_disabled("append")
        points += test_disabled("insert")

        # Test SortedList.add() (8 points)
        for i in xrange(8):
            l1, l2 = self._load_lists(s, "SortedList")
            points += self._strTest(sorted(l1), l2, "SortedList.add() failed")

        # Test sort_file() (5 points) -----------------------------------------
        # Get a subset of the data to work with
        with open(self.data_file, 'r') as f:
            data = f.read().split('\n')
            while data[-1] == '': data.pop()
        words = [str(i) for i in permutation(data)[::20]]
        with open("__temp__.txt", 'w') as f:
            for word in words:
                f.write(word + "\n")

        # Run the student's function and test the results.
        s.sort_file(infile='__temp__.txt', outfile='__ans__.txt')
        with open('__ans__.txt', 'r') as f:
            data = f.read().split('\n')
            while data[-1] == '': data.pop()
        points += 5*self._strTest(sorted(words), data, "sort_file() failed")
        rm("__temp__.txt"); rm("__ans__.txt")

        return points

    def problem7(self, s):
        """Test the Deque class and the reverse_file() function. 15 points."""
        if not hasattr(s, "Deque") or not hasattr(s, "reverse_file"):
            raise NotImplementedError("Problem 7 Incomplete")
        if not issubclass(s.Deque, s.LinkedList):
            raise AssertionError("Deque must inherit from LinkedList!")
        points = 0

        def test_disabled(func):
            l2 = Deque()
            try:
                statement = "l2.{}('a','b','c',_='d')".format(func)
                eval(statement)
                self.feedback += "\nDeque.{}() not disabled ".format(func)
                self.feedback += "correctly (no exception raised)"
            except NotImplementedError:
                return 1
            except Exception as e:
                self.feedback += "\nDeque.{}() not disabled ".format(func)
                self.feedback += "correctly (expected NotImplementedError, "
                self.feedback += "got {} instead)".format(self._errType(e))
                self.feedback += "\n\tError message: {}".format(e)
            return 0

        # Test that Deque.remove() and Deque.insert() are disabled (2 points)
        points += test_disabled("remove")
        points += test_disabled("insert")

        # TODO: Test Deque.append(), appendleft(), pop(), and popleft() (8 pts)

        # Test Deque.append() (2 points)
        l1, l2 = self._load_lists(s, list_type="Deque")
        points += 2*self._strTest(l1, l2, "Deque.append() failed")

        # Test Deque.appendleft() (2 points)
        l1 = [int(i) for i in randint(1, 60, randint(5, 10))]
        l2 = s.Deque()
        for i in l1:
            l2.appendleft(i)
        l1.reverse()
        points += 2*self._strTest(l1, l2, "Deque.appendleft() failed")

        # Test Deque.pop() (2 points)
        l1, l2 = self._load_lists(s, list_type="Deque")
        pops = []
        while len(l2) != 0:
            pops.append(l2.pop())
        l1.reverse()
        points += 2*self._strTest(l1, pops,
                "Deque.pop() failed (showing sequence of pops)")

        # Test Deque.popleft() (2 points)
        l1, l2 = self._load_lists(s, list_type="Deque")
        pops = []
        while len(l2) != 0:
            pops.append(l2.popleft())
        points += 2*self._strTest(l1, pops,
                "Deque.popleft() failed (showing sequence of poplefts)")

        # Test reverse_file() (5 points) --------------------------------------
        # Get a subset of the data to work with
        with open(self.data_file, 'r') as f:
            data = f.read().split('\n')
            while data[-1] == '': data.pop()
        words = [str(i) for i in permutation(data)[::30]]
        with open("__temp__.txt", 'w') as f:
            for word in words:
                f.write(word + "\n")

        # Run the student's function and test the results.
        s.reverse_file(infile='__temp__.txt', outfile='__ans__.txt')
        with open('__ans__.txt', 'r') as f:
            data = f.read().split('\n')
            while data[-1] == '': data.pop()
        points += 5*self._strTest(
                        list(reversed(words)), data, "reverse_file() failed")
        rm("__temp__.txt"); rm("__ans__.txt")

        return points

# END OF FILE =================================================================
