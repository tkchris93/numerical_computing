# plots.py
"""Volume 2: Data Structures 2 (Trees). Plot-producing file."""

import numpy as np
from time import time
from sys import stdout
from scipy.stats import linregress
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from solutions import iterative_search, SinglyLinkedList, BST, AVL

def prob4_plots(start=500, stop=5500, step=500, verbose=False):
    """Vary n from 'start' to 'stop', incrementing by 'step'. At each
    iteration, take the first n words from the specified file.
    
    Time (separately) how long it takes to load a SinglyLinkedList, a BST, and
    an AVL with the data set of n items.
    
    Choose 5 random items from the data set. Time (separately) how long it
    takes to find all 5 items in each object.
    
    Create two lin-log figures.
    The first figure plots the number of items in each dataset against the
    build time for each object.
    The second figure, plots the number of items against the search time for
    each object.
    
    Inputs:
        start, stop, step (ints): parameters for the domain.
    
    Returns:
        Show the plot, but do not return any values.
    """
    
    # Initialize lists to hold results
    lls_build, lls_search = [], []
    bst_build, bst_search = [], []
    avl_build, avl_search = [], []

    data = np.random.random(stop)
    
    # Get the values [start, start + step, ..., stop - step]
    for n in xrange(start,stop,step):
        if verbose:
            print "\rn =",n,; stdout.flush()
    
        # Initialize wordlist and data structures
        subset = data[:n]
        bst = BST()
        avl = AVL()
        lls = SinglyLinkedList()
        
        # Time the singly-linked list build
        begin = time()
        for item in subset:
            lls.append(item)
        lls_build.append(time() - begin)
        
        # Time the binary search tree build
        begin = time()
        for item in subset:
            bst.insert(item)
        bst_build.append(time() - begin)
        
        # Time the AVL tree build
        begin = time()
        for item in subset:
            avl.insert(item)
        avl_build.append(time() - begin)
        
        rand_subset = np.random.choice(subset, size=5, replace=False)
        
        # Time the singly-linked list search
        begin = time()
        for target in rand_subset:
            iterative_search(lls, target)
        lls_search.append(time() - begin)

        # Time the binary search tree search
        begin = time()
        for target in rand_subset:
            bst.find(target)
        bst_search.append(time() - begin)

        # Time the AVL tree search
        begin = time()
        for target in rand_subset:
            avl.find(target)
        avl_search.append(time() - begin)
    
    domain = np.array(xrange(start, stop, step))
    x_axis = np.linspace(start, stop-step, 200)
    
    # Do a least squares fit to the data so the curves aren't noisy.
    def lin_lstq(y_vals):
        slope, intercept = linregress(domain, y_vals)[:2]
        return x_axis*slope + intercept
    lls_build = lin_lstq(lls_build)
    bst_build = lin_lstq(bst_build)
    lls_search = lin_lstq(lls_search)
    bst_search = lin_lstq(bst_search)
    avl_search = lin_lstq(avl_search)
    parabola = lambda t, A, B: A + B*t**2
    a,b = curve_fit(parabola, domain, avl_build)[0]
    avl_build = parabola(x_axis, a, b)

    # Plot the data
    plt.clf()
    plt.figure(1)
    plt.title("Build Times")
    plt.semilogy(x_axis,lls_build,label='Singly-Linked List')
    plt.semilogy(x_axis,bst_build,label='Binary Search Tree')
    plt.semilogy(x_axis,avl_build,label='AVL Tree')
    plt.ylabel("seconds")
    plt.xlabel("data points")
    plt.legend(loc='upper left')
    plt.savefig("BuildTimes.pdf")
    plt.clf()
    
    plt.figure(2)
    plt.title("Search Times")
    plt.semilogy(x_axis,lls_search,label='Singly-Linked List')
    plt.semilogy(x_axis,bst_search,label='Binary Search Tree')
    plt.semilogy(x_axis,avl_search,label='AVL Tree')
    plt.ylabel("seconds")
    plt.xlabel("data points")
    plt.legend(loc='upper left')
    plt.savefig("SearchTimes.pdf")
    plt.clf()

if __name__ == '__main__':
    prob4_plots(500, 5050, 50, True)