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

    # Constructor / main routine ----------------------------------------------
    def __init__(self):
        self.feedback = ""

    def test_all(self, student_module):
        """Grade each problem in sequence and compile feedback."""
        self.feedback = ""
        score = 0

        try:    # Problem 1: 5 points
            points = self.problem1(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 2: 10 points
            points = self.problem2(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 3: 10 points
            points = self.problem3(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 4: 15 points
            points = self.problem4(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 5: 20 points
            points = self.problem5(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except BaseException as e:
            self.feedback += "\nError: " + e.message
        
        try:    # Problem 6: 20 points
            points = self.problem6(student_module)
            score += points
            self.feedback += "\nScore += " + str(points)
        except Exception as e:
            self.feedback += "\nError: " + e.message
        except KeyboardInterrupt as e:
            self.feedback += "\nProblem not graded (code ran for too long)"

        # Report final score.
        total = 70
        percentage = (100.0 * score) / total
        self.feedback += "\n\nTotal score: " + str(score) + "/"
        self.feedback += str(total) + " = " + str(percentage) + "%"
        if   percentage >=  98.0: self.feedback += "\n\nExcellent!"
        elif percentage >=  90.0: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print self.feedback
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t' + comments
        self.score = score

    # Helper Functions
    def strTest(self, x, y, message):
        """Test to see if x and y have the same string representation."""
        if str(x) == str(y):
            return 1
        else:
            self.feedback += message
            self.feedback += "\n\t\tCorrect response: " + str(x)
            self.feedback += "\n\t\tStudent response: " + str(y)
            return 0
    
    def grade(self, points, message):
        """Manually grade a problem and returned points earned."""
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of " + str(points) + ": "))
            except:
                credit = -1
        if credit != points:
            self.feedback += message
        return credit

    # Problems
    def problem1(self, s):
        """Test the Node class comparison and str magic methods. 5 points."""
    
        SNode = s.LinkedListNode
        self.feedback += "\n\nProblem 1 (5 points):"
        points = 0

        # Comparison magic methods
        n1 = SNode(5)
        n2 = SNode(5)
        if not (n1 < n2):
            points += 1
        if n1 == n2:
            points += 1
        n1 = SNode(4)
        n2 = SNode(6)
        if n1 < n2:
            points += 1
        if points < 3:
            self.feedback += "\n\t" + str(3-points) + " "
            self.feedback += "Node class comparison magic method(s) failed"
        
        # Test __str__
        n1 = SNode(6); n2 = SNode("this is a string")
        points += self.strTest(6, n1,"\n\tNode.__str__ failed")
        points += self.strTest("this is a string",n2,"\n\tNode.__str__ failed")

        # TODO: next time, restrict possible inputs (and that's it)
        
        return points

    def problem2(self, s):
        """Test LinkedList.__str__(). 10 Points."""

        self.feedback += "\n\nProblem 2 (10 points):"
        points = 0
        
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

    def problem3(self, s):
        """Test LinkedList.remove() for Exceptions. 10 points."""

        self.feedback += "\n\nProblem 3 (10 points):"
        points = 0
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

    def problem4(self, s):
        """Test LinkedList.insert(). 15 points."""

        self.feedback += "\n\nProblem 4 (15 points):"
        points = 0

        l1 = LinkedList(); l2 = s.LinkedList()

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

    def problem5(self, s):
        """Test the DoublyLinkedList class. 20 points."""

        self.feedback += "\n\nProblem 5 (20 points):"
        points = 0

        l1, l2 = DoublyLinkedList(), s.DoublyLinkedList()
        if not hasattr(l2, "tail"):
            raise AttributeError("'DoublyLinkedList' "
                            + "object has no attribute 'tail'.")

        # Test remove() and add() (12 points)
        function = "DoublyLinkedList.remove()"
        try:
            # Test remove() from empty list (2 points)
            print("\nCorrect output:\t100 is not in the list.")
            print("Student output:\t"),
            try:
                l2.remove(100)
                self.feedback += "\n\tNo exception raised by " + function
                self.feedback ++ " on empty list"
            except ValueError as e:
                points += 1; print(e.message)
                points += self.grade(1,
                    "\n\t" + function + " failed to report on empty list")

            # Test add() (2 points)
            try:
                for i in [0, 2, 4, 5, 7, 8, 9]:
                    l1.add(i); l2.add(i)
            except Exception as e:
                raise Exception("DoublyLinkedList.add() failed: " + str(e))
            points += 2*self.strTest(l1, l2,
                                        "\n\tDoublyLinkedList.add() failed")
            
            # remove() head (2 points)
            l1.remove(0); l2.remove(0)
            points += 2*self.strTest(l1, l2, "\n\t" + function + " failed on "
                + "head removal\n\t(original list: [0, 2, 4, 5, 7, 8, 9])")
            
            # remove() end (2 points)
            l1.remove(9); l2.remove(9)
            points += 2*self.strTest(l1, l2, "\n\t" + function + "failed on "
                + "tail removal\n\t(original list: [2, 4, 5, 7, 8, 9])")
            
            # remove() from middle (2 points)
            l1.remove(5); l2.remove(5)
            points += 2*self.strTest(l1, l2, "\n\t" + function + " failed on "
                + "middle removal\n\t(original list: [2, 4, 5, 7, 8])")
            
            # remove() nonexistent (2 points)
            print("\nCorrect output:\t100 is not in the list.")
            print("Student output:\t"),
            try:
                l2.remove(100)
                self.feedback += "\n\tNo exception raised by " + function
                self.feedback += " for x not in the list"
            except ValueError as e:
                points += 1; print(e.message)
                points += self.grade(1, "\n\t" + function + " failed to "
                                     + "report for x not in the list")
        except BaseException as e:
            raise Exception("DoublyLinkedList.remove() failed: " + str(e))

        # Test insert() (8 points)
        l1, l2 = DoublyLinkedList(), s.DoublyLinkedList()
        try:
            # insert() to empty list (2 points)
            print("\nCorrect output:\t100 is not in the list.")
            print("Student output:\t"),
            try:
                l2.insert(100,100)
                self.feedback += "\n\tNo exception raised by "
                self.feedback += " DoublyLinkedList.insert() on empty list"
            except ValueError as e:
                points += 1; print(e.message)
                points += self.grade(1, "\n\tDoublyLinkedList.insert(x,y) "
                                        + "failed to report on empty list")

            # insert() before head (2 points)
            l1.add(7); l1.insert(1,7)
            l2.add(7); l2.insert(1,7)
            points += 2*self.strTest(l1, l2,
                    "\n\tDoublyLinkedList.insert() failed on inserting before "
                    + "the head\n\t(original list: [7])")
            
            # insert() in the middle (2 points)
            l1.insert(4,7); l2.insert(4,7)
            points += self.strTest(l1, l2,
                    "\n\tDoublyLinkedList.insert() failed on middle insertion"
                    + "\n\t(original list: [1, 7])")
            l1.insert(6,7); l2.insert(6,7)
            points += self.strTest(l1, l2,
                    "\n\tDoublyLinkedList.insert() failed on middle insertion"
                    + "\n\t(original list: [1, 4, 7])")
            
            # insert(data, place) on nonexistant place (2 points)
            print("\nCorrect output:\t100 is not in the list.")
            print("Student output:\t"),
            try:
                l2.insert(1,100)
                self.feedback += "\n\tNo exception raised by DoublyLinkedList"
                self.feedback += ".insert(x,place) for 'place' not in list"
            except ValueError as e:
                points += 1; print(e.message)
                points += self.grade(1, "\n\tDoublyLinkedList.insert(x, place)"
                                + " failed to report for 'place' not in list")
        except BaseException as e:
            raise Exception("DoublyLinkedList.insert() failed: " + str(e))

        # Test inheritance
        if not issubclass(s.DoublyLinkedList, s.LinkedList):
            points = 0
            self.feedback += "\n\tThe DoublyLinkedList class MUST inherit"
            self.feedback += " from the LinkedList class!"

        return points

    def problem6(self, s):
        """Test the SortedLinkedList class and sort_words. 20 points."""

        self.feedback += "\n\nProblem 6 (20 points):"
        points = 0

        # Test add() (2 point)
        l1, l2 = SortedLinkedList(), s.SortedLinkedList()
        entries = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for entry in entries:
            l1.add(entry); l2.add(entry)
        points += 2*self.strTest(l1, l2, "\n\tSortedLinkedList.add() failed"
                    + "\n\t(adding 1, 2, 3, 4, 5, 6, 7, 8, and 9 in order)")

        # Test add() (3 points)
        l1, l2 = SortedLinkedList(), s.SortedLinkedList()
        entries = [9, 8, 7, 6, 5, 4, 2, 3, 1]
        for entry in entries:
            l1.add(entry); l2.add(entry)
        points += 3*self.strTest(l1, l2, "\n\tSortedLinkedList.add() failed"
                    + "\n\t(adding 9, 8, 7, 6, 5, 4, 2, 3, and 1 in order)")

        # Test add() (3 points)
        l1, l2 = SortedLinkedList(), s.SortedLinkedList()
        entries = [1, 3, 5, 7, 9, 2, 4, 6, 8]
        for entry in entries:
            l1.add(entry); l2.add(entry)
        points += 3*self.strTest(l1, l2, "\n\tSortedLinkedList.add() failed"
                    + "\n\t(adding 1, 3, 5, 7, 9, 2, 4, 6, and 8 in order)")

        # Test that insert() was disabled (2 point)
        print("\nCorrect output:\tinsert() has been disabled for this class.")
        print("Student output:\t"),
        try:
            l2.insert(1, 2, 3, 4, 5)
            self.feedback += "\n\tNo exception raised by SortedLinkedList.insert()"
        except (ValueError, NotImplementedError) as e: # NotImplementedError
            points += 1; print(e.message)
            points += self.grade(1, "\n\tSortedLinkedList.insert()" + 
                                " failed to report as disabled")
        except TypeError:
            self.feedback += "\n\tSortedLinkedList.insert() not disabled correctly"
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
        if not isinstance(out, s.SortedLinkedList):
            points = 0
            self.feedback += "\n\tsort_words() must return a "
            self.feedback += "SortedLinkedList object!"
        if not issubclass(s.SortedLinkedList, s.DoublyLinkedList):
            points = 0
            self.feedback += "\n\tThe SortedLinkedList class must inherit "
            self.feedback += "from the DoublyLinkedList class!"

        return points        

