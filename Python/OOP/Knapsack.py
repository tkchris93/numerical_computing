import Backpack

class Knapsack(Backpack):

	def __init__(self, color, max_size):
		self.color = color
		self.max_size = max_size
		self.contents = []
	
