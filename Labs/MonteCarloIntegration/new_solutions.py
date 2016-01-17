# solutions.py
import numpy as np

def prob1(numPoints=500000):
    points = np.random.rand(3, numPoints)
    points = points*2 - 1
    circleMask = [la.norm(points[:,1]) for i in xrange(numPoints)]
    numInCircle = np.sum(circleMask)
    return 8.*numInCircle/numPoints
    

