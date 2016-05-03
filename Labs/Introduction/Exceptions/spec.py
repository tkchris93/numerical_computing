# solution.py
"""Introductory Labs: Exceptions and File I/O Protocol.
<Name>
<Class>
<Date>
"""

# Problem 1
def my_func(a, b, c, d, e):
    print("The first argument is " + a)
    x = sum([b, c])
    y = d + e    
    return a, x, y


# Problem 2
def random_walk(max_iters=1e9):
    walk = 0
    direction = [-1, 1]
    for i in xrange(max_iters):
        walk += choice(direction)
    return walk


