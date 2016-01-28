import numpy as np
from cython_ctridiag import cytridiag as ctri

def init_tridiag(n):
    a = np.random.random_integers(-9,9,n).astype("float")
    b = np.random.random_integers(-9,9,n).astype("float")
    c = np.random.random_integers(-9,9,n).astype("float")
    
    A = np.zeros((b.size,b.size))
    np.fill_diagonal(A,b)
    np.fill_diagonal(A[1:,:-1],a)
    np.fill_diagonal(A[:-1,1:],c)
    return a,b,c,A
    
if __name__ == "__main__":
    n = 10
    a,b,c,A = init_tridiag(n)
    d = np.random.random_integers(-9,9,n).astype("float")
    dd = np.copy(d)
    
    ctri(a,b,c,d)
    
    if np.abs(A.dot(d) - dd).max() < 1e-12:
        print "Test Passed"
    else:
        print "Test Failed"
