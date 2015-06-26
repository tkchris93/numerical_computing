# lab3_solutions.py
""" Volume II Lab 3: Public Key Encryption (RSA)
    Main solutions file. Also see 'rsa_tools'.
    Use the test() method as a test script.
    Written by Shane McQuarrie, Spring 2015.
"""

import rsa_tools as rtl
from numpy.random import randint
from Crypto.PublicKey import RSA

# Students should use their implementation of the Extended Euclidean Algorithm
#   to solve Problem 1. We will use this implementation in our RSA system.
def eea(a, b):
    """The Extended Euclidean Algorithm.
    
    Inputs:
        a (int)
        b (int)
    
    Returns:
        gcd (int), c (int), d (int) such that gcd = ac + bd.
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = eea(b % a, a)
        return (g, x - (b // a) * y, y)

# Problem 1: Implement this class.
class myRSA(object):
    """RSA String Encryption System. Do not use any external modules except for
    'rsa_tools' and your implementation of the Extended Euclidean Algorithm.
    
    Attributes:
        public_key (tup): the RSA key that is available to everyone. Of the
            form (e, n). Used only in encryption.
        _private_key (tup, hidden): the secret RSA key. Of the form (d, n).
            Used only in decryption.
    
    Examples:
        >>> r = myRSA()
        >>> r.generate_keys(1000003,608609,1234567891)
        >>> print(r.public_key)
        (1234567891, 608610825827)
        
        >>> r.decrypt(r.encrypt("SECRET MESSAGE"))
        'SECRET MESSAGE'
        
        >>> s = myRSA()
        >>> s.generate_keys(287117,104729,610639)
        >>> s.decrypt(r.encrypt("SECRET MESSAGE",s.public_key))
        'SECRET MESSAGE
    """
    def __init__(self):
        """Initialize public and private key variables."""
        self.public_key = None
        self._private_key = None
        # Or self.generate_keys() here, if you provide default values.
    
    def generate_keys(self,p=1000003,q=608609,e=1234567891):
        """Create a pair of RSA keys.
        
        Inputs:
            p (int): A large prime.
            q (int): A second large prime .
            e (int): The encryption exponent. 
        
        Returns:
            Set the public_key and _private_key attributes.
        """
        n = p*q
        phi_n = (p-1)*(q-1)
        d = eea(e,phi_n)                        # Use the Extended Euc. Alg.
        if d[0] != 1:
            raise ValueError("e and phi(n) not relatively prime")
        d = d[1]
        d %= phi_n
        
        self.public_key = (e,n)
        self._private_key = (d,n)
    
    def encrypt(self, message, key=None):
        """Encrypt 'message' with a public key and return its encryption as a
        list of integers. If no key is provided, use the 'public_key' attribute
        to encrypt the message.
        
        Inputs:
            message (str): the message to be encrypted.
            key (int tup, opt): the public key to be used in the encryption.
                 Defaults to 'None', in which case 'public_key' is used.
        """
        if not key: key = self.public_key
        part = rtl.partition(message, rtl.string_size(key[1]), '~')
        numbers = []                            # Partition the message
        for i in part:                          # Convert each piece to numbers
            numbers.append(rtl.string_to_int(i))
        ciphertext = []
        for i in numbers:                       # Encrypt the numbers
            ciphertext.append(pow(i,key[0],key[1]))
        return ciphertext
    
    def decrypt(self, message):
        """Decrypt 'message' with the private key and return its decryption as
        a single string. You may assume that the format of 'message' is the
        same as the output of the encrypt() function.
        """
        key = self._private_key
        decryptions = []
        for i in message:                       # Decrypt each number
            decryptions.append(pow(i,key[0],key[1]))
        text = []
        for i in decryptions:                   # Convert back to string
            text.append(rtl.int_to_string(i))
        text = "".join(text)                    # Splice the strings together
        while text.endswith('~'):               # Strip off the fill value.
            text = text[:len(text)-1]
        return text


# Problem 2: Fermat's test for primality.
def is_prime(n):
    """Use Fermat's test for primality to see if 'n' is probably prime.
    Run the test at most 5 times, using integers randomly chosen from [2, n-1]
    as possible witnesses. If a witness number is found, return the number of
    tries it took to find the witness. If no witness number is found after 5
    tries, return 0.
    
    Inputs:
        n (int): the candidate for primality.
    
    Returns:
        The number of tries it took to find a witness number, up to 5 (or 0 if
        no witnesses were found).
    
    """
    for i in range(5):          # Try at most 5 times
        a = randint(2,n)            # pick a random witness
        if 1 != pow(a,n-1,n):       # If a witness is found,
            return i+1                  # return the number of tries
    return 0                    # return 0 if no witness is found.


# Problem 3: Implement an RSA class using PyCrypto.
class PyCrypto(object):
    """RSA String Encryption System. Do not use any external modules except for
    those found in the 'Crypto' package.
    
    Attributes:
        _keypair (RSA obj, hidden): the RSA key (both public and private).
            Facilitates encrypt() and decrypt().
        public_key (str): A sharable string representation of the public key.
    
    Examples:
        
        >>> p = PyCrypto()
        >>> p.decrypt(p.encrypt("SECRET MESSAGE"))
        'SECRET MESSAGE'
        
        >>> print(p.public_key)
        -----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQ...
        ...
        ...HwIDAQAB
        -----END PUBLIC KEY-----
        
        >>> q = PyCrypto()
        >>> q.decrypt(p.encrypt("SECRET MESSAGE",q.public_key))
        'SECRET MESSAGE'
    
    """
    def __init__(self):
        """Initialize the _keypair and public_key attributes."""
        self._keypair = RSA.generate(2048)
        self.public_key = self._keypair.publickey().exportKey()
    
    def encrypt(self, message, key=None):
        """Encrypt 'message' with a public key and return its encryption. If
        no key is provided, use the '_keypair' attribute to encrypt 'message'.
        
        Inputs:
            message (str): the message to be encrypted.
            key (str, opt): the string representation of the public key to be
                used in the encryption. Defaults to 'None', in which case
                '_keypair' is used to encrypt the message.
        """
        if not key:
            return self._keypair.encrypt(message, 2048)
        else:
            return RSA.importKey(key).encrypt(message, 2048)
    
    def decrypt(self, message):
        """Decrypt 'message' and return the decryption."""
        return self._keypair.decrypt(message)

# ----------------------------- END OF SOLUTIONS ----------------------------- #

# prime number generator for sample key generation
def prime(n):
    """Calculates the nth prime number."""
    primes = [2,3,5,7] # start with some primes
    if n < len(primes): print primes[n-1]; return
    i = 11 # initialize the prime candidate
    while len(primes) < n:
        unique = True
        j = 1 # check divisibility by prior primes
        while unique and j < len(primes):
            if i % primes[j] == 0: unique = False
            j += 1
        if unique: primes.append(i)
        i += 2 # increment the candidate by 2 (avoid evens)
    print primes[len(primes) - 1]
    return primes

# TEST THIS SCRIPT WITH TANNER AND BEN'S SOLUTIONS TO MAKE SURE IT WORKS !!!
#   NOT SURE IF THE KEYS WILL ALWAYS BE GENERATED THE SAME (DIFFERENT EEA)...
def test(student_module):
    """Test script. You must import the student's file as a module.
    30 points for problem 1
    10 points for problem 2
    10 points for problem 3
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of 100.
        feedback (str): a printout of test results for the student.
    """
    
    s = student_module
    score = 0
    feedback = ""
    
    try:
        # Problem 1: 30 points
        feedback += "\nTesting problem 1 (30 points)..."
        points = 20
        r1 =   myRSA()
        r2 = s.myRSA()
        # Round 1: test e, d, n (5 pts)
        r1.generate_keys(610639,287117,104729)
        r2.generate_keys(610639,287117,104729)
        if r1.public_key[0] != r2.public_key[0]:
            points -= 1; feedback += "\n\tincorrect public key"
        if r1._private_key[0] != r2._private_key[0]:
            points -= 2; feedback += "\n\tincorrect private key"
        if r2.public_key[1] != r2._private_key[1]:
            points -= 2; feedback += "\n\tincorrect encryption exponent"
        # Round 2: test e, d, n (5 pts)
        r1.generate_keys(562739,588949,7927)
        r2.generate_keys(562739,588949,7927)
        if r1.public_key[0] != r2.public_key[0]:
            points -= 1; feedback += "\n\tincorrect public key"
        if r1._private_key[0] != r2._private_key[0]:
            points -= 2; feedback += "\n\tincorrect private key"
        if r2.public_key[1] != r2._private_key[1]:
            points -= 2; feedback += "\n\tincorrect encryption exponent"
        # test encrypt() (5 pts)
        r2.generate_keys(20731,4021,4987)
        r1.public_key,r1._private_key = r2.public_key,r2._private_key
        if r1.encrypt("Test1") != r2.encrypt("Test1"):
            points -= 1; feedback += "\n\tincorrect encryption"
        if r1.encrypt("_____") != r2.encrypt("_____"):
            points -= 2; feedback += "\n\tincorrect encryption"
        if r1.encrypt("__A__") != r2.encrypt("__A__"):
            points -= 2; feedback += "\n\tincorrect encryption"
        # test decrypt() (5 pts)
        r1.generate_keys(22697,20743,30931)
        r2.public_key,r2._private_key = r1.public_key,r1._private_key
        if r2.decrypt(r1.encrypt("test1")) != "test1":
            points -= 1; feedback += "\n\tincorrect decryption"
        if r2.decrypt(r1.encrypt("2test2")) != "2test2":
            points -= 2; feedback += "\n\tincorrect decryption"
        if r2.decrypt(r1.encrypt("tEst3")) != "tEst3":
            points -= 2; feedback += "\n\tincorrect decryption"
        # test encrypt() and decrypt() together (10 pts)
        def crypt(o,message):
            """Test encrypt() and decrypt(). Return 1 on success, 0 else."""
            mes = o.decrypt(o.encrypt(message))
            if message == mes: return 1
            else: return 0
        r2.generate_keys(610639,287117,104729)
        p = 0
        p += crypt(r2,"small")
        p += crypt(r2,"really really really really really long test")
        p += crypt(r2,"!@#$%^&*^$%##%^%&*&^&$%^#%#$@#%$& weird test")
        p += crypt(r2,"Jared is the bomb.")
        p += crypt(r2,"F$I$N$A$L$_ ### _$T$E$S$T")
        if p < 5:
            feedback += "\n\tmyRSA Decrypt(encryption) failed"
        points += p
        # Key exchange
        r1.generate_keys(17393,12899,3853)
        r2.public_key,r2._private_key = r1.public_key,r1._private_key
        p = 0
        p += crypt(r2,"small")
        p += crypt(r2,"really really really really really long test")
        p += crypt(r2,"!@#$%^&*^$%##%^%&*&^&$%^#%#$@#%$& weird test")
        p += crypt(r2,"Jared is the bomb.")
        p += crypt(r2,"F$I$N$A$L$_ ### _$T$E$S$T")
        if p < 5:
            feedback += "\n\tmyRSA Decrypt(Encrypt(Message)) failed"
        points += p
        
        score += points
        feedback += "\n  Score += " + str(points)
        
        # Problem 2: 10 points
        feedback += "\nTesting problem 2 (10 points)..."
        points = 10
        prime = "\n\tprime marked as nonprime -- is_prime() failed"
        nonprime = "\n\tnonprime marked as prime -- is_prime() failed"
        def primality(n):
            """Call the student's is_prime() function 10 times on 'n'."""
            total = 0
            for i in xrange(10):
                total += s.is_prime(n)
                if total > 0: break
            return total
        # Correct response with primes
        if primality(547):
            points -= 1; feedback += prime
        if primality(4421):
            points -= 1; feedback += prime
        if primality(9739):
            points -= 1; feedback += prime
        if primality(16411):
            points -= 1; feedback += prime
        if primality(43063):
            points -= 1; feedback += prime
        # Correct response with composites
        if not primality(10):
            points -= 1; feedback += nonprime
        if not primality(1000):
            points -= 1; feedback += nonprime
        if not primality(542):
            points -= 1; feedback += nonprime
        if not primality(1643):
            points -= 1; feedback += nonprime
        if not primality(340561):
            points -= 1; feedback += nonprime
        
        score += points
        feedback += "\n  Score += " + str(points)
        
        # Problem 3: 10 points
        feedback += "\nTesting problem 3 (10 points)..."
        p = 0
        r2 = s.PyCrypto()
        # Test encrypt and decrypt together
        p += crypt(r2,"small")
        p += crypt(r2,"really really really really really long test")
        r2 = s.PyCrypto()
        p += crypt(r2,"!@#$%^&*^$%##%^%&*&^&$%^#%#$@#%$& weird test")
        p += crypt(r2,"Jared is the bomb.")
        r2 = s.PyCrypto()
        p += crypt(r2,"F$I$N$A$L$_ ### _$T$E$S$T")
        if p < 5:
            feedback += "\n\tPyCrypto Decrypt(Encrypt(Message))) failed"
        points = p
        p = 0
        # Test send()
        def sender(p,q,message):
            """Test send(). Return 1 on success, 0 else."""
            mes = q.decrypt(p.encrypt(message,q.public_key))
            if message == mes: return 1
            else: return 0
        r1 =   PyCrypto()
        r2 = s.PyCrypto()
        p += sender(r2,r1,"small")
        p += sender(r2,r1,"really really really really really long test")
        r1 =   PyCrypto()
        r2 = s.PyCrypto()
        p += sender(r2,r1,"!@#$%^&*^$%##%^%&*&^&$%^#%#$@#%$& weird test")
        p += sender(r1,r2,"Jared is the bomb.")
        r1 =   PyCrypto()
        r2 = s.PyCrypto()
        p += sender(r1,r2,"F$I$N$A$L$_ ### _$T$E$S$T")
        if p < 5:
            feedback += "\n\tPyCrypto Decrypt(send(Message,Public Key)) failed"
        points += p
        
        score += points
        feedback += "\n  Score += " + str(points)
    
    except:
        feedback += "\n\nCompilation Error!!"
    
    # Report final score    
    feedback += "\n\nTotal score: "+str(score)+"/50 = "+str(score/.5)+"%"
    return score/.5,feedback