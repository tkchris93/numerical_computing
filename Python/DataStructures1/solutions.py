# solutions.py
"""Volume II Lab 4: Data Structures 1 (Linked Lists)
Solutions file. Written by Shane McQuarrie.
"""

# Problem 1: Modify the constructor of the Node class.
class Node(object):
    """A basic node class for storing data."""
    def __init__(self, data):
        """Store 'data' in the 'value' attribute.

        Raises:
            TypeError: if 'data' is not of type int, long, float, or str.
        """
        if type(data) not in {int, long, float, str}:
            raise TypeError("Invalid data type")
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


# Problems 2, 3, 4, 5: Complete the LinkedList class.
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

    # Problem 2: Write LinkedList.find().
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

    # Problem 3: Write LinkedList.__len__() and LinkedList.__str__().
    def __len__(self):
        """Return the number of nodes in the list."""
        return self._size

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
                item = "'{}'".format(current.value)
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
        self._size -= 1

    # Problem 5: Write LinkedList.insert().
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
            after.prev.next = new_node          # --> new
            new_node.prev = after.prev          # <-- new
            new_node.next = after               # new -->
            after.prev = new_node               # new <--
        self._size += 1


# Problem 6: Write a SortedList class and a function called sort_file().
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

def sort_file(infile, outfile):
    """Sort the file 'infile' by line and write the results to 'outfile'."""
    with open(infile, 'r') as f:            # Read the lines in as a list.
        lines = f.readlines()
    sorted_list = SortedList()              # Instantiate a SortedList object.
    for line in lines:                      # Add each line to the SortedList.
        sorted_list.add(line)
    current = sorted_list.head              # Write the sorted lines to the
    with open(outfile, 'w') as f:           #  outfile.
        while current is not None:
            f.write(str(current.value))
            current = current.next


# Problem 7: Write a Deque class and a function called reverse_file().
class Deque(LinkedList):
    """Deque doubly-linked list data structure class.

    Attributes:
        head (LinkedListNode): the first node in the list.
        tail (LinkedListNode): the last node in the list.
    """
    def appendleft(self, data):
        """Place a new node containing 'data' at the beginning of the list."""
        if self.head is None:               # Case 1: Empty list.
            LinkedList.append(self, data)
        else:                               # Case 2: Nonempty list.
            LinkedList.insert(self, data, self.head.value)

    def pop(self):
        """Remove the last node in the list and return its value."""
        if self.tail is None:               # Case 1: Empty list.
            raise ValueError("The list is empty")
        else:                               # Case 2: Nonempty list.
            data = self.tail.value
            LinkedList.remove(self, data)
            return data

    def popleft():
        """Remove the first node in the list and return its value."""
        if self.head is None:               # Case 1: Empty list.
            raise ValueError("The list is empty")
        else:                               # Case 2: Nonempty list.
            data = self.head.value
            LinkedList.remove(self, data)
            return data

    def remove(*args, **kwargs):
        raise NotImplementedError("remove() is disabled")

    def insert(*args, **kwargs):
        raise NotImplementedError("insert() is disabled")

def reverse_file(infile, outfile):
    """Reverse the file 'infile' by line and write the results to 'outfile'."""
    with open(infile, 'r') as f:            # Read the lines in as a list.
        lines = f.readlines()
    deque = Deque()                         # Instantiate a SortedList object.
    for line in lines:                      # Add each line to the SortedList.
        print(repr(line))
        deque.append(line)
    with open(outfile, 'w') as f:           # Write to the outfile in reverse.
        while deque.head is not None:
            f.write(str(deque.pop()))


# END OF SOLUTIONS ========================================================== #

from numpy.random import permutation

