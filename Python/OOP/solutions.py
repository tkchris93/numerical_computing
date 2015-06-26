# solutions.py
""" Volume II Lab 2: Object Oriented Programming
    Main solutions file. See also 'Backpack_solutions.py' and 'Knapsack.py'.
    Use the test() method as a test script.
    Written by Shane McQuarrie, Spring 2015.
"""

# Students should have their 'Backpack' class in a 'Backpack.py' file and
#   import it with the following line:
# from Backpack import Backpack


# Problem 1: Modify constructor to include name, max_size. Modify put() to
#   contents size from exceeding max_size. Write dump(). (Problem 3 below)
class Backpack(object):
    """Backpack object. Has a color, name, maximum size, and a list of contents.
    
    Attributes:
        color (str): the color of the backpack.
        name (str): the name of the backpack.
        max_size (int): the maximum number of items that can fit in the
            backpack.
        contents (list): the contents of the backpack.
    """

    def __init__(self,color='black',name='backpack',max_size=5):
        """Constructor for a backpack object. Set the color, name, and max size
        of the backpack. Also initialize the contents list.
        
        Inputs:
            color (str, opt): the color of the backpack. Defaults to 'black'.
            name (str, opt): a label for the backpack. Defaults to 'backpack'.
            max_size (int, opt): the maximum number of items that can fit in
                the backpack. Defaults to 5.
        
        Returns:
            A backpack object wth no contents.
        """
        
        self.color = color
        self.name = name
        self.max_size = max_size
        self.contents = []
    
    def put(self,item):
        """Add an item to the backpack content list if there is room."""
        if len(self.contents) >= self.max_size:         # Check for overflow
            print "Backpack Full."
        else:
            self.contents.append(item)
    
    def take(self, item):
        """Remove an item from the backpack."""
        self.contents.remove(item)
    
    def dump(self):
        """Remove all items from the backpack."""
        self.contents = []
    
    def __add__(self, other):
        """Add the contents of 'other' to the contents of 'self'. Note that the
        contents of 'other' are unchanged.
        """
        self.contents = self.contents + other.contents
    
    def __lt__(self,other):
        return len(self.contents) < len(other.contents)
    
    # Problem 3: Write the __str__ and __eq__ methods for the Backpack class
    def __str__(self):
        """String Representation.
        Examples:
            >>> b = Backpack()             |    Or,
            >>> b.put('something')         |
            >>> b.put('something else')    |    >>> c = Backpack('red','Bob',3)
            >>> print(b)                   |    >>> print(c)
            Name:       backpack           |    Name:       Bob
            Color:      black              |    Color:      red
            Size:       2                  |    Size:       0
            Max Size:   5                  |    Max Size:   3
            Contents:                      |    Contents:   Empty
                        something          |
                        something else     |
        """
        out = "Name:\t\t" + self.name
        out += "\nColor:\t\t" + self.color
        out += "\nSize:\t\t" + str(len(self.contents))
        out += "\nMax Size:\t" + str(self.max_size)
        out += "\nContents:"
        if len(self.contents) == 0: out += "\tNone"     # Empty list
        else:                                           # Nonempty list
            for i in xrange(len(self.contents)):
                out += "\n\t\t" + str(self.contents[i])
        return out
    
    def __eq__(self,other):
        """Two backpack objects are equal if and only if they have the same
        name, color, and contents. Note that the contents do not need to be
        in the same order for the contents to be the same.
        """
        if self.name != other.name: return False        # Check name
        if self.color != other.color: return False      # Check color
        if len(self.contents) != len(other.contents): return False
        l1 = self.contents                              # Check contents:
        l2 = other.contents                             #  first list size, then
        l1.sort()                                       #  sort for comparison
        l2.sort()
        for i in xrange(len(l1)):
            if l1[i] != l2[i]: return False
        return True                     # If nothing is unequal, return True.


