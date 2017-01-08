import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn import decomposition
from scipy import linalg as la


iris = load_iris()

def iris_base():
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, aspect='equal')

    plt.plot(iris.data[50:150,0], iris.data[50:150,2], 'k.')
    plt.xlim([2, 8])
    plt.ylim([2, 8])
    plt.xlabel(r"Sepal Length (cm)")
    plt.ylabel(r"Petal Length (cm)")

    return fig

def ibase():
    iris_base()
    plt.savefig('iris0.pdf')
    plt.clf()

def iris1():
    fig = iris_base()

    pca = decomposition.PCA(n_components=2)
    pca.fit(iris.data[50:150, np.array([0, 2])])
    mean = np.mean(iris.data[50:150, np.array([0, 2])], 0)
    stds = np.std(iris.data[50:150, np.array([0, 2])], 0)
    components = pca.components_

    plt.quiver(mean[0], mean[1], 1.5 * stds[0], 0, scale_units='xy', angles='xy', scale=1)
    plt.quiver(mean[0], mean[1], 0, 1.5 * stds[1], scale_units='xy', angles='xy', scale=1)
    plt.savefig('iris1.pdf')
    plt.clf()

def iris2():
    fig = iris_base()

    pca = decomposition.PCA(n_components=2)
    pca.fit(iris.data[50:150, np.array([0, 2])])
    mean = np.mean(iris.data[50:150, np.array([0, 2])], 0)
    stds = np.std(iris.data[50:150, np.array([0, 2])], 0)
    components = pca.components_
    variance_ratio = pca.explained_variance_ratio_

    plt.quiver(mean[0], mean[1],
               -2 * variance_ratio[0] * components[0,0], 
               -2 * variance_ratio[0]*components[0,1],
               scale_units='xy', angles='xy', scale=1)
    plt.quiver(mean[0], mean[1], 
               5 * variance_ratio[1] * components[1,0], 
               5 * variance_ratio[1] * components[1,1], 
               scale_units='xy', angles='xy', scale=1)
    plt.savefig('iris2.pdf')
    plt.clf()
    
def iris_pca():
    X = iris.data
    # pre-process
    Y = X - X.mean(axis=0)
    # get SVD
    U,S,VT = la.svd(Y,full_matrices=False)
    # project onto the first two principal components
    Yhat = U[:,:2].dot(np.diag(S[:2]))
    # plot results
    setosa = iris.target==0
    versicolor = iris.target==1
    virginica = iris.target==2
    p1, p2 = Yhat[:,0], Yhat[:,1]
    plt.scatter(p1[setosa],p2[setosa], marker='.', color='blue', label='Setosa')
    plt.scatter(p1[versicolor],p2[versicolor], marker='.', color='red', label='Versicolor')
    plt.scatter(p1[virginica],p2[virginica], marker='.', color='green', label='Virginica')
    plt.legend(loc=2)
    plt.ylim([-4,5])
    plt.xlim([-4,4])
    plt.xlabel("First Principal Component")
    plt.ylabel("Second Principal Component")
    plt.savefig('iris_pca.pdf')
    plt.clf()

def iris_scree():
    X = iris.data
    # pre-process
    Y = X - X.mean(axis=0)
    # get SVD
    U,S,VT = la.svd(Y,full_matrices=False)
    L = S**2
    plt.plot(L/L.sum(dtype=float), 'o-')
    plt.xlabel("Principal Components")
    plt.ylabel("Percentage of Variance")
    plt.savefig('iris_scree.pdf')
    plt.clf()
    


if __name__ == "__main__":
    iris_scree()
    iris_pca()
