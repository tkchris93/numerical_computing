# solutions.py
"""Volume II Lab 5: Data Structures II (Trees). Solutions file."""

from matplotlib import pyplot as plt
from numpy.random import choice
from time import time


class SinglyLinkedListNode(object):
    """Simple singly-linked list node."""
    def __init__(self, data):
        self.value, self.next = data, None

class SinglyLinkedList(object):
    """A very simple singly-linked list with a head and a tail."""
    def __init__(self):
        self.head, self.tail = None, None
    def append(self, data):
        """Add a Node containing 'data' to the end of the list."""
        n = SinglyLinkedListNode(data)
        if self.head is None:
            self.head, self.tail = n, n
        else:
            self.tail.next = n
            self.tail = n

def iterative_search(linkedlist, data):
    """Find the node containing 'data' using an iterative approach.
    If there is no such node in the list, or if the list is empty,
    raise a ValueError.
    
    Inputs:
        linkedlist (LinkedList): a linked list object
        data: the data to find in the list.
    
    Returns:
        The node in 'linkedlist' containing 'data'.
    """
    current = linkedlist.head
    while current is not None:
        if current.value == data:
            return current
        current = current.next
    raise ValueError(str(data) + " is not in the list.")

# Problem 1: rewrite iterative_search() using recursion.
def recursive_search(linkedlist, data):
    """Find the node containing 'data' using a recursive approach.
    If there is no such node in the list, or if the list is empty,
    raise a ValueError.
    
    Inputs:
        linkedlist (LinkedList): a linked list object.
        data: the data to find in the list.
    
    Returns:
        The node in 'linkedlist' containing 'data'.
    """
    def _step(current):
        """Check the current node, and step right if not found."""
        if current is None:         # Base case 1: dead end
            raise ValueError(str(data) + " is not in the list.")
        if current.value == data:   # Base case 2: the data matches
            return current
        else:                       # Recurse if not found
            return _step(current.next)
    
    return _step(linkedlist.head)


class BSTNode(object):
    """A Node class for Binary Search Trees. Contains some data, a
    reference to the parent node, and references to two child nodes.
    """
    def __init__(self, data):
        """Construct a new node and set the data attribute. The other
        attributes will be set when the node is added to a tree.
        """
        self.value = data
        self.prev = None        # A reference to this node's parent node.
        self.left = None        # self.left.value < self.value
        self.right = None       # self.value < self.right.value
    

