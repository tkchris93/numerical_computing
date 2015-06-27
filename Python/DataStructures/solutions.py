# lab4_solutions.py
"""Volume II Lab 4: Data Structures 1
    Main solutions file. See also 'Node.py'.
    Written by Shane McQuarrie, Summer 2015.
"""

# The student should import their various Node classes from 'Node.py'.
# from Node import LinkedListNode
# from Node import DoublyLinkedListNode
from WordList import create_word_list

# ============================== Node classes ============================== #
# The following classes should be located in the students' 'Node.py' file.
# Problem 1: Add the magic methods __str__, __lt__, __le__, __eq__,
#   __gt__, and __ge__ to this class.
class Node(object):
    """A Node class for storing data."""
    def __init__(self, data):
        """Construct a new node that stores some data."""
        self.data = data
    def __str__(self): return str(self.data)
    def __lt__(self, other): return self.data <  other.data
    def __le__(self, other): return self.data <= other.data
    def __eq__(self, other): return self.data == other.data 
    def __gt__(self, other): return self.data >  other.data
    def __ge__(self, other): return self.data >= other.data

class LinkedListNode(Node):
    """A Node class for linked lists. Inherits from the 'Node' class.
    Contains a reference to the next node in the list.
    """
    def __init__(self, data):
        """Construct a Node and add an attribute for the next node in the list.
        """
        Node.__init__(self, data)
        self.next = None


class DoublyLinkedListNode(LinkedListNode):
    """A Node class for doubly-linked lists. Inherits from the 'Node' class.
    Contains references to the next and previous nodes in the list.
    """
    def __init__(self,data):
        """Set the next and prev attributes."""
        Node.__init__(self,data)
        self.next = None
        self.prev = None

# ============================== List classes ============================== #
# The following classes should be located in the students' 'solutions.py' file.
# Problems 2, 3, 4: Complete the implementation of the LinkedList class.
class LinkedList(object):
    """Singly-linked list data structure class.
    The first node in the list is referenced to by 'head'.
    """
    def __init__(self):
        """Create a new empty linked list. Create the head
        attribute and set it to None since the list is empty.
        """
        self.head = None
    
    def add(self, data):
        """Create a new Node containing 'data' and add it to
        the end of the list.
        
        Example:
            >>> my_list = LinkedList()
            >>> my_list.add(1)
            >>> my_list.head.data
            1
            >>> my_list.add(2)
            >>> my_list.head.next.data
            2
        """
        new_node = LinkedListNode(data)
        # or new_node = Node(data), depending on how LinkedListNode was imported
        new_node = LinkedListNode(data)
        if self.head is None:
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = new_node
    
    # Problem 2: Implement the __str__ method so that a LinkedList instance can
    #   be printed out the same way that Python lists are printed.
    def __str__(self):
        """String representation: the same as a standard Python list.
        
        Example:
            >>> my_list = LinkedList()
            >>> my_list.add(1)
            >>> my_list.add(2)
            >>> my_list.add(3)
            >>> print(my_list)
            [1, 2, 3]
            >>> str(my_list) == str([1,2,3])
            True
        """
        current = self.head             # List construction method
        items = list()
        while current:
            items.append(current.data)
            current = current.next
        return str(items)
        """current = self.head          # String construction method
        out = "["
        while current:
            out += str(current.data)
            current = current.next
            if current: out += ", "
        out += "]"
        return out
        """

        # Problem 3: Finish implementing remove() so that if the node is not
        #   found, the user is informed.
    def remove(self, data):
        """Remove the node containing 'data'. If the list is empty, or if the
        target node is not in the list, print "<data> is not in the list."
        
        Example:
            >>> print(my_list)
            [1, 2, 3]
            >>> my_list.remove(2)
            >>> print(my_list)
            [1, 3]
            >>> my_list.remove(2)
            2 is not in the list.
            >>> print(my_list)
            [1, 3]
        """
        if self.head is None:           # If the list is empty,
            print str(data) + " is not in the list."    # inform the user
            return                                      # and return.
        if self.head.data == data:      # Remove the head:
            self.head = self.head.next      # Reset the head
        else:                           # Remove nonhead:
            curr = self.head
            while curr.next.data != data:   # Find the node before 'data' node
                curr = curr.next
                if curr.next is None:           # (If the node is not found,
                    print str(data) + " is not in the list."
                    return                      # inform the user and return)
            new_next_node = curr.next.next  # point it to the node after 'data'
            curr.next = new_next_node

    # Problem 4: Implement insert().
    def insert(self, data, place):
        """Create a new Node containing 'data'. Insert it into the list before
        the first Node in the list containing 'place'. If the list is empty, or
        if 'place' is not in the list, print "<place> is not in the list."
        
        Example:
            >>> print(my_list)
            [1, 3]
            >>> my_list.insert(2,3)
            >>> print(my_list)
            [1, 2, 3]
            >>> my_list.insert(2,4)
            4 is not in the list.
        """
        
        n = LinkedListNode(data)        # Create a new node with the data.
        if self.head is None:           # If the list is empty, return.
            print str(place) + " is not in the list."
            return
        # Compare nodes by comparing their data, or by using the Node __eq__.
        # if self.head == n:
        if self.head.data == place:     # Insert at the head:
            n.next = self.head              # Point n to the head
            self.head = n                   # Set n as the new head node
        else:                           # Middle insertion:
            curr = self.head                # Find the node before 'place' node
            while curr.next.data != place:
                curr = curr.next
                if curr.next is None:           # (If the location is not found,
                    print str(place) + " is not in the list."
                    return                      # inform the user and return)
            n.next = curr.next              # point n to 'place' node
            curr.next = n                   # point curr to n