# Problem 2: The Jetpack class (Based off of the Knapsack class, included below)
class Jetpack(Backpack):
    """Jetpack object. Inherits from the Backpack class. In addition to storing
    items like a backpack, a jetpack has fuel that is used to fly.
    
    Attributes:
        color (str): the color of the jetpack.
        name (str): the name of the jetpack.
        max_size (int): the maximum number of items that can fit in the
            jetpack.
        contents (list): the contents of the jetpack.
        fuel (int): the amount of fuel in the jetpack's tank.
    """

    def __init__(self,color='silver',name='jetpack',max_size=2,fuel=10):
        """Constructor for a jetpack object. A jetpack only holds 2 items by
        default instead of 5, and has an additional attribute for fuel.
        
        Inputs:
            color (str, opt): the color of the knapsack. Defaults to 'brown'.
            name (str, opt): the name of the knapsack. Defaults to 'knapsack'.
            max_size (int, opt): the maximum number of items that can be stored
                in the jetpack. Defaults to 2.
            fuel (int, opt): the starting amount of fuel. Defaults to 10.
        
        Returns:
            A jetpck object with no contents and 10 units of fuel.
        """
        
        Backpack.__init__(self, color, name, max_size)
        self.fuel = fuel
        # Or self.fuel = 10, without fuel as an argument for __init__().
    
    def fly(self,amount):
        """Fly by using 'amount' units of fuel."""
        if self.fuel - amount < 0:                  # Check current fuel
            print "Not enough fuel!"
        else:
            self.fuel -= amount
    
    def dump(self):
        """Empty the contents of the jetpack and dump out all the fuel."""
        Backpack.dump(self)
        # Or self.contents = []
        self.fuel = 0                               # Reset fuel to 0
    
    def __repr__(self):
        out = Backpack.__repr__(self)
        out += "\nFuel:\t\t" + str(self.fuel)
        return out

# An example class for Inheritance. Students do not need to modify this class;
#   it is given to them in 'Knapsack.py' but is not used in their solutions.
class Knapsack(Backpack):
    """Knapsack object. Inherits from the Backpack class.
    A knapsack is smaller than a backpack and can be tied closed.
    """
    def __init__(self, color='brown', name='knapsack', max_size=3):
        """Constructor for a knapsack object. A knapsack only holds 3 item by
        default instead of 5. Use the Backpack constructor to initialize the
        name and max_size attributes.
        
        Inputs:
            color (str, opt): the color of the knapsack. Defaults to 'brown'.
            name (str, opt): the name of the knapsack. Defaults to 'knapsack'.
            max_size (int, opt): the maximum number of items that can be stored
                in the knapsack. Defaults to 3.
        
        Returns:
            A knapsack object with no contents.
        """
        
        Backpack.__init__(self, color, name, max_size)
        self.closed = True
    
    def put(self, item):
        """If the knapsack is untied, use the Backpack put() method."""
        if self.closed:
            print "Knapsack is closed!"
        else:
            Backpack.put(self, item)
    
    def take(self, item):
        """If the knapsack is untied, use the Backpack take() method."""
        if self.closed:
            print "Knapsack is closed!"
        else:
            Backpack.take(self, item)
    
    def untie(self):
        """Untie the knapsack."""
        self.closed = False
    
    def tie(self):
        """Tie the knapsack."""
        self.closed = True

# Problem 3: See the 'Backpack' class above.

