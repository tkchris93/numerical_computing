"""Volume I Lab X: Unit test with python
<Name>
<Date>
"""
import math

#Problem 1 Write unit tests to test the addition. Be sure to install pytest-cov in order to see your code coverage change
def addition(a,b):
    return a+b

def smallest_factor(n):
    """Finds the smallest prime factor of a number.
    Assume n is a positive integer.
    """
    if n == 1:
        return 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return i
    return n


#Problem 2 Write unit tests to test the following
def operator(a,b,oper):
    if type(oper) != str:
        raise ValueError("Oper should be a string")
    if len(oper) != 1:
        raise ValueError("Oper should be one character")
    if oper == "+":
        return a+b
    if oper == "/":
        if b == 0:
            raise ValueError("You can't divide by zero!")
        return a/float(b)
    if oper == "-":
        return a-b
    if oper == "*":
        return a*b
    else:
        raise ValueError("Oper can only be: '+', '/', '-', or '*'")

#Problem 3 Write unit test for this class
class ComplexNumber(object):
    def __init__(self, real=0, imag=0):
        self.real = real
        self.imag = imag
    def conjugate(self):
        conjugate = ComplexNumber(real=self.real, imag=-self.imag)
        return conjugate
    def norm(self):
        magnitude = math.sqrt(self.real**2 + self.imag**2)
        return magnitude
    def __add__(self, other):
        real = self.real + other.real
        imag = self.imag + other.imag
        return ComplexNumber(real=real, imag=imag)
    def __sub__(self, other):
        real = self.real - other.real
        imag = self.imag - other.imag
        return ComplexNumber(real=real, imag=imag)
    def __mul__(self, other):
        real = self.real*other.real - self.imag*other.imag
        imag = self.imag*other.real + other.imag*self.real
        return ComplexNumber(real=real, imag=imag)
    def __div__(self, other):
        if other.real==0 and other.imag==0:
            raise ValueError("Cannot divide by zero")
        bottom = (other.conjugate()*other*1.).real
        top = self*other.conjugate()
        return ComplexNumber(real=(top.real/bottom), imag=(top.imag/bottom))
    def __eq__(self, other):
        return self.imag == other.imag and self.real == other.real
    def __str__(self):
        return str(self.real)+('+' if self.imag>=0 else '')+str(self.imag)+'i'



def read_in_cards(filename):
    cards = []
    with open(filename, 'r') as infile:
        cards = infile.read().strip().split('\n')
    if len(cards) != 12:
        raise ValueError("There must be 12 cards in each file")
    if len(set(cards)) != 12:
        raise ValueError("There may not be any duplicate cards")
    for card in cards:
        if len(str(card)) != 4:
            raise ValueError(str(card) + " is invalid: wrong number of characters")
        for a in str(card):
            if a not in ['0','1','2']:
                raise ValueError(str(card) + " can only contain the digits 0, 1 and 2")
    return cards

def is_set(a,b,c):
    for i in range(4):
        if (int(a[i]) + int(b[i]) + int(c[i])) % 3 != 0:
            return False
    return True

def count_matches(filename):
    cards = read_in_cards(filename)
    count = 0
    for i in xrange(len(cards)):
        for j in xrange(i+1,len(cards)):
            for k in xrange(j+1, len(cards)):
                if is_set(cards[i], cards[j], cards[k]):
                    count += 1
                    print cards[i], cards[j], cards[k]
    return count