# Problem 5: Implement this class.
class DoublyLinkedList(LinkedList):
    """Doubly-linked list data structure class. Inherits from the 'LinkedList'
    class. Has a 'head' for the front of the list and a 'tail' for the end.
    """
    def __init__(self):
        """Create a new empty doubly-linked list. Create the tail attribute and
        set it to None.
        """
        LinkedList.__init__(self)
        self.tail = None
    
    def add(self, data):
        """Create a new Node containing 'data' and add it to
        the end of the list. Use 'tail' to speed things up.
        """
        new_node = DoublyLinkedListNode(data)
        if self.head is None:           # Empty list
            self.head = new_node            # Assign head
            self.tail = new_node            # Assign tail
        else:                           # Nonempty list
            self.tail.next = new_node       # tail --> new_node
            new_node.prev = self.tail       # tail <-- new_node
            self.tail = new_node            # reset tail to end

    def remove(self, data):
        """Remove the node containing 'data'. If the list is empty, or if the
        target node is not in the list, print "<data> is not in the list."
        """
        if not self.head:               # If the list is empty,
            print str(data) + " is not in the list."    # inform the user
            return                                      # and return.
        if self.head.data == data:      # Remove the head:
            if not self.head.next:          # If there's only one node:
                self.head = None                # reset the head
                self.tail = None                # and the tail
                # self.__init__()               # or do both at once
            else:                           # If there are more than one nodes:
                self.head.next.prev = None      # head <-/- head.next
                self.head = self.head.next      # Reset the head
        else:                           # Remove nonhead:
            curr = self.head
            while curr.data != data:        # Find the target node
                curr = curr.next
                if not curr:                    # (If the node was not found,
                    print str(data) + " is not in the list."
                    return                      # inform the user and return)
            if curr == self.tail:           # If it's the tail:
                curr.prev.next = None           # tail.prev -/-> tail
                self.tail = curr.prev           # reset the tail
            else:                           # It it's not the tail:
                curr.prev.next = curr.next      # target.prev --> target.next
                curr.next.prev = curr.prev      # target.prev <-- target.next
    
    def insert(self, data, place):
        """Create a new Node containing 'data'. Insert it into the list before
        the first Node in the list containing 'place'. If the list is empty, or
        if 'place' is not in the list, print "<place> is not in the list."
        """
        
        n = DoublyLinkedListNode(data)  # Create a new node with the data.
        if self.head is None:           # If the list is empty,
            print str(place) + " is not in the list."   # inform the user
            return                                      # and return.
        # Compare nodes by comparing their data, or by using the Node __eq__.
        # if self.head == n:
        if self.head.data == place:    # Insert at the head:
            n.next = self.head              # n --> head
            self.head.prev = n              # n <-- head
            self.head = n                   # Set n as the new head node
        else:                           # Middle insertion:
            curr = self.head                # Find the node before 'place' node
            while curr.next.data != place:
                curr = curr.next
                if not curr.next:               # (If the location is not found,
                    print str(place) + " is not in the list."
                    return                      # inform the user and return)
            n.next = curr.next              # n --> place
            n.prev = curr                   # curr <-- n
            curr.next.prev = n              # n <-- place
            curr.next = n                   # curr --> n