# Modify this class for problems 2 and 3
class BST(object):
    """Binary Search Tree data structure class.
    The 'root' attribute references the first node in the tree.
    """
    def __init__(self):
        """Initialize the root attribute."""
        self.root = None
    
    def find(self, data):
        """Return the node containing 'data'. If there is no such node
        in the tree, or if the tree is empty, raise a ValueError.
        """
        
        # Define a recursive function to traverse the tree.
        def _step(current):
            """Recursively step through the tree until the node containing
            'data' is found. If there is no such node, raise a Value Error.
            """
            if current is None:                     # Base case 1: dead end.
                raise ValueError(str(data) + " is not in the tree.")
            if data == current.value:               # Base case 2: data found!
                return current
            if data < current.value:                # Recursively search left.
                return _step(current.left)
            else:                                   # Recursively search right.
                return _step(current.right)
        
        # Start the recursion on the root of the tree.
        return _step(self.root)
    
    # Problem 2: Implement BST.insert()
    def insert(self, data):
        """Insert a new node containing 'data' at the appropriate location.
        Do not allow for duplicates in the tree: if there is already a node
        containing 'data' in the tree, raise a ValueError.
        
        Example:
            >>> b = BST()       |   >>> b.insert(1)     |       (4)
            >>> b.insert(4)     |   >>> print(b)        |       / \
            >>> b.insert(3)     |   [4]                 |     (3) (6)
            >>> b.insert(6)     |   [3, 6]              |     /   / \
            >>> b.insert(5)     |   [1, 5, 7]           |   (1) (5) (7)
            >>> b.insert(7)     |   [8]                 |             \
            >>> b.insert(8)     |                       |             (8)
        """

        # Create the node to be inserted.
        new_node = BSTNode(data)
        
        def _find_parent(current):
            """Recursively descend through the tree to find the node that
            should be the parent of the new node. Do not allow for duplicates.
            """

            # Base case: error (shouldn't happen).
            assert current is not None, "_find_parent() error"
            # Base case: duplicate values.
            if data == current.value:
                raise ValueError("{} is already in the tree".format(data))
            # Look to the left.
            elif data < current.value:
                # Recurse on the left branch.
                if current.left is not None:
                    return _find_parent(current.left)
                # Base case: insert the node on the left.
                else:
                    current.left = new_node
            # Look to the right.
            else:
                # Recurse on the right branch.
                if current.right:
                    return _find_parent(current.right)
                # Base case: insert the node on the right.
                else:
                    current.right = new_node
            return current
        
        # Case 1: The tree is empty. Assign the root to the new node.
        if self.root is None:
            self.root = new_node

        # Case 2: The tree is nonempty. Use _find_parent() and double link.
        else:
            # Find the parent and insert the new node as its child.
            parent = _find_parent(self.root)
            # Double-link the child to its parent.
            new_node.prev = parent
    
    # Problem 3: Implement BST.remove()
    def remove(self, data):
        """Remove the node containing 'data'. Consider several cases:
            - The tree is empty
            - The target is the root:
                - The root is a leaf node, hence the only node in the tree
                - The root has one child
                - The root has two children
            - The target is not the root:
                - The target is a leaf node
                - The target has one child
                - The target has two children
            If the tree is empty, or if there is no node containing 'data',
            raise a ValueError.
        
        Examples:
        
            >>> print(b)        |   >>> b.remove(1)     |   [3]
            [4]                 |   >>> b.remove(7)     |   [5]
            [3, 6]              |   >>> b.remove(6)     |   [8]
            [1, 5, 7]           |   >>> b.remove(4)     |
            [8]                 |   >>> print(b)        |
        """
        
        def _successor(node):
            """Find the next-largest node in the tree by travelling
            right once, then left as far as possible.
            """
            assert node.right is not None   # Function called inappropriately
            node = node.right               # Step right once
            while node.left:
                node = node.left            # Step left until done
            return node
        
        # Case 1: the tree is empty
        if self.root is None:
            raise ValueError("The tree is empty.")
        # Case 2: the target is the root
        target = self.find(data)
        if target == self.root:
            # Case 2a: no children
            if not self.root.left and not self.root.right:
                self.__init__()
            # Case 2b: one child
            if not target.right:
                self.root = target.left
            elif not target.left:
                self.root = target.right
            # Case 2c: two children
            else:
                pred = _successor(target)
                self.remove(pred.value)
                target.value = pred.value
            # reset the new root's prev to None
            if self.root:
                self.root.prev = None
        # Case 3: the target is not the root
        else:
            # Case 3a: no children
            if not target.left and not target.right:
                parent = target.prev
                if target.value < parent.value:
                    parent.left = None
                elif target.value > parent.value:
                    parent.right = None
            # Case 3b: one child
            elif not target.right:
                parent = target.prev
                if parent.right is target:
                    parent.right = target.left
                elif parent.left is target:
                    parent.left = target.left
                target.left.prev = parent
            elif not target.left:
                parent = target.prev
                if parent.right is target:
                    parent.right = target.right
                elif parent.left is target:
                    parent.left = target.right
                target.right.prev = parent
            # Case 3c: two children
            else:
                pred = _successor(target)
                self.remove(pred.value)
                target.value = pred.value
    
    def __str__(self):
        """String representation: a hierarchical view of the BST.
        Do not modify this method, but use it often to test this class.
        (this method uses a depth-first search; can you explain how?)
        
        Example:  (3)
                  / \     '[3]          The nodes of the BST are printed out
                (2) (5)    [2, 5]       by depth levels. The edges and empty
                /   / \    [1, 4, 6]'   nodes are not printed.
              (1) (4) (6)
        """
        
        if self.root is None:                   # Print an empty tree
            return "[]"
        # If the tree is nonempty, create a list of lists.
        # Each inner list represents a depth level in the tree.
        str_tree = [list() for i in xrange(_height(self.root) + 1)]
        visited = set()                         # Track visited nodes
        
        def _visit(current, depth):
            """Add the data contained in 'current' to its proper depth level
            list and mark as visited. Continue recusively until all nodes have
            been visited.
            """
            str_tree[depth].append(current.value)
            visited.add(current)
            if current.left and current.left not in visited:
                _visit(current.left, depth+1)  # travel left recursively (DFS)
            if current.right and current.right not in visited:
                _visit(current.right, depth+1) # travel right recursively (DFS)
        
        _visit(self.root, 0)                    # Load the list of lists.
        out = ""                                # Build the final string.
        for level in str_tree:
            if level != list():                 # Ignore empty levels.
                out += str(level) + "\n"
            else:
                break
        return out

