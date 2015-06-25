# Location: Lab4_Spec.py
from Node import LinkedListNode as Node

class LinkedList(object):
    ''' 
    A class for creating linked list objects.
    ''' 

    def __init__(self):
        ''' 
        Creates a new linked list.
        Create the head attribute and sets it to None since the list is empty
        ''' 
        self.head = None
	
	def remove_node(self, data):
		print "Hello"	

	def add_node(self, data):
        ''' 
        Create a new Node containing the data and add it to the end of the list
        '''
		print "Hello" 
        new_node = Node(data)
        if self.head is None:
            # If the list is empty, set point the head attribute to the new node.
            self.head = new_node
        else:
            # If the list is not empty, traverse the list and place the new_node at the end.
            current_node = self.head
            while current_node.next is not None:
                # This moves the current node to the next node if it is not empty
                current_node = current_node.next
            current_node.next = new_node