# Problem 6: Implement this class and use it to sort a large data set.
class SortedLinkedList(DoublyLinkedList):
    """Sorted doubly-linked list data structure class."""

    def add(self, data):
        """Create a new Node containing 'data' and insert it at the
        appropriate location to preserve list sorting.
        Example:
            >>> print(my_list)
            [3, 5]
            >>> my_list.add(2)
            >>> my_list.add(4)
            >>> my_list.add(6)
            >>> print(my_list)
            [2, 3, 4, 5, 6]
        """
        if not self.head:                   # Empty list.
            DoublyLinkedList.add(self,data)
        elif self.tail.data <= data:        # Insert at the tail
            DoublyLinkedList.add(self,data)
        else:                               # Insert not at the tail:
            current = self.head
            while current.data < data:      # Find insertion location
                current = current.next
            DoublyLinkedList.insert(self,data,current.data)     # Insert
    
    def insert(self, data):
        """Overload insert() so the user is forced to use add()."""
        self.add(data)
    # Or simply: insert = add

# Conclude problem 6 by implementing this function.
def sort_words(filename = "English.txt"):
    """Use the 'create_word_list' method from the 'WordList' module to generate
    a scrambled list of words from the specified file. The use an instance of
    the SortedLinkedList class to sort the list.
    """
    s = SortedLinkedList()                  # Create the Sorted List object
    word_list = create_word_list(filename)  # Generate the word list
    for word in word_list:                  # Add each word to the Sorted List
        s.add(word)
    return s                                # Return the Sorted Linked List.