class AVL(BST):
    """AVL Binary Search Tree data structure class. Inherits from the BST
    class. Includes methods for rebalancing upon insertion. If your
    BST.insert() method works correctly, this class will work correctly.
    Do not modify.
    """
    def _checkBalance(self, n):
        return abs(_height(n.left) - _height(n.right)) >= 2
    
    def _rotateLeftLeft(self, n):
        temp = n.left
        n.left = temp.right
        if temp.right:
            temp.right.prev = n
        temp.right = n
        temp.prev = n.prev
        n.prev = temp
        if temp.prev:
            if temp.prev.value > temp.value:
                temp.prev.left = temp
            else:
                temp.prev.right = temp
        if n == self.root:
            self.root = temp
        return temp
    
    def _rotateRightRight(self, n):
        temp = n.right
        n.right = temp.left
        if temp.left:
            temp.left.prev = n
        temp.left = n
        temp.prev = n.prev
        n.prev = temp
        if temp.prev:
            if temp.prev.value > temp.value:
                temp.prev.left = temp
            else:
                temp.prev.right = temp
        if n == self.root:
            self.root = temp
        return temp
    
    def _rotateLeftRight(self, n):
        temp1 = n.left
        temp2 = temp1.right
        temp1.right = temp2.left
        if temp2.left:
            temp2.left.prev = temp1
        temp2.prev = n
        temp2.left = temp1
        temp1.prev = temp2
        n.left = temp2
        return self._rotateLeftLeft(n)
    
    def _rotateRightLeft(self, n):
        temp1 = n.right
        temp2 = temp1.left
        temp1.left = temp2.right
        if temp2.right:
            temp2.right.prev = temp1
        temp2.prev = n
        temp2.right = temp1
        temp1.prev = temp2
        n.right = temp2
        return self._rotateRightRight(n)
    
    def _rebalance(self,n):
        """Rebalance the subtree starting at the node 'n'."""
        if self._checkBalance(n):
            if _height(n.left) > _height(n.right):
                # Left Left case
                if _height(n.left.left) > _height(n.left.right):
                    n = self._rotateLeftLeft(n)
                # Left Right case
                else:
                    n = self._rotateLeftRight(n)
            else:
                # Right Right case
                if _height(n.right.right) > _height(n.right.left):
                    n = self._rotateRightRight(n)
                # Right Left case
                else:
                    n = self._rotateRightLeft(n)
        return n
    
    def insert(self, data):
        """Insert a node containing 'data' into the tree, then rebalance."""
        # insert the data like usual
        BST.insert(self, data)
        # rebalance from the bottom up
        n = self.find(data)
        while n:
            n = self._rebalance(n)
            n = n.prev
    
    def remove(*args, **kwargs):
        """Disable remove() to keep the tree in balance."""
        raise NotImplementedError("remove() has been disabled for this class.")

