# markov_chains.py
"""Volume II: Markov Chains.
<Name>
<Class>
<Date>
"""

import numpy as np


# Problem 1
def random_markov(n):
    """Create and return a transition matrix for a random Markov chain with
    'n' states. This should be stored as an nxn NumPy array.
    """
    raise NotImplementedError("Problem 1 Incomplete")


# Problem 2
def forecast():
    """Forecast tomorrow's weather given that today is hot."""
    transition = np.array([[0.7, 0.6], [0.3, 0.4]])

    # Sample from a binomial distribution to choose a new state.
    return np.binomial(1, transition[1, 0])


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
    raise NotImplementedError("Problem 3 Incomplete")


# Problem 4
def analyze_simulation():
    """Investigate and interpret the results of the simulations in the previous
    two problems. Specifically, find the average percentage of days that are
    hot, mild, cold, and freezing in each simulation. Does the starting day
    alter the results? Print a report of your findings (return nothing).
    """
    raise NotImplementedError("Problem 4 Incomplete")


# Problems 5 and 6
class SentenceGenerator(object):
    """Markov chain creator for simulating bad English.

    Attributes:
        (what attributes do you need to keep track of?)

    Example:
        >>> yoda = SentenceGenerator("Yoda.txt")
        >>> print yoda.babble()
        The dark side of loss is a path as one with you.
    """

    def __init__(self, filename):
        """Read the specified file and build a transition matrix from its
        contents. You may assume that the file has one complete sentence
        written on each line.
        """
        raise NotImplementedError("Problem 5 Incomplete")

    def babble(self):
        """Begin at the start sate and use the strategy from
        four_state_forecast() to transition through the Markov chain.
        Keep track of the path through the chain and the corresponding words.
        When the stop state is reached, stop transitioning and terminate the
        sentence. Return the resulting sentence as a single string.
        """
        raise NotImplementedError("Problem 6 Incomplete")

