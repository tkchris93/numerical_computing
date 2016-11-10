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
        maxs = a.max(axis=1)
        return maxs

    result = dview.apply_sync(draw, N)
    myarray = np.array(result).flatten()
    plt.hist(myarray, bins=50)
    plt.show()
    return myarray

def prob5():
    def create_occurrence_dict():
        occur_dict = dict()
        for doc in batch:
            processed_words = []

            # get a list of words
            with open(doc, 'r') as f:
                lines = f.read()
            words = lines.strip().lower().split(' ')
            for w in words:
                if w not in stopwords_set:
                    processed_words.append(w)

            occur_dict[doc] = dict()
            for w in processed_words:
                if w not in occur_dict[doc].keys():
                    occur_dict[doc][w] = 1
                else:
                    occur_dict[doc][w] += 1

        return occur_dict

    from nltk.corpus import stopwords
    from os import walk
    import scipy.sparse as spar

    stopwords_set = set(stopwords.words('english'))
    stopwords_set.add("")

    for (dirname, dirpath, filename) in walk("state_union"):
        doc_batch = ["/home/tanner/Work/DevTeam/numerical_computing/Vol3B/Parallel1/state_union/" + f for f in filename]

    dview.scatter("batch", doc_batch)
    dictionaries = dview.apply_sync(create_occurrence_dict)

    vocab = []
    for d in dictionaries:
        for doc in d.keys():
            vocab += d[doc].keys()

    vocab = sorted(list(set(vocab)))

    occur_matrix = spar.csr_matrix((len(filename), len(vocab))).tolil()
    for d in dictionaries:
        for i, doc in enumerate(sorted(d.keys())):
            for j, word in enumerate(sorted(d[doc].keys())):
                occur_matrix[i,j] += d[doc][word]
    return occur_matrix.tocsr()
