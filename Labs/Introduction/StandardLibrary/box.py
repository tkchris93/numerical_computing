# box.py
"""Introductory Labs: The Standard Library. Auxiliary file."""

from itertools import combinations

def isvalid(roll, remaining):
    """Check to see whether or not a roll is valid. That is, check if there
    exists a combination of the entries of 'remaining' that sum up to 'roll'.

    Parameters:
        roll (int): The value of a dice roll.
        remaining (list): the list of the numbers that still need to be
            removed before the box can be shut.
    
    Returns:
        True if the roll is valid.
        False if the roll is invalid.
    """
    for i in xrange(1, len(remaining)+1):
        for combo in combinations(remaining, i):
            if sum(combo) == roll:
                return True
    return False


def parse_input(player_input, remaining):
    """Convert a string of numbers into a list of unique integers, if possible.
    Then check that each of those integers is an entry in the other list.

    Parameters:
        player_input (str): a string of integers, separated by spaces.
            The player's choices for which numbers to remove.
        remaining (list): the list of the numbers that still need to be
            removed before the box can be shut.
    
    Returns:
        A list of the integers if the input was valid.
        An empty list if the input was invalid.
    """
    try:
        choices = [int(i) for i in player_input.split()]
        if len(set(choices)) != len(choices):
            raise ValueError
        if any([number not in remaining for number in choices]):
            raise ValueError
        return choices
    except ValueError:
        return []

