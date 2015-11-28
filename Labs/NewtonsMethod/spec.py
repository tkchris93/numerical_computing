# spec.py

# Problem 1.1: Implement this function.
def Newtons_method(f, x0, Df, iters=15, tol=.002):
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

# Problem 1.2: Implement this function.
def problemOneTwo():
    '''
    Return a tuple of the number of iterations to get 5 digits of accuracy
    for f = cos(x) with x_0 = 1 and x_0 = 2.
    '''

# Problem 1.3: Implement this function.
def problemOneThree():
    '''
    Plot f(x) = sin(x)/x - x on [-4,4].  Return the zero of this function to
    7 digits of accuracy.
    '''

# Problem 1.4: Implement this function.
def problemOneFour():
    '''
    Return a tuple of
    1. The number of iterations to get 2 digit of accuracy for f(x) = x^9
        with x_0 = 1.
    2. A string with the reason to why you think the convergence is slow for 
        this function.
    '''

# Problem 1.5: Implement this function.
def problemOneFive():
    '''
    Return a string as to what happens and why for the function f(x) = x^(1/3) where
    x_0 = .01.
    '''

# Problem 2 (Optional): Modify the function Newtons_method() to calculate the numerical
# derivative of f using centered coefficients.


# Problem 3.1: Implement this function.
def plot_basins(f, Df, roots, xmin, xmax, ymin, ymax, numpoints=100,iters=15, colormap='brg'):
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

# Problem 3.2: Implement this function.
def problemThreeTwo():
    '''
    Run plot_basins() on the function x^3-1 on the domain [-1.5,1.5]x[-1.5,1.5].
    '''