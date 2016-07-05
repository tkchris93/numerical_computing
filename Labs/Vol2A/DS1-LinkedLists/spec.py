# name this file 'solutions.py'.
"""Volume II Lab 4: Data Structures 1 (Linked Lists)
<Name>
<Class>
<Date>
"""


# Problem 1
class Node(object):
    """A basic node class for storing data."""
    def __init__(self, data):
        """Store 'data' in the 'value' attribute."""
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

    # Problem 2: LinkedList.find().

    # Problem 3: LinkedList.__len__() and LinkedList.__str__().

    # Problem 4: LinkedList.remove().

    # Problem 5: LinkedList.insert().


# Problem 6: Write a Deque class.


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
