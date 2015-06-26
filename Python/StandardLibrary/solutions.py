# solutions.py
""" Volume II Lab 1: The Standard Library
    Main solutions file. See also 'calculator.py' and 'test_module.py'.
    Use the test() method as a test script.
    Written by Shane McQuarrie, Spring 2015.
"""

import calculator # as c
import sys
import time
import matrix_multiply # as m

# Problem 1
def prob1(l):
    """Accept a list 'l' of numbers as input and return a list with the
    minimum, maximum, and average of the original list.
    """
    ans = []
    ans.append(min(l))
    ans.append(max(l))
    ans.append(float(sum(l))/len(l))
    return ans

# Problem 2
def prob2():
    """Determine which Python objects are mutable and which are immutable. Test
    numbers, strings, lists, tuples, and dictionaries.
    """

    # numbers: num+= 1
    num1 = 0
    num2 = num1
    num1 += 1
    print("Numbers:\t"),
    if num1 == num2: print("Mutable")
    else: print("Immutable")

    # strings: str1 += 'a'
    str1 = "a"
    str2 = str1
    str1 += "a"
    print("Strings:\t"),
    if str1 == str2: print("Mutable")
    else: print("Immutable")

    # lists: list1.append(1)
    list1 = [4,3,2]
    list2 = list1
    list1.append(1)
    print("Lists:\t\t"),
    if list1 == list2: print("Mutable")
    else: print("Immutable")

    # tuples: tup1 += (1,)
    tup1 = (4,3,2)
    tup2 = tup1
    tup1 += (1,)
    print("Tuples:\t\t"),
    if tup1 == tup2: print("Mutable")
    else: print("Immutable")

    # dictionaries: dic1[1] = 'a'
    dic1 = dict()
    dic1[1] = 'b'
    dic2 = dic1
    dic1[1] = 'a'
    print ("Dictionaries:\t"),
    if dic1 == dic2: print("Mutable")
    else: print("Immutable")

# Problem 3
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
    a2 = calculator.mult(a,a)
    b2 = calculator.mult(b,b)
    a2plusb2 = calculator.add(a2, b2)
    return calculator.sqrt(a2plusb2)
    # Or, simply
    c = calculator              # or "import calculator as c" at the top
    return c.sqrt(c.add(c.mult(a,a),c.mult(b,b)))

# Problem 4: Utilize the 'matrix_multiply' module and 'matrices.npz' to
#   implement this function.
def prob4():
    """If no command line argument is given, print "No Input." If anything
    other than "matrices.npz is given, print "Incorrect Input." If
    "matrices.npz" is given as a command line argument, use the 'load_matrices'
    function to load two matrices called 'A' and 'B'. Finally, time how long
    each method takes to multiply the two matrices together. Print your results
    to the terminal.
    """
    if len(sys.argv) == 1: print("No input")
    elif sys.argv[1] != "matrices.npz": print("Incorrect Input")
    else:   # If the correct filename is given,
        m = matrix_multiply     # or "import matrix_multiply as m" at the top
        A,B = m.load_matrices(sys.argv[1])  # load the matrices
        
        # time method1()
        start = time.time()
        m.method1(A,B)
        print(time.time() - start)
        
        # time method2()
        start = time.time()
        m.method2(A,B)
        print(time.time() - start)
        
        # time method3()
        start = time.time()
        m.method3(A,B)
        print(time.time() - start)

# Everything under this 'if' statement is executed when this file is run from
#   the terminal. In this case, if we enter 'python solutions.py word' into the
#   terminal, then sys.argv is ['solutions.py, 'word'], and prob4() is executed.
if __name__ == "__main__":
    prob4()

# =========================== END OF SOLUTIONS =========================== #

# Test script
def test(student_module, student_file):
    """Test script. You must import the students file as a module AND have the
    students' filename (because of the sys stuff in problem 4)
    3 points for problem 1
    5 points for problem 2
    5 points for problem 3
    7 points for problem 4
    
    Parameters:
        student_module: the imported module for the student's file.
        student_file: the student's filename, including the path.
    
    Returns:
        score (int): the student's score, out of 100
        feedback (str): a printout of test results for the student.
    """
    
    import os
    if os.system('ls ' + student_file):
        return
    s = student_module
    path = student_file
    score = 0
    feedback = ""
    
    try:
        # Problem 1: 3 points
        feedback += "Testing problem 1 (3 points)..."
        points = 3
        l = [192102312,-234892,9423,1220002,82,3432,23892,100000,-123812]
        [min1,max1,ave1] = s.prob1(l)
        [min2,max2,ave2] = prob1(l)
        if max1 != max2:
            points -= 1; feedback += "\n\tincorrect maximum"
        if min1 != min2:
            points -= 1; feedback += "\n\tincorrect minimum"
        if ave1 != ave2:
            points -= 1; feedback += "\n\tincorrect average"

        feedback += "\n  Score += " + str(points)
        score += points
    
        # Problem 2: 5 points
        feedback += "\nTesting problem 2 (5 points)..."
        print"\nExpected output:"
        prob2()
        print"\nStudent output:"
        s.prob2()
        points = int(input("\nScore out of 5: "))
        if points < 5: feedback += "\n\tincorrect response(s)"
        
        feedback += "\n  Score += " + str(points)
        score += points
        
        # Problem 3: 5 points
        feedback += "\nTesting problem 3 (5 points)..."
        points = 5
        if s.prob3(5,12) != prob3(5,12):
            points -= 2; feedback += "\n\tincorrect hypotenuse length"
        if s.prob3(6,7) != prob3(6,7):
            points -= 3; feedback += "\n\tincorrect hypotenuse length"
            
        feedback += "\n  Score += " + str(points)
        score += points
        
        # Problem 4: 7 points
        feedback += "\nTesting problem 4 (7 points)..."
        points = 7
        print("\nExpected output:")
        os.system('python lab1_solutions.py')
        os.system('python lab1_solutions.py "Wrong Name"')
        os.system('python lab1_solutions.py "matrices.npz"')
        print("\nStudent output:")
        os.system('python ' + path)
        os.system('python ' + path + ' "Wrong Name"')
        os.system('python ' + path + ' "matrices.npz"')
        points = int(input("\nScore out of 7: "))
        if points < 7: feedback += "\n\tincorrect outputs"

        feedback += "\n  Score += " + str(points)
        score += points
        
    except:
        feedback += "\n\nCompilation Error!!"
    
    feedback += "\n\nTotal score: "+str(score)+"/20 = "+str(score/.2)+"%"
    return score/.2, feedback