def _height(current):
    """Calculate the height of a given node by descending recursively until
    there are no further child nodes. Return the number of children in the
    longest chain down. Helper function for the AVL class and BST.__str__.
    Do not modify.
                                node | height
    Example:  (c)                  a | 0
              / \                  b | 1
            (b) (f)                c | 3
            /   / \                d | 1
          (a) (d) (g)              e | 0
                \                  f | 2
                (e)                g | 0
    """
    if current is None:     # Base case: the end of a branch.
        return -1           # Otherwise, descend down both branches.
    return 1 + max(_height(current.right), _height(current.left))

# Problem 4: Test build and search speeds for LinkedList, BST, and AVL objects.
def time_structures(filename="English.txt", start=500, stop=5000, step=500):
    """Reach each line from the given file. This will be the data set.
    Vary n from 'start' to 'stop', incrementing by 'step'. At each
    iteration, take the first n words from the specified file.
    
    Time (separately) how long it takes to load a SinglyLinkedList, a BST, and
    an AVL with the data set of n items.
    
    Choose 5 random items from the data set. Time (separately) how long it
    takes to find all 5 items in each object.
    
    Create one plot with two lin-log subplots (use plt.semilogy() instead of
    plt.plot()). In the first subplot, plot the number of items in each
    dataset against the build time for each object. In the second subplot,
    plot the number of items against the search time for each object.
    
    Inputs:
        filename (str): the file to use in creating the data sets.
    
    Returns:
        Show the plot, but do not return any values.
    """
    
    # Initialize lists to hold results
    lls_build, lls_search = [], []
    bst_build, bst_search = [], []
    avl_build, avl_search = [], []

    # TODO: change this to numbers, not strings from a file.
    # Read in the data.
    with open(filename, 'r') as f:
        data = f.readlines()
    
    for n in xrange(start, stop+step, step):
        print "\rn =", n,
    
        # Initialize the subset and data structures.
        subset = choice(data, size=n, replace=False) # or = data[:n]
        bst = BST()
        avl = AVL()
        lls = SinglyLinkedList()
        
        # BUILD TIMES -------------------------------------
        # SinglyLinkedList
        begin = time()
        for word in subset:
            lls.append(word)
        lls_build.append(time() - begin)
        
        # BST
        begin = time()
        for word in subset:
            bst.insert(word)
        bst_build.append(time() - begin)
        
        # AVL
        begin = time()
        for word in subset:
            avl.insert(word)
        avl_build.append(time() - begin)
        
        # SEARCH TIMES -------------------------------------
        small_subset = choice(subset, size=5, replace=False)
        
        # SinglyLinkedList
        begin = time()
        for target in small_subset:
            iterative_search(lls, target)
        lls_search.append(time() - begin)

        # BST
        begin = time()
        for target in small_subset:
            bst.find(target)
        bst_search.append(time() - begin)

        # AVL
        begin = time()
        for target in small_subset:
            avl.find(target)
        avl_search.append(time() - begin)
    
    # Plot the data.
    domain  = list(xrange(start, stop+step, step))
    
    plt.subplot(121)
    plt.title("Build Times")
    plt.semilogy(domain, lls_build, label='Singly-Linked List')
    plt.semilogy(domain, bst_build, label='Binary Search Tree')
    plt.semilogy(domain, avl_build, label='AVL Tree')
    plt.ylabel("seconds")
    plt.xlabel("data points")
    plt.legend(loc='upper left')
    
    plt.subplot(122)
    plt.title("Search Times")
    plt.semilogy(domain, lls_search, label='Singly-Linked List')
    plt.semilogy(domain, bst_search, label='Binary Search Tree')
    plt.semilogy(domain, avl_search, label='AVL Tree')
    plt.ylabel("seconds")
    plt.xlabel("data points")
    plt.legend(loc='upper left')
    
    plt.show()


