import pickle
import numpy as np
import sys

def load_data(n=100000):

	num_list = pickle.load(open("num_list.p", 'rb'))
	num_bst = pickle.load(open("num_bst.p", 'rb'))

	numbers = np.random.permutation(np.array(range(n)))

	for i in xrange(n):
		num_list.add_node(numbers[i])
		num_tree.insert(numbers[i])
		sys.stdout.write('Iteration ' + str(i + 1) + ' of ' + str(n) + '\r')
		sys.stdout.flush()

	return num_list, num_tree

def load_words():
	raise NotImplementedError


