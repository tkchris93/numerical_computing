# solutions.py
import numpy as np
from matplotlib import pyplot as plt

# Problem 1: Implement this function.
def Newtons_method(f, x0, Df, iters=15, tol=.1e-5, alpha = 1):
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
    xold = x0
    for numiters in range(1,iters+1):
        xnew = xold-alpha*f(xold)*1./Df(xold)
        if abs(xnew-xold)<tol:
            return xnew,True,numiters
        else:
            xold = xnew
    return xnew,False,numiters
        

# Problem 2.1: Implement this function.
def problemTwoOne():
    '''
    Plot f(x) = sin(x)/x - x on [-4,4].  
    Return the zero of this function to 7 digits of accuracy.
    '''
    f = lambda x : (1.*np.sin(x))/x - x
    df = lambda x : -1*(x**2+np.sin(x)-x*np.cos(x))/(x**2)
    x = np.linspace(-4,4,num=100)
    plt.plot(x,f(x))
    plt.show()
    xnew,converged,numiters = Newtons_method(f,1,df,tol = .0000001)
    return xnew

# Problem 2.2: Implement this function.
def problemTwoTwo():
    '''
    Return a string as to what happens and why for the function f(x) = x^(1/3) where
    x_0 = .01.
    '''
    f = lambda x: np.sign(x)*np.power(np.abs(x), 1./3)
    df = lambda x :1./3./np.power(np.abs(x), 2./3)
    xnew,converged,numiters = Newtons_method(f,.01,df)
    return "The values are getting further and further away from the correct value so it never converges.  Because the derivative at the root is infinity."

# Problem 3: Implement this function
def problemThree():
    '''
    Given P1[(1+r)**N1-1]=P2[1-(1+r)**(-N2)], if N1 = 30, N2 = 20, P1 = 2000, and P2 = 8000, use Newton's method to determine r.  
    Return r.
    '''
    f =  lambda r: 2000*((1+r)**30-1)-8000*(1-1./(1+r)**20)
    Df = lambda r: 30*2000*(1+r)**29 - 8000*20./(1+r)**21
    x0 = 0.5
    xnew,converged,numiters = Newtons_method(f,x0,Df)
    return xnew

# Problem 4: Modify Newtons_method and implement this function
def problemFour():
    '''
    Find an alpha < 1 so that running Newtons_method() on f(x) = x**(1/3) with x0 = .01 converges. 
    Return the results of Newtons_method().
    '''
    f = lambda x: np.sign(x)*np.power(np.abs(x), 1./3)
    df = lambda x :1./3./np.power(np.abs(x), 2./3)
    return Newtons_method(f,.01,df, alpha = .25)
    
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
    x_old = x0
    x_val = [x_old[0]]
    y_val = [x_old[1]]
    
    for x in xrange(iters):
        x_new = np.array([x_old]).T - alpha*np.linalg.inv(Df(x_old)).dot(f(x_old))
        if np.linalg.norm(x_new-np.array([x_old]).T) < tol:
            return x_val, y_val
        else:
            x_old = [x_new[0,0],x_new[1,0]]
            x_val.append(x_old[0])
            y_val.append(x_old[1])
    
    return x_val, y_val


def problemFive():
    '''
    Solve the system using Newton's method and Newton's method with backtracking    
    '''
    DF = lambda x: np.array([[4*x[1]-1, 4*x[0]],[-x[1], -x[0]-2*x[1]]])
    F = lambda x: np.array([[4*x[0]*x[1]-x[0]], [-x[0]*x[1]+1-x[1]**2]])
    x, y = Newtons_vector(F, [-.2,.2], DF, alpha = .25, iters = 12)
    x1, y1  = Newtons_vector(F, [-.2,.2], DF, alpha = 1)
    
    plt.scatter(x,y, color = 'b')
    plt.plot(x, y, color = 'b', linewidth = 3)
    plt.scatter(x1, y1, color = 'r')
    plt.plot(x1, y1, color = 'r')
    
    #Create contour plot
    n=400
    xran = np.linspace(-7,8,n)
    yran = np.linspace(-6,6,n)
    X, Y = np.meshgrid(xran,yran)
    F = -X*Y+1-Y**2
    G = 5*X*Y-X*(1+Y)
    plt.contour(X, Y, F, [-4,-2,0,2,4,6],cmap=plt.get_cmap('afmhot'))
    plt.contour(X, Y, G ,0,cmap=plt.get_cmap('afmhot')) 
    plt.xlim(-6,8)
    plt.ylim(-6,6)
    plt.show()
    
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
    xreal = np.linspace(xmin,xmax,numpoints)
    ximag = np.linspace(ymin,ymax,numpoints)
    Xreal,Ximag = np.meshgrid(xreal,ximag)
    Xold = Xreal + 1j*Ximag
    for numiters in xrange(iters):
        x = Xold - 1.* f(Xold)/Df(Xold)
        Xold = x

    convergedarray = np.zeros(Xold.shape)
    for i in range(Xold.shape[0]):
        for j in range(Xold.shape[1]):
            convergedarray[i,j] = np.abs(roots-x[i,j]).argmin()
    plt.pcolormesh(Xreal,Ximag,convergedarray,cmap=colormap)
    plt.show()
    

# Problem 7: Implement this function.
def problemSeven():
    '''
    Run plot_basins() on the function x^3-1 on the domain [-1.5,1.5]x[-1.5,1.5].
    '''
    f = lambda x : x**3 - 1
    Df = lambda x : 3*x**2
    roots = np.array([1,-1j**(1./3),1j**(2./3)])
    xmin = -1.5
    xmax = 1.5
    ymin = -1.5
    ymax = 1.5
    plot_basins(f,Df,roots,xmin,xmax,ymin,ymax)

def testing():
    f = lambda x : x**3-x
    Df = lambda x : 3*x**2 - 1
    roots = np.array([0,1,-1])
    xmin = -1.5
    xmax = 1.5
    ymin = -1.5
    ymax = 1.5
    plot_basins(f,Df,roots, xmin,xmax,ymin,ymax)

if __name__ == '__main__':
    print "Problem 2.1:"
    print problemTwoOne()
    print "Problem 2.2:"
    print problemTwoTwo()
    print "Problem 3:"
    print problemThree()
    print "Problem 4:"
    print problemFour()
    print "Problem 5:"
    print problemFive()
    print "Problem 7:"
    print problemSeven()
    #print testing()
