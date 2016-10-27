# spec.py

# Problem 1: Implement this function.
def Newtons_method(f, x0, Df, iters=15, tol=.1e-5):
    '''
    Use Newton's method to approximate a zero of a function.
    Inputs:
        f (function): A function handle. Should represent a function 
            from R to R.
        x0 (float): Initial guess.
        Df (function): A function handle. Should represent the derivative
             of f.
        iters (int): Maximum number of iterations before the function
            returns. Defaults to 15.
        tol (float): The function returns when the difference between
            successive approximations is less than tol.
    Returns:
        A tuple (x, converged, numiters) with
        x (float): the approximation for a zero of f
        converged (bool): a Boolean telling whether Newton's method converged
        numiters (int): the number of iterations the method computed
    '''
    raise NotImplementedError("Problem 1 Incomplete")
        
# Problem 2.1: Implement this function.
def problemTwoOne():
    '''
    Plot f(x) = sin(x)/x - x on [-4,4].  
    Return the zero of this function to 7 digits of accuracy.
    '''
    raise NotImplementedError("Problem 2.1 Incomplete")

# Problem 2.2: Implement this function.
def problemTwoTwo():
    '''
    Return a string as to what happens and why for the function f(x) = x^(1/3) where
    x_0 = .01.
    '''
    raise NotImplementedError("Problem 2.2 Incomplete")
    
# Problem 3: Implement this function
def problemThree():
    '''
    Given P1[(1+r)**N1-1]=P2[1-(1+r)**(-N2)], if N1 = 30, N2 = 20, P1 = 2000, and P2 = 8000, use Newton's method to determine r.  
    Return r.
    '''
    raise NotImplementedError("Problem 3 Incomplete")

# Problem 4: Modify Newtons_method and implement this function
def problemFour():
    '''
    Find an alpha < 1 so that running Newtons_method() on f(x) = x**(1/3) with x0 = .01 converges. 
    Return the results of Newtons_method().
    '''
    raise NotImplementedError("Problem 4 Incomplete")
    
# Problem 5: Implement Newtons_vector() to solve Bioremediation problem
def Newtons_vector(f, x0, Df, iters = 15, tol = 1e-5, alpha = 1):
    '''
    Use Newton's method to approximate a zero of a vector valued function.
    Inputs:
        f (function): A function handle.
        x0 (list): Initial guess.
        Df (function): A function handle. Should represent the derivative
             of f.
        iters (int): Maximum number of iterations before the function
            returns. Defaults to 15.
        tol (float): The function returns when the difference between
            successive approximations is less than tol.
        alpha (float): Defaults to 1.  Allows backstepping.
    Returns:
        A tuple (x_values, y_values) where x_values and y_values are lists that contain the x and y value from each iteration of Newton's method

    '''
    raise NotImplementedError("Problem 5.1 Incomplete")

def problemFive():
    '''
    Solve the system using Newton's method and Newton's method with backtracking    
    '''
    raise NotImplementedError("Problem 5.2 Incomplete")
    
# Problem 6: Implement this function.
def plot_basins(f, Df, roots, xmin, xmax, ymin, ymax, numpoints=1000,iters=15, colormap='brg'):
    '''
    Plot the basins of attraction of f.
    INPUTS:
        f (function): Should represent a function from C to C.
        Df (function): Should be the derivative of f.
        roots (array): An array of the zeros of f.
        xmin, xmax, ymin, ymax (float,float,float,float): Scalars that define the domain
            for the plot.
        numpoints (int): A scalar that determines the resolution of the plot. Defaults to 100.
        iters (int): Number of times to iterate Newton's method. Defaults to 15.
        colormap (str): A colormap to use in the plot. Defaults to 'brg'.
    '''
    raise NotImplementedError("Problem 6 Incomplete")

# Problem 7: Implement this function.
def problemSeven():
    '''
    Run plot_basins() on the function x^3-1 on the domain [-1.5,1.5]x[-1.5,1.5].
    '''
    raise NotImplementedError("Problem 7 Incomplete")

