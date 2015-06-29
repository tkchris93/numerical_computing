# WordList.py
"""Volume II Lab 4: Data Structures 1 (Auxiliary file)
    Do not modify this file in any way.
"""

import numpy as np

# Use this function in problem 6 to implement sort().
def create_word_list(filename='English.txt'):
    """Read in a list of words from the specified file.
    Randomize the ordering and return the list.
    """
    file = open(filename, 'r')      # open the file with read-only access
    file = file.read()              # read in each line (and close file)
    file = file.split('\n')         # strip off the endline characters
    file = file[:-1]                # remove the last endline
                                    # randomize, convert to a list, and return.
    return list(np.random.permutation(file))

# You do not need this function, but read it anyway.
def export_word_list(words, outfile='Test.txt'):
    """Write a list of words to the specified file. You are not required to use
    this function, but it may be useful in testing sort().
    
    Take note of how file input / output works in Python. The concept will
    resurface many times in later labs.
    """
    file = open(outfile, 'w'        # open the file with write-only access
    for w in words:                 # write each word to the file, appending
        file.write(w + '\n')        #   an endline character after each word
    f.close()                       # close the file.