# Problem 4: The Complex Number class
class ComplexNumber(object):
    """Complex number object. Has a real and imaginary part.
    
    Attributes:
        real (float): the real part of the complex number.
        imag (float): the imaginary part of the complex number.
    """
    def __init__(self, a, b):
        """Initialize (separately) the real and imaginary components.
        Inputs:
            a (float): the real part.
            b (float): the imaginary part."""
        self.real = a
        self.imag = b
    
    def conjugate(self):
        """Return a ComplexNumber object of the complex conjugate."""
        return ComplexNumber(self.real, -1*self.imag)
    
    def norm(self):
        """Return the magnitude of the complex number."""
        return self.real**2 + self.imag**2

    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return ComplexNumber(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        r = (self.real * other.real) - (self.imag * other.imag)
        i = (self.real * other.imag) + (self.imag * other.real)
        return ComplexNumber(r, i)
        # Or,
        # return ComplexNumber(self.real*other.real - self.imag*other.imag,
        #    self.real*other.imag + self.imag*other.real)
    
    def __div__(self,other):
        """(a + bj)/(c + dj)
            = (a + bj)(c - dj)/(c + dj)(c - dj)         # Multiply by conjugate
            = ((ac + bd) + (bc - ad)j)/(c**2 + d**2)    # Distribute
            = ((ac + bd)/other.norm()) + ((bc - ad)j/other.norm())
        """
        r = ((self.real * other.real) + (self.imag * other.imag))/other.norm()
        i = ((self.imag * other.real) - (self.real * other.imag))/other.norm()
        return ComplexNumber(r,i)
        # Or
        # conj = other.conjugate()
        # numer = self*conj
        # denom = float((other*conj).real)
        # return ComplexNumber(numer.real/denom, numer.imag/denom)


# ----------------------------- END OF SOLUTIONS ----------------------------- #

# Test Script
def test(student_module):
    """Test script. You must import the students file as a module.
    10 points for problem 1
    15 points for problem 2
    20 points for problem 3
    20 points for problem 4
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of 100.
        feedback (str): a printout of the test results for the student.
    """

    s = student_module
    score = 0
    feedback = ""
    try:
        # Problem 1: 10 points
        feedback += "Testing problem 1 (10 points)..."
        points = 7
        # Test default name and max_size attributes
        b1 = Backpack()
        b2 = s.Backpack()
        if b1.name != b2.name:
            points -= 1; feedback += "\n\tincorrect name"
        if b1.max_size != b2.max_size:
            points -= 1; feedback += "\n\tincorrect max_size"
        # Test non-default color, name, and max_size attributes
        b1 =   Backpack(color='asvnawie',name='efnaiwen', max_size=3)
        b2 = s.Backpack(color='asvnawie',name='efnaiwen', max_size=3)
        if b1.color != b2.color:
            points -= 1; feedback += "\n\tincorrect color"
        if b1.name != b2.name:
            points -= 1; feedback += "\n\tincorrect name"
        if b1.max_size != b2.max_size:
            points -= 1; feedback += "\n\tincorrect max_size"
        # Test put() (no going over the limit)
        b1.put('f'); b1.put('u'); b1.put('n')
        b2.put('f'); b2.put('u'); b2.put('n')
        print("\nExpected output:\t"),
        b1.put('something else that should not fit')
        print("Student output: \t"),
        b2.put('something else that should not fit')
        part = int(input("\nScore out of 1: "))
        if not part: feedback += "\n\tput() failed to print 'Backpack Full!'"
        points += part
        if b1.contents != b2.contents:
            points -= 1; feedback += "\n\tincorrect contents -- put() failed"
        # Test dump()
        b1.dump()
        b2.dump()
        if b1.contents != b2.contents:
            points -= 1; feedback += "\n\tincorrect contents -- dump() failed"
        # Test docstrings
        print("\nStudent docstrings:\n")
        print(b2.__doc__)
        print(b2.__init__.__doc__)
        part = int(input("\nScore out of 2: "))
        if part < 2: feedback += "\n\tbad 'Backpack' docstring(s)"
        points += part
    
        feedback += "\n  Score += " + str(points)
        score += points
    
        # Problem 2: 15 points
        feedback += "\nTesting problem 2 (15 points)..."
        points = 11
        # Test default name, and max_size attributes
        b1 = Jetpack()
        b2 = s.Jetpack()
        if b1.name != b2.name:
            points -= 1
            feedback += "\n\tincorrect name (inheritance problem?)"
        if b1.max_size != b2.max_size:
            points -= 1
            feedback += "\n\tincorrect max_size (inheritance problem?)"
        # Test non-default color, name, and max_size attributes
        b1 =   Jetpack(color='asvnawie',name='efnaiwen', max_size=3)
        b2 = s.Jetpack(color='asvnawie',name='efnaiwen', max_size=3)
        if b1.color != b2.color:
            points -= 1
            feedback += "\n\tincorrect color (inheritance problem?)"
        if b1.name != b2.name:
            points -= 1
            feedback += "\n\tincorrect name (inheritance problem?)"
        if b1.max_size != b2.max_size:
            points -= 1
            feedback += "\n\tincorrect max_size (inheritance problem?)"
         # Test fuel attribute
        if b1.fuel != b2.fuel:
            points -= 1
            feedback += "\n\tincorrect fuel -- wrong default amount"
        # Test put() (no going over the limit)
        b1.put('f'); b1.put('u'); b1.put('n')
        b2.put('f'); b2.put('u'); b2.put('n')
        print("\nExpected output:\t"),
        b1.put('something else that should not fit')
        print("Student output: \t"),
        b2.put('something else that should not fit')
        part = int(input("\nScore out of 1: "))
        if not part:
            feedback += "\n\tput() failed to print 'Backpack Full!'. "
            feedback += "(inheritance problem?)"
        points += part
        if b1.contents != b2.contents: points -= 1
        # Test dump()
        b1.dump()
        b2.dump()
        if b1.contents != b2.contents:
            points -= 1; feedback += "\n\tincorrect contents -- dump() failed"
        if b1.fuel != b2.fuel:
            points -= 1; feedback += "\n\tincorrect fuel -- dump() failed"
        # Test fly()
        b1.fuel = 10
        b2.fuel = 10
        print("\nExpected output:\t"),
        b1.fly(20)
        print("Student output: \t"),
        b2.fly(20)
        part = int(input("\nScore out of 1: "))
        if not part: feedback += "\n\tfly() failed to print 'Not enough fuel!'"
        points += part
        if b1.fuel != b2.fuel:
            points -= 1; feedback += "\n\tincorrect fuel -- fly() failed"
        b1.fly(5)
        b2.fly(5)
        if b1.fuel != b2.fuel:
            points -= 1; feedback += "\n\tincorrect fuel -- fly() failed"
        # Test docstrings
        print("\nStudent docstrings:\n")
        print(b2.__doc__)
        print(b2.__init__.__doc__)
        part = int(input("\nScore out of 2: "))
        if part < 2: feedback += "\n\tbad 'Jetpack' docstring(s)"
        points += part
        
        feedback += "\n  Score += " + str(points)
        score += points
        
        # Problem 3: 20 points
        points = 10
        feedback += "\nTesting problem 3 (20 points)..."
        # Test __repr__ on an empty, default backpack
        b1 =   Backpack()
        b2 = s.Backpack()
        print("\nExpected output:")
        print(b1)
        print("\nStudent output:")
        print(b2)
        part = int(input("\nScore out of 5: "))
        if part < 5: feedback += "\n\tincorrect __repr__ for 'Backpack' object"
        points += part
        # Test __repr__ on a partially full backpack
        b1 =   Backpack('Blue and White','ACME',7)
        b2 = s.Backpack('Blue and White','ACME',7)
        b1.put('thing1'); b1.put('thing2'); b1.put('thing3')
        b2.put('thing1'); b2.put('thing2'); b2.put('thing3')
        print("\nExpected output:")
        print(b1)
        print("\nStudent output:")
        print(b2)
        part = int(input("\nScore out of 5: "))
        if part < 5: feedback += "\n\tincorrect __repr__ for 'Backpack' object"
        points += part
        # Test __eq__ in False case
        b1 =   Backpack('Color','Name',5)
        b2 = s.Backpack('Color','Name',5)
        b1.name = 'FalseName'
        if b1 == b2:
            points -= 1; feedback += "incorrect __eq__ for different names"
        b1.name = 'Name'; b1.color = 'Red'
        if b1 == b2:
            points -= 1; feedback += "incorrect __eq__ for different colors"
        b1.color = 'Color'
        b1.put('an item')
        b2.put("a different item")
        if b1 == b2:
            points -= 1;
            feedback += "incorrect __eq__ for different contents"
            feedback += "(same size contents list)"
        b1.put("yet another item")
        if b1 == b2:
            points -= 2
            feedback += "incorrect __eq__ for different contents"
            feedback += "(different sized contents list)"
        # Test __eq__ in True case
        b1 =   Backpack('green','Math',3)
        b2 = s.Backpack('green','Math',3)
        if not (b1 == b2):
            points -= 1; feedback += "incorrect __eq__ for same names"
        b1.put('an item')
        b2.put('an item')
        if not (b1 == b2):
            points -= 2; feedback += "incorrect __eq__ for same contents"
        b1.put('A')
        b2.put('B')
        b1.put('B')
        b2.put('A')
        if not (b1 == b2):
            points -= 2
            feedback += "incorrect __eq__ for same contents"
            feedback += "(same contents in different order)"

        feedback += "\n  Score += " + str(points)
        score += points
    
        # Problem 4: 20 points
        feedback += "\nTesting problem 4 (20 points)..."
        points = 18
        x1 =   ComplexNumber(3392,-493)
        y1 = s.ComplexNumber(3392,-493)
        # Test real / imag attributes
        if x1.real != y1.real:
            points -= 1; feedback += "\n\tincorrect real"
        if x1.imag != y1.imag:
            points -= 1; feedback += "\n\tincorrect imag"
        # Test conjugate()
        x2 = x1.conjugate()
        y2 = y1.conjugate()
        if x2.real != y2.real:
            points -= 1
            feedback += "\n\tincorrect real -- conjugate() failed"
        if x2.imag != y2.imag:
            points -= 1
            feedback += "\n\tincorrect imag -- conjugate() failed"
        # Test norm()
        if x1.norm() != y1.norm():
            points -= 2
            feedback += "\n\tnorm() failed"
        # Test __add__
        x2 = ComplexNumber(-21,210)
        y2 = ComplexNumber(-21,210)
        x3 = x1 + x2
        y3 = y1 + y2
        if x3.real != y3.real:
            points -= 1
            feedback += "\n\tincorrect real -- __add__ failed"
        if x3.imag != y3.imag:
            points -= 1
            feedback += "\n\tincorrect imag -- __add__ failed"
        # Test __sub__
        x3 = x1 - x2
        y3 = y1 - y2
        if x3.real != y3.real:
            points -= 1
            feedback += "\n\tincorrect real -- __sub__ failed"
        if x3.imag != y3.imag:
            points -= 1
            feedback += "\n\tincorrect imag -- __sub__failed"
        # Test __mul__
        x3 = x1 * x2
        y3 = y1 * y2
        if x3.real != y3.real:
            points -= 2
            feedback += "\n\tincorrect real -- __mul__ failed"
        if x3.imag != y3.imag:
            points -= 2
            feedback += "\n\tincorect imag -- __mul__ failed"
        # Test __div__
        x3 = x1 / x2
        y3 = y1 / y2
        if x3.real != y3.real:
            points -= 2
            feedback += "\n\tincorrect real -- __div__ failed"
        if x3.imag != y3.imag:
            points -= 2
            feedback += "\n\tincorrect imag -- __div__ failed"
        # Test docstrings
        print("\nStudent docstrings:\n")
        print(y1.__doc__)
        print(y1.__init__.__doc__)
        part = int(input("\nScore out of 2: "))
        if part < 2: feedback += "\n\tbad 'ComplexNumber' docstring(s)"
        points += part
        
        feedback += "\n  Score += " + str(points)
        score += points
        
    except:
        feedback += "\n\nCompilation Error!"
    
    # Report final score    
    feedback += "\n\nTotal score: "+str(score)+"/65 = "+str(score/.65)+"%"
    return score/.65, feedback
