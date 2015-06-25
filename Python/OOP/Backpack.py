class Backpack:
	
	def __init__(self, color = 'black'):
		self.color = color
		self.contents = []

	def put(self, item):
		self.contents.append(item)

	def take(self, item):
		self.contents.remove(item)

	def __add__(self, other):
		self.contents = self.contents + other.contents
