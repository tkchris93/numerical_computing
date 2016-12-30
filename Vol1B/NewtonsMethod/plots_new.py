import matplotlib.pyplot as plt
import numpy as np
import sys

def Newtons_method_vector(f, x0, Df, iters = 15, tol = 1e-5, alpha = 1):
    x_old = x0

    x_val = [x_old[0]]
    y_val = [x_old[1]]

    #Do Newton's method for the specified amount of iterations
    for x in xrange(iters):
        x_new = np.array([x_old]).T - alpha*np.linalg.inv(Df(x_old)).dot(f(x_old))

        #if already within the tolerance, break from the iterations
        if np.linalg.norm(x_new-np.array([x_old]).T) < tol:
            return x_val, y_val

        else:
            x_old = [x_new[0,0],x_new[1,0]]
            x_val.append(x_old[0])
            y_val.append(x_old[1])

    return x_val, y_val

def plot_contour():
    DF = lambda x: np.array([[4*x[1]-1, 4*x[0]],[-x[1], -x[0]-2*x[1]]])
    F = lambda x: np.array([[4*x[0]*x[1]-x[0]], [-x[0]*x[1]+1-x[1]**2]])

    x, y = Newtons_method_vector(F, [-.2,.2], DF, alpha = .25, iters = 13, tol = 1e-2)
    x1, y1 = Newtons_method_vector(F, [-.2,.2], DF, alpha = 1, iters = 6)


    plt.scatter(x,y, color = 'b')
    plt.plot(x, y, color = 'b', linewidth = 3)
    plt.scatter(x1, y1, color = 'r')
    plt.plot(x1, y1, color = 'r')

    for i in range(len(x1)-2):
        plt.annotate(str(i), xy = (x1[i],y1[i]))
    for j in [1, 2, len(x)-1]:
        plt.annotate(str(j), xy = (x[j],y[j]))

    #Create contour plot
    n=400
    xran = np.linspace(-7,8,n)
    yran = np.linspace(-6,6,n)
    X, Y = np.meshgrid(xran,yran)
    F = -X*Y+1-Y**2
    plt.contour(X, Y, F, [-4,-2,0,2,4,6],cmap=plt.get_cmap('afmhot'))
    plt.contour(X, Y, 5*X*Y-X*(1+Y),0,cmap=plt.get_cmap('afmhot'))
    plt.xlim(-6,8)
    plt.ylim(-6,6)
    plt.plot()
    plt.savefig('figures/contour.pdf', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    plot_contour()
