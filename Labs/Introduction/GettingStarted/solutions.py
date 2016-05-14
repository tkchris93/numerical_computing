# solutions.py
"""Introductory Labs: Getting Started. Solutions file.
NOTE: For this Introductory lab, we recommend NOT providing a specifications
file so that they have to define the functions themselves.
"""

# Problem 1 (ungraded)
if __name__ == '__main__':
    print("Hello, world!")


# Problem 2
def sphere_volume(r):
    """Return the volume of the sphere of radius 'r'.
    Use 3.14159 for pi in your computation.
    """
    return (4 * 3.14159 / 3)*r**3


# Problem 3
def first_half(my_string):
    """Return the first half of the string 'my_string'. Exclude the
    middle character if there are an odd number of characters.

    Examples:
        >>> first_half("python")
        'pyt'
        >>> first_half("ipython")
        'ipy'
    """
    return my_string[:len(my_string)//2]
    
def backward(my_string):
    """Return the reverse of the string 'my_string'.
    
    Examples:
        >>> backward("python")
        'nohtyp'
        >>> backward("ipython")
        'nohtypi'
    """
    return my_string[::-1]


# Problem 4
def list_ops():
    """Define a list with the entries "ant", "bear", "cat", and "dog".
    Perform the following operations on the list:
        - Append "elephant".
        - Remove "ant"
        - Remove the entry at index 1.
        - Replace the entry at index 2 with "eagle".
        - Append "fox".
    Return the resulting list.

    Examples:
        >>> list_ops()
        ['bear', 'dog', 'eagle', 'fox']
    """
    my_list = ["ant", "bear", "cat", "dog"]
    my_list.append("elephant")
    my_list.remove("ant")
    my_list.remove(my_list[1])
    my_list[2] = "eagle"
    my_list.append("fox")
    return my_list


# Problem 5
def pig_latin(word):
    """Translate the string 'word' into Pig Latin
    
    Examples:
        >>> pig_latin("apple")
        'applehay'
        >>> pig_latin("banana")
        'ananabay'
    """
    if word[0] in "aeiou":
        return word + "hay"
    else:
        return word[1:] + word[0] + "ay"
        

# Problem 6
def int_to_string(my_list):
    """Translate 'my_list', a list of numbers 1-26, to corresponding
    lowercase letters of the alphabet. 1 -> a, 2 -> b, 3 -> c, and so on.
    
    Example:
        >>> int_to_string([13, 1, 20, 8])
        ['m', 'a', 't', 'h'] 
    """
    # Using a list comprehension.
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return [alphabet[i-1] for i in my_list]

    # Using a dictionary.
    my_dictionary = {1:'a',  2:'b',  3:'c',  4:'d',  5:'e',  6:'f',  7:'g',
                     8:'h',  9:'i', 10:'j', 11:'k', 12:'l', 13:'m', 14:'n',
                    15:'o', 16:'p', 17:'q', 18:'r', 19:'s', 20:'t', 21:'u',
                    22:'v', 23:'w', 24:'x', 25:'y', 26:'z'}
    output = []
    for number in my_list:
        output.append(my_dictionary[number])
    return output


# Problem 7
def alt_harmonic(n):
    """Return the partial sum of the first n terms of the alternating
    harmonic series. Use this function to approximae ln(2).
    """
    return sum([(-1)**(i+1)/float(i) for i in xrange(1,n)])

