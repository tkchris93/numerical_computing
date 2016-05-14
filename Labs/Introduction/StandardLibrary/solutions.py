# solutions.py
"""Introductory Labs: The Standard Library. Solutions file."""

# calculator.py ===============================================================
# Students write this module as part of problem 3. Do not provide to students.

def add(x,y):
    return x+y

def mult(x,y):
    return x*y

def sqrt(x):
    return x**.5
    # or, from math import sqrt at the top.

# matrix_multiply.py ==========================================================
# This module is provided to students and used to complete problem 4.

import numpy as np

def load_matrices(filename):
    """Returns two matrices if the correct filename is given."""
    
    files = np.load(filename)
    return files['arr_0'], files['arr_1']


def method1(A,B):
    """Multiply the matrices 'A' and 'B' together using nested for loops."""
    
    product_matrix = np.zeros((A.shape[0], B.shape[1]))
    for i in range(product_matrix.shape[0]):
        for j in range(product_matrix.shape[1]):
            for k in range(product_matrix.shape[0]):
                product_matrix[i,j] += A[i,k]*B[k,j] 
    
    return product_matrix


def method2(A,B):
    """Multiply the matrices 'A' and 'B' together with some vectorization.
    Use xrange() instead of range() to make things a little faster.
    """
    
    product_matrix = np.zeros((A.shape[0], B.shape[1]))
    for i in xrange(product_matrix.shape[0]):
        for j in xrange(product_matrix.shape[1]):
            product_matrix[i,j] = np.dot(A[i,:], B[:,j])
    
    return product_matrix


def method3(A,B):
    """Use numpy's matrix multiplication method for maximum speed."""
    
    return np.dot(A,B)


# solutions.py ================================================================

import sys
import time

# Problem 1: Implement this function.
def prob1(l):
    """Accept a list 'l' of numbers as input and return a list with the
    minimum, maximum, and average of the original list (in that order).
    """
    return [min(l), max(l), float(sum(l))/len(l)]


# Problem 2: Implement this function.
def prob2():
    """Programmatically determine which Python objects are mutable and which
    are immutable. Test numbers, strings, lists, tuples, and dictionaries.
    Print your results to the terminal.
    """

    # numbers: num+= 1
    num1 = 0
    num2 = num1
    num1 += 1
    print("Numbers:\t"),
    if num1 == num2:
        print("Mutable")
    else:
        print("Immutable")

    # strings: str1 += 'a'
    str1 = "a"
    str2 = str1
    str1 += "a"
    print("Strings:\t"),
    if str1 == str2:
        print("Mutable")
    else:
        print("Immutable")

    # lists: list1.append(1)
    list1 = [4,3,2]
    list2 = list1
    list1.append(1)
    print("Lists:\t\t"),
    if list1 == list2:
        print("Mutable")
    else:
        print("Immutable")

    # tuples: tup1 += (1,)
    tup1 = (4,3,2)
    tup2 = tup1
    tup1 += (1,)
    print("Tuples:\t\t"),
    if tup1 == tup2:
        print("Mutable")
    else:
        print("Immutable")

    # dictionaries: dic1[1] = 'a'
    dic1 = dict()
    dic1[1] = 'b'
    dic2 = dic1
    dic1[1] = 'a'
    print("Dictionaries:\t"),
    if dic1 == dic2:
        print("Mutable")
    else:
        print("Immutable")


# Problem 3: Write a 'calculator' module and use it to implement this function.
def prob3(a,b):
    """Calculate and return the length of the hypotenuse of a right triangle.
    Do not use any methods other than those that are imported from the
    'calculator' module.
    Parameters:
        a : the length one of the sides of the triangle.
        b : the length the other nonhypotenuse side of the triangle.
    Returns:
        The length of the triangle's hypotenuse.
    """
    # c = calculator              # or "import calculator as c" at the top
    # return c.sqrt(c.add(c.mult(a,a),c.mult(b,b)))

    # Or, a slightly longer way:
    a2 = mult(a,a)
    b2 = mult(b,b)
    a2plusb2 = add(a2, b2)
    return sqrt(a2plusb2)


# Problem 4
def prob4():
    """If no command line argument is given, print "No Input."
    If anything other than "matrices.npz is given, print "Incorrect Input."
    If "matrices.npz" is given as a command line argument, use functions
    from the provided 'matrix_multiply' module to load two matrices, then
    time how long each method takes to multiply the two matrices together.
    Print your results to the terminal.
    """
    # Students should use matrix_multiply.method() instead of method()
    # m = matrix_multiply     # or "import matrix_multiply as m" at the top
    if len(sys.argv) == 1:
        print("No Input.")
    elif sys.argv[1] != "matrices.npz":
        print("Incorrect Input.")
    else:   # If the correct filename is given,
        # load the matrices
        A,B = load_matrices(sys.argv[1])
        
        # time method1()
        start = time.time()
        method1(A,B)
        print(time.time() - start)
        
        # time method2()
        start = time.time()
        method2(A,B)
        print(time.time() - start)
        
        # time method3()
        start = time.time()
        method3(A,B)
        print(time.time() - start)

if __name__ == "__main__":
    prob4()