# =========================== END OF SOLUTIONS =========================== #
# Test script
def test(student_module, node_module, late=False):
    """Test script. You must import the student's 'solutions.py' and 'Node.py'
    files as modules.
    
     5 points for problem 1
    10 points for problem 2
    10 points for problem 3
    15 points for problem 4
    20 points for problem 5
    20 points for problem 6
    
    Inputs:
        student_module: the imported module for the student's file.
        node_module: the imported module for the student's 'Node.py' file.
        late (bool): if True, half credit is awarded.
    
    Returns:
        score (int): the student's score, out of 80.
        feedback (str): a printout of test results for the student.
    """
    s = student_module
    score = 0
    feedback = s.__doc__
    print(feedback)

    def testPart(p,x,y,m):
        """Test to see if x and y have the same string representation. If
        correct, award 'p' points and return no message. If incorrect, return
        0 and return 'm' as feedback.
        """
        if str(x) == str(y): return p, ""
        else: return 0, m
    
    def testTail(p,x,y,m):
        """Test to see if x and y have the same tail attribute. If correct,
        award 'p' points and return no message. If incorrect, return 0 and
        return 'm' as feedback. Problematic if list has 0 or 1 entries.
        """
        if x.tail.prev.next == y.tail.prev.next: return p, ""
        else: return 0, m
    
    def strTest(p,m):
        """Manually grade a problem worth 'p' points with error message 'm'."""
        part = p + 1
        while part > p:
            part = int(input("\nScore out of " + str(p) + ": "))
        if part < p: return part,m
        else: return part,""
    
    from numpy.random import permutation # numpy is not required for this lab
    def shrink_file(infile, outfile):
        """Shrink the dataset in problem 6 so it can be tested quickly."""
        f = open(infile, 'r')
        f = f.read()
        f = f.split('\n')
        f = f[:-1]
        x = list(permutation(f))[::20]
        f = open(outfile, 'w')
        for i in x:
            f.write(i + '\n')
        f.close()
    
    try:
        # Problem 1: 5 points
        feedback += "\nTesting problem 1 (5 points):"
        points = 0
        SNode = node_module.Node
        # Comparison magic methods
        n1 = SNode(5)
        n2 = SNode(5)
        if n1 <= n2: points += 1
        if n1 == n2: points += 1
        n1 = SNode(4)
        n2 = SNode(6)
        if not (n1 > n2): points += 1
        if points < 3:
            feedback += "\n\t" + str(3-points)
            feedback += " Node class comparison magic method(s) failed"
        # __str__
        n1 = Node(6)
        if str(n1) == str(n2): points += 2
        else: feedback += "\n\tNode.__str__ failed"
        
        score += points; feedback += "\n  Score += " + str(points)
        
        # Problem 2: 10 points
        feedback += "\nTesting problem 2 (10 points):"
        points = 0
        # Empty list
        l1 = s.LinkedList()
        l2 = list()
        p,f = testPart(1,l1,l2,"\n\tLinkedList.__str__ failed on empty list")
        points += p; feedback += f
        # Single item
        l1.add(3)
        l2.append(3)
        p,f = testPart(3,l1,l2,"\n\tLinkedList.__str__ failed on single item")
        points += p; feedback += f
        # Two items
        l1.add('applesausage')
        l2.append('applesausage')
        p,f = testPart(3,l1,l2,"\n\tLinkedList.__str__ failed on two items")
        points += p; feedback += f
        # Many items
        entries = ['a','b',3,10.0,-1+3j,'...testing...']
        for i in entries:
            l1.add(i)
            l2.append(i)
        p,f = testPart(3,l1,l2,"\n\tLinkedList.__str__ failed on many items")
        points += p; feedback += f
        if points == 0:
            feedback += "\n\tCheck LinkedList.add() and LinkedList.__str__"
        
        score += points; feedback += "\n  Score += " + str(points)
        
        # Problem 3: 10 points
        feedback += "\nTesting problem 3 (10 points):"
        points = 0
        l1 =   LinkedList()
        l2 = s.LinkedList()
        # remove() from empty list
        print("\nCorrect output:\t"),;  l1.remove(100)
        print("Student output:\t"),;    l2.remove(100)
        p,f = strTest(2,
            "\n\tLinkedList.remove() failed to report on empty list")
        points += p; feedback += f
        # Test add() (no credit, but vital for other points)
        for i in [1,3,2,5,4,7,6,9,8]:
            l1.add(i); l2.add(i)
        p,f=testPart(0,l1,l2,
            "\n\tIf __str__ fails, these tests will all fail")
        points += p; feedback += f
        # remove() head
        l1.remove(1); l1.remove(3)
        l2.remove(1); l2.remove(3)
        p,f = testPart(2,l1,l2,
            "\n\tLinkedList.remove() failed on head removal")
        points += p; feedback += f
        # remove() end
        l1.remove(8); l1.remove(9)
        l2.remove(8); l2.remove(9)
        p,f = testPart(2,l1,l2,
            "\n\tLinkedList.remove() failed on tail removal")
        points += p; feedback += f
        # remove() from middle
        l1.remove(5); l1.remove(4)
        l2.remove(5); l2.remove(4)
        p,f=testPart(2,l1,l2,
            "\n\tLinkedList.remove() failed on middle removal")
        points += p; feedback += f
        # remove() nonexistent 
        print("\nCorrect output:\t"),;  l1.remove(100)
        print("Student output:\t"),;    l2.remove(100)
        p,f = strTest(2,
            "\n\tLinkedList.remove(x) failed to report for x not in list")
        points += p; feedback += f
        
        score += points; feedback += "\n  Score += " + str(points)
        
        # Problem 4: 15 Points
        feedback += "\nTesting problem 4 (15 points):"
        points = 0
        l1 =   LinkedList()
        l2 = s.LinkedList()
        # insert() empty list
        print("\nCorrect output:\t"),;  l1.insert(1,100)
        print("Student output:\t"),;    l2.insert(1,100)
        p,f = strTest(2,
            "\n\tLinkedList.insert() failed to report on empty list")
        points += p; feedback += f
        # insert() before head
        l1.add(5); l1.insert(3,5); l1.insert(1,3)
        l2.add(5); l2.insert(3,5); l2.insert(1,3)
        p,f=testPart(5,l1,l2,
            "\n\tLinkedList.insert() failed on head insertion")
        points += p; feedback += f
        # insert() in the middle
        l1.insert(2,3); l1.insert(4,5)
        l2.insert(2,3); l2.insert(4,5)
        p,f=testPart(5,l1,l2,
            "\n\tLinkedList.insert() failed on middle insertion")
        points += p; feedback += f
        print("\nCorrect output:")
        l1.insert(1,10); l1.insert(1,11); l1.insert(1,12)
        print("\nStudent output:")
        l2.insert(1,10); l2.insert(1,11); l2.insert(1,12)
        p,f = strTest(3,
            "\n\tLinkedList.insert(x,place) failed to report on bad place")
        points += p; feedback += f
        
        score += points; feedback += "\n  Score += " + str(points)
        
        # Problem 5: 20 points
        feedback += "\nTesting problem 5 (20 points):"
        points = 0
        l1 =   DoublyLinkedList()
        l2 = s.DoublyLinkedList()
        # remove() from empty list
        print("\nCorrect output:\t"),;  l1.remove(100)
        print("Student output:\t"),;    l2.remove(100)
        p,f = strTest(1,
            "\n\tDoublyLinkedList.remove() failed to report on empty list")
        points += p; feedback += f
        # Test add() (no credit, but vital for other points)
        for i in [1,3,2,5,4,7,6,9,8]:
            l1.add(i); l2.add(i)
        p,f=testPart(1,l1,l2,"\n\tDoublyLinkedList.add() failed")
        points += p; feedback += f
        p,f = testTail(1,l1,l2,
            "\n\tDoublyLinkedList.tail failed on add()")
        points += p; feedback += f
        # remove() head
        l1.remove(1); l1.remove(3)
        l2.remove(1); l2.remove(3)
        p,f = testPart(1,l1,l2,
            "\n\tDoublyLinkedList.remove() failed on head removal")
        points += p; feedback += f
        p,f = testTail(1,l1,l2,
            "\n\tDoublyLinkedList.tail failed on head removal")
        points += p; feedback += f
        # remove() end
        l1.remove(8); l1.remove(9)
        l2.remove(8); l2.remove(9)
        p,f = testPart(1,l1,l2,
            "\n\tDoublyLinkedList.remove() failed on tail removal")
        points += p; feedback += f
        p,f = testTail(1,l1,l2,
            "\n\tDoublyLinkedList.tail failed on tail removal")
        points += p; feedback += f
        # remove() from middle
        l1.remove(5); l1.remove(4)
        l2.remove(5); l2.remove(4)
        p,f=testPart(1,l1,l2,
            "\n\tDoublyLinkedList.remove() failed on middle removal")
        points += p; feedback += f
        p,f = testTail(1,l1,l2,
            "\n\tDoublyLinkedList.tail failed on middle removal")
        points += p; feedback += f
        # remove() nonexistent 
        print("\nCorrect output:\t"),;  l1.remove(100)
        print("Student output:\t"),;    l2.remove(100)
        p,f = strTest(1,
            "\n\tDoublyLinkedList.remove(x) failed to report for x not in list")
        points += p; feedback += f
        # insert() empty list
        l1.__init__(); l2.__init__()
        print("\nCorrect output:\t"),;  l1.insert(1,100)
        print("Student output:\t"),;    l2.insert(1,100)
        p,f = strTest(1,
            "\n\tDoublyLinkedList.insert() failed to report on empty list")
        points += p; feedback += f
        # insert() before head
        l1.add(5); l1.insert(3,5); l1.insert(1,3)
        l2.add(5); l2.insert(3,5); l2.insert(1,3)
        p,f=testPart(3,l1,l2,
            "\n\tDoublyLinkedList.insert() failed on head insertion")
        points += p; feedback += f
        p,f = testTail(1,l1,l2,
            "\n\tDoublyLinkedList.tail failed on head insertion")
        points += p; feedback += f
        # insert() in the middle
        l1.insert(2,3); l1.insert(4,5)
        l2.insert(2,3); l2.insert(4,5)
        p,f=testPart(3,l1,l2,
            "\n\tDoublyLinkedList.insert() failed on middle insertion")
        points += p; feedback += f
        p,f = testTail(1,l1,l2,
            "\n\tDoublyLinkedList.tail failed on middle insertion")
        points += p; feedback += f
        print("\nCorrect output:")
        l1.insert(1,10); l1.insert(1,11); l1.insert(1,12)
        print("\nStudent output:")
        l2.insert(1,10); l2.insert(1,11); l2.insert(1,12)
        p,f = strTest(1,
            "\n\tDoublyLinkedList.insert(x,place) failed to report on bad place")
        points += p; feedback += f
        
        score += points; feedback += "\n  Score += " + str(points)
        
        # Problem 6: 20 points
        feedback += "\nTesting problem 6 (20 points):"
        points = 0
        l1 =   SortedLinkedList()
        l2 = s.SortedLinkedList()
        # 10 points for correct SortedLinkedList
        # test 1
        entries = [1,2,3,4,5,'a','b','c','d','e']
        for i in entries:
            l1.add(i); l2.add(i)
        p,f = testPart(3,l1,l2,"\n\tSortedLinkedList.add() failed")
        points += p; feedback += f
        # test 2
        l1.__init__()
        l2.__init__()
        entries = [9,8,7,6,5,4,2,3,1,'a','i','u','o','e']
        for i in entries:
            l1.add(i); l2.add(i)
        p,f = testPart(3,l1,l2,"\n\tSortedLinkedList.add() failed")
        points += p; feedback += f
        # test 3
        l1.__init__(); l2.__init__()
        entries = [1,3,5,7,9,2,4,6,8,0]
        for i in entries:
            l1.add(i); l2.add(i)
        p,f = testPart(4,l1,l2,"\n\tSortedLinkedList.insert() failed")
        points += p; feedback += f
        # 10 points for correct sort_words() output.
        shrink_file("English.txt", "Short.txt")
        word_list = create_word_list("Short.txt")
        word_list.sort()
        p,f = testPart(10,word_list,s.sort_words("Short.txt"),
            "\n\tsort_words() function failed.")
        points += p; feedback += f
        
        score += points; feedback += "\n  Score += " + str(points)
    
    except: feedback += "\n\nCompilation Error!!"
    
    if late:    # Late submission penalty
        feedback += "\n\nHalf credit for late submission."
        feedback += "\nRaw score: " + str(score) + "/80"
        score *= .5
    
    # Report final score
    feedback += "\n\nTotal score: "+str(score)+"/80 = "+str(score/.8)+"%"
    if score/.8 < 72.0 and not late:
        feedback += "\n\nOn any given problem, if one test fails then"
        feedback += " subsequent tests are likely to fail.\nFix the tests in"
        feedback += " the order that they are mentioned in this feedback file."
    if score/.8 >= 98.0: feedback += "\n\nExcellent!"
    elif score/.8 >= 90.0: feedback += "\n\nGreat job!"
    
    return score,feedback