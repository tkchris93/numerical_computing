# solutions.py
import numpy as np
import matplotlib.pyplot as plt


from ipyparallel import Client
client = Client()
dview = client[:]

def prob3():
    def draw():
        import numpy as np
        a = np.random.randn(1000000).astype(np.float32)
        return np.average(a), a.max(), a.min()

    result = dview.apply_sync(draw)
    means = []
    maxs = []
    mins = []
    for i in xrange(len(result)):
        means.append(result[i][0])
        maxs.append(result[i][1])
        mins.append(result[i][2])

    print "means =", means
    print "maxs =", maxs
    print "mins =", mins

def prob4(N):
    m = 500000//len(client.ids)
    def draw(N):
        import numpy as np
        a = np.random.randn(N, m).astype(np.float32)
        print a.shape
        maxs = a.max(axis=1)
        return maxs

    result = dview.apply_sync(draw, N)
    myarray = np.array(result).flatten()
    plt.hist(myarray, bins=50)
    plt.show()
    return myarray

def prob5():
    # solution coming.
    # Create a dictionary on each engine, gather the dictionaries, then create the sparse occurence matrix.
