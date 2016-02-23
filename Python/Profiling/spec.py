"""Volume I Lab 18: Profiling and Optimizing Python Code
<Name>
<Class>
<Date>
"""

# Problem 1
def compare_timings(f, g, *args):
    """Compares the timings of 'f' and 'g' with arguments '*args'.

    Inputs:
        f (callable): first function to compare.
        g (callable): second function to compare.
        *args (any type): arguments to use when callings functions
            'f' and 'g'
    Returns:
        comparison (string): The comparison of the runtimes of functions
            'f' and 'g' in the following format :
                Timing for <f>: <time>
                Timing for <g>: <time>
            where the values inside <> vary depending on the inputs)
    """
    raise NotImplementedError("Problem 1 incomplete")

# Problem 2
def LU(A):
    """Returns the LU decomposition of a square matrix."""
    n = A.shape[0]
    U = np.array(np.copy(A), dtype=float)
    L = np.eye(n)
    for i in range(1,n):
        for j in range(i):
            L[i,j] = U[i,j]/U[j,j]
            for k in range(j,n):
                U[i,k] -= L[i,j] * U[j,k]
    return L,U

def LU_opt(A):
    """Returns the LU decomposition of a square matrix."""
    raise NotImplementedError("Problem 2 incomplete")

def compare_LU(A):
    """Prints a comparison of LU and LU_opt with input of the matrix A."""
    raise NotImplementedError("Problem 2 incomplete")

# Problem 3
def mysum(X):
    """Return the sum of the elements of X.
    Inputs:
        X (array) - a 1-D array
    """
    raise NotImplementedError("Problem 3 incomplete")

def compare_sum(X):
    """Prints a comparison of mysum and sum and prints a comparison
    of mysum and np.sum."""
    raise NotImplementedError("Problem 3 incomplete")

# Problem 4
def fib(n):
    """A generator that yields the first n Fibonacci numbers."""
    raise NotImplementedError("Problem 4 incomplete")

# Problem 5
def foo(n):
    """(A part of this Problem is to be able to figure out what this
    function is doing. Therefore, no details are provided in
    the docstring.)
    """
    my_list = []
    for i in range(n):
        num = np.random.randint(-9,9)
        my_list.append(num)
    evens = 0
    for j in range(n):
        if j%2 == 0:
            evens += my_list[j]
    return my_list, evens

# Problem 5
def foo_opt(n):
    """An optimized version of 'foo'"""
    raise NotImplementedError("Problem 5 incomplete")

def compare_foo(n):
    """Prints a comparison of foo and foo_opt"""
    raise NotImplementedError("Problem 5 incomplete")

# Problem 6
def pymatpow(X, power):
    """ Return X^{power}.

    Inputs:
        X (array) - A square 2-D NumPy array
        power (int) - The power to which we are taking the matrix X.
    Returns:
        prod (array) - X^{power}
    """
    prod = X.copy()
    temparr = np.empty_like(X[0])
    size = X.shape[0]
    for n in xrange(1, power):
        for i in xrange(size):
            for j in xrange(size):
                tot = 0.
                for k in xrange(size):
                    tot += prod[i,k] * X[k,j]
                temparr[j] = tot
            prod[i] = temparr
    return prod

def numba_matpow(X, power):
    """ Return X^{power}. Compiled using Numba.

    Inputs:
        X (array) - A square 2-D NumPy array
        power (int) - The power to which we are taking the matrix X.
    Returns:
        prod (array) - X^{power}
    """
    raise NotImplementedError("Problem 6 incomplete")

def numpy_matpow(X, power):
    """ Return X^{power}.

    Inputs:
        X (array) - A square 2-D NumPy array
        power (int) - The power to which we are taking the matrix X.
    Returns:
        prod (array) - X^{power}
    """
    raise NotImplementedError("Problem 6 incomplete")

def compare_matpow(X, power):
    """Prints a comparison of pymatpow and numba_matpow and prints a
    comparison of pymatpow and numpy_matpow"""
    raise NotImplementedError("Problem 6 incompelete")

# Problem 7
def pytridiag(a,b,c,d):
    """Solve the tridiagonal system Ax = d where A has diagonals a, b, and c.

    Inputs:
        a, b, c, d (array) - All 1-D NumPy arrays of equal length.
    Returns:
        x (array) - solution to the tridiagonal system.
    """
    n = len(a)

    # Make copies so the original arrays remain unchanged
    aa = np.copy(a)
    bb = np.copy(b)
    cc = np.copy(c)
    dd = np.copy(d)

    # Forward sweep
    for i in xrange(1, n):
        temp = aa[i]/bb[i-1]
        bb[i] = bb[i] - temp*cc[i-1]
        dd[i] = dd[i] - temp*dd[i-1]

    # Back substitution
    x = np.zeros_like(a)
    x[-1] = dd[-1]/bb[-1]
    for i in xrange(n-2, -1, -1):
        x[i] = (dd[i]-cc[i]*x[i+1])/bb[i]

    return x

def init_tridiag(n):
    """Initializes a random nxn tridiagonal matrix A.

    Inputs:
        n (int) : size of array

    Returns:
        a (1-D array) : (-1)-th diagonal of A
        b (1-D array) : main diagonal of A
        c (1-D array) : (1)-th diagonal of A
        A (2-D array) : nxn tridiagonal matrix defined by a,b,c.
    """
    a = np.random.random_integers(-9,9,n).astype("float")
    b = np.random.random_integers(-9,9,n).astype("float")
    c = np.random.random_integers(-9,9,n).astype("float")

    a[a==0] = 1
    b[b==0] = 1
    c[c==0] = 1

    A = np.zeros((b.size,b.size))
    np.fill_diagonal(A,b)
    np.fill_diagonal(A[1:,:-1],a[1:])
    np.fill_diagonal(A[:-1,1:],c)
    return a,b,c,A

def numba_tridiag(a,b,c,d):
    """Solve the tridiagonal system Ax = d where A has diagonals a, b, and c.

    Inputs:
        a, b, c, d (array) - All 1-D NumPy arrays of equal length.
    Returns:
        x (array) - solution to the tridiagonal system.
    """
    raise NotImplementedError("Problem 7 incomplete")

def compare_tridiag():
    """Prints a comparison of numba_tridiag and pytridiag and prints
    a comparison of numba_tridiag and scipy.linalg.solve."""
    raise NotImplementedError("Problem 7 incomplete")

# Problem 8
def compare_old():
    """Prints a comparison of an old algorithm from a previous lab
    and the optimized version."""
    raise NotImplementedError("Problem 8 incomplete")
