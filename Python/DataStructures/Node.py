class Node(object):
	
	def __init__(self, data):
		self.data = data

	def __str__(self):
		return str(self.data)

class LinkedListNode(Node):

	def __init__(self, data):
		Node.__init__(self, data)
		self.next = None
