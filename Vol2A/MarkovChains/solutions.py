# solutions.py
"""Volume II: Markov Chains. Solutions file."""

import numpy as np
from scipy import linalg as la


# Problem 1
def random_markov(n):
    """Create and return a transition matrix for a random Markov chain with
    'n' states. This should be stored as an nxn NumPy array.
    """
    transition_matrix = np.random.random((n,n))
    return transition_matrix / transition_matrix.sum(axis=0)


# Problem 2
def forecast(days):
    """Run a simulation for the weather over the specified number of days,
    with hot as the starting state. Return a list containing the day-by-day
    results, not including the starting day.

    Examples:
        >>> forecast(3)
        [1, 1, 0]
        >>> forecast(5)
        [0, 0, 0, 1, 0]
    """
    transition = np.array([[.7, .6], [.3, .4]])
    state = 0
    record = []
    for day in xrange(days):
        state = np.random.binomial(1, transition[1, state])
        record.append(state)
    return record


# Problem 3
def four_state_forecast(days):
    """Run a simulation for the weather over the specified number of days,
    with mild as the starting state, using the four-state Markov chain.
    Return a list containing the day-by-day results, not including the
    starting day.

    Examples:
        >>> four_state_forecast(3)
        [0, 1, 3]
        >>> four_state_forecast(5)
        [2, 1, 2, 1, 1]
    """
    transition = np.array([ [.5, .3, .1, 0.],
                            [.3, .3, .3, .3],
                            [.2, .3, .4, .5],
                            [0., .1, .2, .2]])
    state = 0
    record = []
    for day in xrange(days):
        state = np.argmax(np.random.multinomial(1, transition[:,state]))
        record.append(state)
    return record


# Problem 4
def steady_state(A, tol=1e-12, N=40):
    """Compute the steady state of the transition matrix A.

    Inputs:
        A ((n,n) ndarray): A column-stochastic transition matrix.
        tol (float): The convergence tolerance.
        N (int): The maximum number of iterations to compute.

    Raises:
        ValueError: if the iteration does not converge within N steps.

    Returns:
        x ((n,) ndarray): The steady state distribution vector of A.
    """
    # Generate a random initial state distribution vector.
    x = np.random.random(A.shape[0])
    x /= x.sum()

    # Run the iteration until convergence.
    for i in xrange(N):
        x1 = np.dot(A, x)
        if la.norm(x - x1) < tol:
            return x1
        x = x1

    # Raise an exception after N iterations without convergence.
    raise ValueError("Iteration did not converge")


class SentenceGenerator(object):
    """Markov chain creator for simulating bad English.

    Attributes:
        (what attributes do you need to keep track of?)

    Example:
        >>> yoda = SentenceGenerator("Yoda.txt")
        >>> print(yoda.babble())
        The dark side of loss is a path as one with you.
    """

    # Problem 5
    def __init__(self, filename):
        """Read the specified file and build a transition matrix from its
        contents. You may assume that the file has one complete sentence
        written on each line.
        """
        self.filename = filename
        self.states = ["$tart"]

        # Initialize an empty transition matrix of the appropriate size.
        with open(self.filename, 'r') as source:
            self.num_states = len(set(source.read().split())) + 2
        self.chain = np.zeros((self.num_states, self.num_states))

        # Process the data. This assumes one sentence per line in the file.
        with open(self.filename, 'r') as source:
            for line in source:
                sentence = line.split()

                for word in sentence:
                    if word not in self.states:
                        self.states.append(word)
                indices = [self.states.index(word) for word in sentence]

                self.chain[indices[0], 0] += 1                 # $tart -> first
                for i in xrange(len(indices)-1):
                    self.chain[indices[i+1], indices[i]] += 1  # middle -> next
                self.chain[-1, indices[-1]] += 1               # last -> $top

        self.chain[-1, -1] = 1.
        self.states.append("$top")

        # Make each column sum to 1.
        self.chain /= self.chain.sum(axis=0)

    # Problem 6
    def babble(self):
        """Begin at the start sate and use the strategy from
        four_state_forecast() to transition through the Markov chain.
        Keep track of the path through the chain and the corresponding words.
        When the stop state is reached, stop transitioning and terminate the
        sentence. Return the resulting sentence as a single string.
        """
        stop = self.num_states - 1
        path = []
        state = np.argmax(np.random.multinomial(1, self.chain[:,0]))

        # Begin at the start state and end at the stop state.
        while state != stop:
            path.append(self.states[state])
            state = np.argmax(np.random.multinomial(1, self.chain[:,state]))

        return " ".join(path)
