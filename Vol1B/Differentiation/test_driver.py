# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 16:41:20 2015

@author: acme
"""

# spec.py
import numpy as np
from matplotlib import pyplot as plt
from numpy import linalg as la

# Problem 1: Implement this function.
def centered_difference_quotient(f,pts,h = 1e-5):
    derivative = lambda x: .5*(f(x+h)-f(x-h))/h
    return derivative(pts)


# Problem 2: Implement this function.
def jacobian(f,n,m,pt,h = 1e-5):
    '''
    Compute the approximate Jacobian matrix of f at pt using the centered
    difference quotient.
    Inputs:
        f (function): the multidimensional function for which the derivative
            will be approximated
        n (int): dimension of the domain of f
        m (int): dimension of the range of f
        pt (array): an n-dimensional array representing a point in R^n
        h (float): a float to use in the centered difference approximation
    Returns:
        Jacobian matrix of f at pt using the centered difference quotient.
    '''
    I = np.eye(n)
    J = np.zeros((m,n))
    for i in xrange(n):
        e = I[:,i]
        J[:,i] = .5*(f(pt+h*e) - f(pt-h*e))/h
        
    return J


# Problem 3: Implement this function.
def findError():
    '''
    Compute the maximum error of your jacobian function for the function
    f(x,y)=[(e^x)*sin(y)+y^3,3y-cos(x)] on the square [-1,1]x[-1,1].
    Returns:
        Maximum error of your jacobian function.
    '''
    f = lambda x: np.array([np.exp(x[0])*np.sin(x[1]) + x[1]**3, 3*x[1] - np.cos(x[0])])
    Df = lambda x: np.array([[np.exp(x[0])*np.sin(x[1]),np.exp(x[0])*np.cos(x[1]) + 3*x[1]**2],[np.sin(x[0]),3]])
 
    
    max_error = 0.
    xx = np.linspace(-1,1,100)
    for x in xx:
        for y in xx:
            pt = np.array([x,y])
            err_matrix =  Df([x,y]) - jacobian(f, 2,2, pt)
            error = la.norm(err_matrix)
            if error > max_error:
                max_error = error
                print error
                
    return max_error
    

def get_img(filename):
    #Gets a grayscale image
    img = plt.imread(filename)
    #return (img[:,:,0] + img[:,:,1] + img[:,:,2])/3.
    return img[:,:,2]

# ======= TEST DRIVER ===========
# Test script
def test(student_module, late=False):
    """Test script. You must import the students file as a module.
    
    10 points for problem 1
    10 points for problem 2
    10 points for problem 3
    10 points for problem 4
    10 points for problem 5
    10 points for problem 6
    10 points for problem 7
    
    Parameters:
        student_module: the imported module for the student's file.
        late (bool, opt): if True, half credit is awarded.
    
    Returns:
        score (int): the student's score, out of 55.
        feedback (str): a printout of results for the student.
    """
    
    def arrayTest(A,B,f):
        if np.allclose(A,B):
            return 1, ""
        else:
            return 0, f
    
    def grade(p):
        """Manually grade a problem worth 'p' points"""
        part = -1
        while part > p or part < 0:
            part = int(input("\nScore out of " + str(p) + ": "))
        if part == p: return p,""
        else: 
            m = "\n" + raw_input("\nEnter extra feedback:")
            return part,m
            
    
        
    s = student_module
    score = 0
    total = 50
    feedback = ""
    
    
    try: #Problem 1: 15 points
        feedback += "\n\nProblem 1 (15 points):"
        points = 0  
        pts = np.linspace(-5,5,40)
        
        #Test 1: Sine
        sine = lambda x: 2*np.sin(x)
        err_message = "\nIncorrect output for f(x) = 2*sin(x)."
        
        y = centered_difference_quotient(sine,pts)
        y_s = s.centered_difference_quotient(sine,pts)
        
        p,f = arrayTest(y, y_s, err_message)
        points += p*5
        feedback += f
        
        #Test 2: abs
        absfunc = lambda x: 2*np.abs(4 - x**2)
        err_message = "\nIncorrect output for f(x) = abs(4 - x^2)."
        
        y = centered_difference_quotient(absfunc,pts)
        y_s = s.centered_difference_quotient(absfunc,pts)
        
        p,f = arrayTest(y, y_s, err_message)
        points += p*5
        feedback += f
        
        #Test 3: exponential
        exfunc = lambda x: np.exp(x)/(0.5*x**2 + 1)
        err_message = "\nIncorrect output for f(x) = e^x/(.5x^2 + 1)."
        
        y = centered_difference_quotient(exfunc,pts)
        y_s = s.centered_difference_quotient(exfunc,pts)
        
        p,f = arrayTest(y, y_s, err_message)
        points += p*5
        feedback += f
        
        score += points
        feedback += "\nScore += " + str(points)  
        
    except Exception as e:
        feedback += "\nError: " + e.message
        
    
    try: #Problem 2: 10 points
        feedback += "\n\nProblem 2 (10 points):"
        points = 0    
        
        
        f1 = lambda y: np.array([y[0]*y[1], y[1]*y[2], y[0] - y[1], 2 + y[2]**2])
        f2 = lambda y: np.array([np.cos(y[1]), np.sin(y[0]**2) + np.sin(y[1]**2), y[0], y[1]*np.exp(y[0])])
        
        #Test 1
        pt1 = np.array([1.,1.,1.]) 
        J1 = jacobian(f1, 3, 4, pt1)
        J1_s = s.jacobian(f1, 3, 4, pt1)
        err_message1 = '\nIncorrect Jacobian for f(x,y,z) = [xy, yz, x-y, 2+z^2] at point %s. Answer should be: \n%s'%(str(pt1), str(J1))
        p,f = arrayTest(J1, J1_s, err_message1)
        points += p*2.5
        feedback += f
        
        #Test 2
        pt2 = np.array([-40., 0.5, 10.])
        J2 = jacobian(f1, 3, 4, pt2)
        J2_s = s.jacobian(f1, 3, 4, pt2)
        err_message2 = '\nIncorrect Jacobian for f(x,y,z) = [xy, yz, x-y, 2+z^2] at point %s. Answer should be: \n%s'%(str(pt2),str(J2))
        p,f = arrayTest(J2, J2_s, err_message2)
        points += p*2.5
        feedback += f
        
        #Test 3
        pt3 = np.array([3.1415, 3.1415])
        J3 = jacobian(f2, 2, 4, pt3)
        J3_s = s.jacobian(f2, 2, 4, pt3)
        err_message3 = '\nIncorrect Jacobian for f(x,y,z) = [cos(y), sin(x^2), x, y*e^x] at point %s. Answer should be: \n%s'%(str(pt3),str(J3))
        p,f = arrayTest(J3, J3_s, err_message3)
        points += p*2.5
        feedback += f
        
        #Test 4
        pt4 = np.array([-15., 45.])
        J4 = jacobian(f2, 2, 4, pt4)
        J4_s = s.jacobian(f2, 2, 4, pt4)
        err_message4 = '\nIncorrect Jacobian for f(x,y,z) = [cos(y), sin(x^2), x, y*e^x] at point %s. Answer should be: \n%s'%(str(pt4),str(J4))
        p,f = arrayTest(J4, J4_s, err_message4)
        points += p*2.5
        feedback += f
        
        
        
        score += points
        feedback += "\nScore += " + str(points)  
        
        
    except Exception as e:
        feedback += "\nError: " + e.message
        
        
    try: #Problem 3: 5 points
        feedback += "\n\nProblem 3 (5 points):"
        points = 0  
        
        max_error = 1.2018346519324208e-10
        s_max_error = s.findError()
        
        rel_error = abs(max_error-s_max_error)/max_error
        if rel_error < 0.4:
            points += 5
        elif rel_error < 1.0:
            feedback += '\nNot quite it (but close!)'
            points += 3
        else:
            feedback += '\nIncorrect max error (should be on the order of 1e-10)'
            
        score += points
        feedback += "\nScore += " + str(points) 
        
    except Exception as e:
        feedback += "\nError: " + e.message
        
        
        
    try: #Problem 4: 10 points
        feedback += "\n\nProblem 4 (10 points):"
        points = 0 
        
        img = get_img('chevy.jpg')
        plt.imshow(img, cmap="gray")
        plt.show()
        G = (1.0/159)*np.array([[2,4,5,4,2],[4,9,12,9,4],[5,12,15,12,5],[4,9,12,9,4],[2,4,5,4,2]])
        Im1 = s.Filter(img, G)
        plt.imshow(Im1,cmap="gray")
        plt.show()
        p,f = grade(10)
        points += p
        feedback += f
        
        score += points
        feedback += "\nScore += " + str(points)
        
    except Exception as e:
        feedback += "\nError: " + e.message
        
        
    try: #Problem 5: 10 points
        feedback += "\n\nProblem 5 (10 points):"
        points = 0 
        
        img = get_img('chevy.jpg')
        Im2 = s.sobelFilter(img)
        plt.imshow(Im2,cmap="gray")
        plt.show()
        p,f = grade(10)
        points += p
        feedback += f
        
        score += points
        feedback += "\nScore += " + str(points)
        
    except Exception as e:
        feedback += "\nError: " + e.message        
        
    if late:    # Late submission penalty
        feedback += "\n\nHalf credit for late submission."
        feedback += "\nRaw score: " + str(score) + "/" + str(total)
        score *= .5
        
    if score > total:
        feedback += "\n\nLowest problem dropped."
        score = total
    
    # Report final score.
    feedback += "\n\nTotal score: " + str(score) + "/" + str(total)
    percentage = (100.0 * score) / total
    feedback += " = " + str(percentage) + "%"
    if   percentage >=  98.0: feedback += "\n\nExcellent!"
    elif percentage >=  90.0: feedback += "\n\nGreat job!"
    return score, feedback
        