def test(student_module):
    """Test script. You must import the student's 'solutions.py' as a module.
    
     5 points for problem 1
     5 points for problem 2
    10 points for problem 3
    10 points for problem 4
    10 points for problem 5
    15 points for problem 6
    15 points for problem 7
    
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


# TODO: UPDATE THIS TEST DRIVER !!!!!!
class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info."""

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
                self.feedback += "\n\nProblem %d (%d points):"%(number, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += %d"%points
            except BaseException as e:
                self.feedback += "\n%s: %s"%(self._errType(e),e)

        # Grade each problem.
        test_one(self.problem1, 1, 0)   # Problem 1:  5 points.
        test_one(self.problem2, 2, 0)   # Problem 2:  5 points.
        test_one(self.problem3, 3, 0)   # Problem 3: 10 points.
        test_one(self.problem4, 4, 0)   # Problem 4: 10 points.
        test_one(self.problem5, 5, 0)   # Problem 5: 10 points.
        test_one(self.problem6, 6, 0)   # Problem 6: 15 points.
        test_one(self.problem7, 7, 0)   # Problem 7: 15 points.

        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: {}/{} = {}%%".format(
                                    self.score, total, percentage)
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t%s'%comments

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        if isinstance(error, BaseException):
            return str(type(error)).lstrip("<type 'exceptions.").rstrip("'>")
        else:
            return str(error)

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
        points = 0
        
        return points

    def problem2(self, s):
        """Test LinkedList.find(). 5 points."""
        points = 0

        return points

    def problem3(self, s):
        """Test LinkedList.__len__() and LinkedList.__str__(). 10 Points."""
        points = 0

        return points
        
        # Test an empty list
        l1 = []; l2 = s.LinkedList()
        points += self.strTest(l1, l2,
                        "\n\tLinkedList.__str__ failed on empty list")
        
        # Single item
        l1.append("This"); l2.add("This")
        points += self.strTest(l1, l2,
                        "\n\tLinkedList.__str__ failed with single item")
        
        # Two items
        l1.append("is"); l2.add("is")
        points += self.strTest(l1, l2,
                        "\n\tLinkedList.__str__ failed with two items")
        
        # Many items
        entries = [1, "Linked List!"]
        for i in entries:
            l1.append(i); l2.add(i)
        points += 2*self.strTest(l1, l2,
                        "\n\tLinkedList.__str__ failed with many items")

        # Round 2
        l1 = []; l2 = s.LinkedList()
        entries = [1, 2.0, ["list"], {"set"}, {"dict":"ionary"}]
        for entry in entries:
            l1.append(entry); l2.add(entry)
        points += 5*self.strTest(l1, l2,
                        "\n\tLinkedList.__str__ failed with many items")
        
        return points

    def problem4(self, s):
        """Test LinkedList.remove(). 10 points."""
        points = 0

        return points

        l1 = []; l2 = s.LinkedList()

        # Test LinkedList.remove() from empty list (2 points)
        print("\nCorrect output:\t100 is not in the list.\nStudent output:\t"),
        try:
            l2.remove(100)
            self.feedback += "\n\tNo exception raised by LinkedList.remove(x)"
            self.feedback += " on empty list"
        except ValueError as e:
            points += 1; print(e.message)
            points += self.grade(1,
                "\n\tLinkedList.remove() failed to report on empty list")

        # Test add() (no credit, but vital for other points)
        for i in [1, 3, 2, 5, 4, 7, 6]:
            l1.append(i); l2.add(i)
        self.strTest(l1, l2,
                "\n\tIf LinkedList.__str__ fails, these tests will all fail!")
        
        # remove() head (1 point)
        l1.remove(1); l2.remove(1)
        points += self.strTest(l1, l2,
                            "\n\tLinkedList.remove() failed on head removal"
                            + "\n\t(original list: [1, 3, 2, 5, 4, 7, 6])")
        
        # remove() end (1 point)
        l1.remove(6); l2.remove(6)
        points += self.strTest(l1, l2,
                            "\n\tLinkedList.remove() failed on tail removal"
                            + "\n\t(original list: [3, 2, 5, 4, 7, 6])")
        
        # remove() from middle (1 point)
        l1.remove(5); l2.remove(5)
        points += self.strTest(l1, l2,
                            "\n\tLinkedList.remove() failed on middle removal"
                            + "\n\t(original list: [3, 2, 5, 4, 7])")
        
        # remove() nonexistent (5 points)
        print("\nCorrect output:\t100 is not in the list.\nStudent output:\t"),
        try:
            l2.remove(100)
            self.feedback += "\n\tNo exception raised by LinkedList.remove(x)"
            self.feedback += " for x not in the list"
        except ValueError as e:
            points += 4; print(e.message)
            points += self.grade(1, "\n\tLinkedList.remove(x) failed to "
                                 + "report for x not in the list")

        return points

    def problem5(self, s):
        """Test LinkedList.insert(). 10 points."""
        points = 0

        return points

        l1, l2 = LinkedList(), s.LinkedList()

        # insert() to empty list (2 points)
        print("\nCorrect output:\t100 is not in the list.\nStudent output:\t"),
        try:
            l2.insert(100,100)
            self.feedback += "\n\tNo exception raised by LinkedList.insert()"
            self.feedback += " on empty list"
        except ValueError as e:
            points += 1; print(e.message)
            points += self.grade(1,
                "\n\tLinkedList.insert(x,y) failed to report on empty list")

        # insert() before head (5 points)
        l1.add(5); l1.insert(2,5)
        l2.add(5); l2.insert(2,5)
        points += 5*self.strTest(l1, l2,
                "\n\tLinkedList.insert() failed on inserting before the head"
                + "\n\t(original list: [5])")
        
        # insert() in the middle (5 points)
        l1.insert(4,5); l2.insert(4,5)
        points += 2*self.strTest(l1, l2,
                "\n\tLinkedList.insert() failed on middle insertion"
                + "\n\t(original list: [2, 5]")
        l1.insert(3,4); l2.insert(3,4)
        points += 3*self.strTest(l1, l2,
                "\n\tLinkedList.insert() failed on middle insertion"
                + "\n\t(original list: [2, 4, 5]")
        
        # insert(data, place) on nonexistant place (3 points)
        print("\nCorrect output:\t100 is not in the list.\nStudent output:\t"),
        try:
            l2.insert(1,100)
            self.feedback += "\n\tNo exception raised by LinkedList.insert(x,"
            self.feedback += "place) for 'place' not in list"
        except ValueError as e:
            points += 2; print(e.message)
            points += self.grade(1, "\n\tLinkedList.insert(x, place)" + 
                                " failed to report for 'place' not in list")
        return points

    def problem6(self, s):
        """Test the SortedList class and sort_file(). 15 points."""
        points = 0

        return points

        # Test add() (2 point)
        l1, l2 = SortedList(), s.SortedList()
        entries = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for entry in entries:
            l1.add(entry); l2.add(entry)
        points += 2*self.strTest(l1, l2, "\n\tSortedList.add() failed"
                    + "\n\t(adding 1, 2, 3, 4, 5, 6, 7, 8, and 9 in order)")

        # Test add() (3 points)
        l1, l2 = SortedList(), s.SortedList()
        entries = [9, 8, 7, 6, 5, 4, 2, 3, 1]
        for entry in entries:
            l1.add(entry); l2.add(entry)
        points += 3*self.strTest(l1, l2, "\n\tSortedList.add() failed"
                    + "\n\t(adding 9, 8, 7, 6, 5, 4, 2, 3, and 1 in order)")

        # Test add() (3 points)
        l1, l2 = SortedList(), s.SortedList()
        entries = [1, 3, 5, 7, 9, 2, 4, 6, 8]
        for entry in entries:
            l1.add(entry); l2.add(entry)
        points += 3*self.strTest(l1, l2, "\n\tSortedList.add() failed"
                    + "\n\t(adding 1, 3, 5, 7, 9, 2, 4, 6, and 8 in order)")

        # Test that insert() was disabled (2 point)
        print("\nCorrect output:\tinsert() has been disabled for this class.")
        print("Student output:\t"),
        try:
            l2.insert(1, 2, 3, 4, 5)
            self.feedback += "\n\tNo exception raised by SortedList.insert()"
        except (ValueError, NotImplementedError) as e: # NotImplementedError
            points += 1; print(e.message)
            points += self.grade(1, "\n\tSortedList.insert()" + 
                                " failed to report as disabled")
        except TypeError:
            self.feedback += "\n\tSortedList.insert() not disabled correctly"
            self.feedback +="\n\t\t(insert() should accept any number of arguments)"

        # Test sort_words() (10 points)
        with open("English.txt", 'r') as f:
            stuff = f.read().split('\n')
            if stuff[-1] == '\n': stuff.pop()
        words = list(permutation(stuff))[::20]
        with open("Short.txt", 'w') as f:
            for word in words:
                f.write(word + '\n')

        word_list = create_word_list("Short.txt")
        word_list.sort()
        out = s.sort_words("Short.txt")
        points += 10*self.strTest(word_list, out, "\n\tsort_words() failed.")

        # detect cheating
        if not isinstance(out, s.SortedList):
            points = 0
            self.feedback += "\n\tsort_words() must return a "
            self.feedback += "SortedList object!"
        if not issubclass(s.SortedList, s.LinkedList):
            points = 0
            self.feedback += "\n\tThe SortedList class must inherit "
            self.feedback += "from the LinkedList class!"

        return points        


    def problem7(self, s):
        """Test the Deque class and the reverse_file() function. 15 points."""
        return 0
