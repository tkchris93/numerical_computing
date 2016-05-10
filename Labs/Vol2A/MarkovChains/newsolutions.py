# newsolutions.py
"""Volume II: Markov Chains. Solutions file."""

import numpy as np
# from scipy.sparse import lil_matrix
# from sklearn.preprocessing import normalize

# Problem 1
def random_markov(n):
    """Create a transition matrix for a random Markov chain with n states.
    This should be stored as an nxn numpy array. The columns sum to 1.
    """
    transition_matrix = np.empty((n,n))
    for j in range(n):
        column = np.random.random(n)
        column /= column.sum()
        transition_matrix[:,j] = column
    return transition_matrix


# Problem 2
def forecast(num_days):
    """Run a simulation for the weather over 'num_days' days, with
    'hot' as the starting state. Return a list containing the day-by-day
    results, not including the starting day.

    Example:
        >>> forecast(3)
        [1, 1, 0]

        # Or, if you prefer,
        >>> forecast(5)
        ['cold', 'hot', 'hot', 'cold', 'cold']
    """
    transition_matrix = np.array([[.7, .6], [.3, .4]])
    current_state = 0
    record = []
    for day in xrange(num_days):
        random_number = np.random.random()
        if random_number < transition_matrix[1, current_state]:
            current_state = 1
        else:
            current_state = 0
        record.append(current_state)
    return record
# Roughly 66.7% of the entries should be zeros.
# Roughly 33.3% of the entries should be ones.


# Problem 3
def four_state_forecast(days=1):
    transition = np.array([ [.5, .3, .1, 0.],
                            [.3, .3, .3, .3],
                            [.2, .3, .4, .5],
                            [0., .1, .2, .1]    ])
    current_state = 0
    record = []
    for day in xrange(days):
        current_state = np.argmax(
                    np.random.multinomial(1, transition[:,current_state]))
        record.append(current_state)
    return record
# Roughly 24.6% of the entries should be zeros.
# Roughly 30.1% of the entries should be ones.
# Roughly 33.2% of the entries should be twos.
# Roughly 12.1% of the entries should be threes.


# Problem 4
def analyze_simulation():
    """Analyze the results of the previous two problems."""
    hot1, cold1, hot2, mild, cold2, frozen  = [], [], [], [], [], []
    for i in xrange(10):
        f2 = forecast(10000)
        f4 = four_state_forecast(10000)
        hot1.append(f2.count(0))
        cold1.append(f2.count(1))
        hot2.append(f4.count(0))
        mild.append(f4.count(1))
        cold2.append(f4.count(2))
        frozen.append(f4.count(3))
    print("2-state forecast Hot days:\t{}%".format(np.mean(hot1)/100.))
    print("2-state forecast Cold days:\t{}%".format(np.mean(cold1)/100.))
    print("4-state forecast Hot days:\t{}%".format(np.mean(hot2)/100.))
    print("4-state forecast Mild days:\t{}%".format(np.mean(mild)/100.))
    print("4-state forecast Cold days:\t{}%".format(np.mean(cold2)/100.))
    print("4-state forecast Freezing days:\t{}%".format(np.mean(frozen)/100.))


class SentenceGenerator(object):
    """Note: This implementation is ROW STOCHASTIC!!!

    Example:
        >>> yoda = SentenceGenerator("Yoda.txt")
        >>> print yoda.babble()
        The dark side of loss is a path as one with you.
    """

    def __init__(self, filename=None):
        if filename is not None:
            self._read(filename)

    def _read(self, filename, sparse=False): # TODO: take sparse out? Optional?
        self.filename = filename
        self.states = ["$tart"]
        
        # Initialize an empty transition matrix.
        with open(self.filename, 'r') as source:
            self.num_states = len(set(source.read().split())) + 2
        # if sparse:
            # self.chain = lil_matrix((self.num_states, self.num_states))
        # else:
        self.chain = np.zeros((self.num_states, self.num_states))

        # Process the data.
        with open(self.filename, 'r') as source:
            for line in source:
                sentence = line.split()
                
                for word in sentence:
                    if word not in self.states:
                        self.states.append(word)
                index = [self.states.index(word) for word in sentence]
                
                self.chain[0, index[0]] += 1                # &tart -> first
                for i in xrange(len(index)-1):
                    self.chain[index[i], index[i+1]] += 1   # middle -> next
                self.chain[index[-1], -1] += 1              # last -> en&
        
        self.chain[-1, -1] = 1

        # Make each row sum to 1.
        # if sparse:
            # self.chain = normalize(self.chain, norm="l1", axis=1)
        # else:
        self.chain /= self.chain.sum(axis=1)[:,np.newaxis]

    def babble(self):
        stop = self.num_states - 1
        output = ""
        state = 0
        while state != stop:
            if state != 0:
                output += " "
            # Tranisition to a new state.
            state = np.argmax(np.random.multinomial(1, self.chain[state]))
            # TODO: transitions don't quite work yet with sparse matrices.
            # Record the corresponding word.
            if state != stop:
                output += self.states[state]
        return output 


if __name__ == '__main__':
    analyze_simulation()
    yoda = SentenceGenerator("Yoda.txt")
    for i in xrange(5):
        print yoda.babble()
