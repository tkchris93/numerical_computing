# testDriver.py
"""Introductory Labs: Object Oriented Programming. Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout

from math import sqrt
from numpy.random import randint
from solutions import Backpack, Jetpack


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

    10 points for problem 1: Backpack constructor, put(), and dump()
    10 points for problem 2: Jetpack constructor, fly(), and dump().
    10 points for problem 3: Backpack __eq__() and __str__().
    10 points for problem 4: ComplexNumber class.

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.

    This particular test driver is designed to allow flexibility in the
    student's Backpack and Jetpack classes by never explicitly calling
    a particular attribute name. That is, instead of examining a Backpack's
    'max_size' attribute (which the student may or may not have called
    'max_size'), the Backpack's put() method is called to ensure that the
    contents list has not grown past the limit. The only exception is that
    'contents' is specifically referred to, because it is explicitly named
    that way in the example code.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.problems = [   (self.problem1, "Problem 1", 10),
                            (self.problem2, "Problem 2", 10),
                            (self.problem3, "Problem 3", 10),
                            (self.problem4, "Problem 4", 10)    ]

    # Helper Functions --------------------------------------------------------
    def _evalTest(self, expression, message):
        """Test a boolean 'expression' to see if it is True.
        Report the given 'message' if it is not.
        """
        if expression:
            return 1
        else:
            self.feedback += "\n{}".format(message)
            return 0

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test the Backpack class. 10 points."""

        # Test the constructor (2 points)
        b1 = Backpack("Teacher", "silver")
        b2 = s.Backpack("Student", "green")
        points = 2

        # Test put() (6 points).
        for item in range(5):
            b1.put(item); b2.put(item)
        points += self._eqTest(b1.contents, b2.contents,
                "Backpack.put() failed to update Backpack.contents correctly")
        print("\nCorrect output:\t"),; b1.put(5)
        print("Student output:\t"),; b2.put(5)
        points += self._grade(1, 'Backpack.put() failed to print "No Room!"')
        points += self._eqTest(b1.contents, b2.contents,
                "Backpack.put() failed to update Backpack.contents correctly")

        b1 = Backpack("Teacher", "silver", 1)
        b2 = s.Backpack("Student", "green", 1)
        b1.put(100); b2.put(100)
        print("\nCorrect output:\t"),; b1.put(200)
        print("Student output:\t"),; b2.put(200)
        points += self._grade(1, 'Backpack.put() failed to print "No Room!"')
        points += 2*self._eqTest(b1.contents, b2.contents,
            "Backpack.put() failed to update Backpack.contents correctly")

        # Test dump() (2 points)
        b1.dump(); b2.dump()
        points += 2*self._eqTest(b1.contents, b2.contents,
                            "Backpack.dump() failed to empty contents")
        return points

    def problem2(self, s):
        """Test the Jetpack class. 10 Points."""

        # Test the constructor (2 points)
        j1, j2 = Jetpack("Teacher", "silver"), s.Jetpack("Student", "green")
        points = 2

        # Test put() (2 points).
        for item in range(2):
            j1.put(item); j2.put(item)
        points += .5*self._eqTest(j1.contents, j2.contents,
                "Jetpack.put() failed to update Jetpack.contents correctly")
        print("\nCorrect output:\t"),; j1.put(5)
        print("Student output:\t"),; j2.put(5)
        points += self._grade(1, 'Jetpack.put() failed to print "No Room!"')
        points += .5*self._eqTest(j1.contents, j2.contents,
                "Backpack.put() failed to update Backpack.contents correctly")

        # Test fly() (4 points)
        print("\nCorrect output:\t"),; j1.fly(11)
        print("Student output:\t"),; j2.fly(11)
        points += self._grade(2, 'Jetpack.fly() failed to print '
                                                        '"Not enough fuel!"')
        j2 = Jetpack("Student", "green", 0, 50)
        j2.fly(10); j2.fly(10); j2.fly(10); j2.fly(10); j2.fly(9)
        print("\nCorrect output:\t"),; j1.fly(11)
        print("Student output:\t"),; j2.fly(11)
        points += self._grade(2, 'Jetpack.fly() failed to print '
                                                        '"Not enough fuel!"')

        # Test dump() (2 points)
        j1.dump(); j2.dump()
        print("\nCorrect output:\t"),; j1.fly(1)
        print("Student output:\t"),; j2.fly(1)
        points += self._grade(2, 'Jetpack.fly() failed to print '
                                                        '"Not enough fuel!"')

        # Check Inheritance (required to get any points).
        points *= self._evalTest(issubclass(s.Jetpack, s.Backpack),
                    "The Jetpack class must inherit from the Backpack class!")

        return int(points)

    def problem3(self, s):
        """Test the Backpack class's magic methods. 10 points."""

        # Test Backpack.__eq__() in False case (3 points).
        b1 = s.Backpack("Name1", "Color", 10)
        b2 = s.Backpack("Name2", "Color", 10)
        points = self._evalTest(not b1==b2,
                                "Backpack.__eq__() failed (different names)")

        b1 = s.Backpack("Name", "Color1", 10)
        b2 = s.Backpack("Name", "Color2", 10)
        points += self._evalTest(not b1==b2,
                                "Backpack.__eq__() failed (different colors)")

        b1 = s.Backpack("Name", "Color", 10)
        b2 = s.Backpack("Name", "Color", 10)
        for item in [1, 2, 3]:
            b1.put(item); b2.put(item)
        b2.put(4)
        points += self._evalTest(not b1==b2,
                    "Backpack.__eq__() failed (different number of contents)")


        # Test Backpack.__eq__() in True case (2 points).
        b1 = s.Backpack("Name", "Color", 100)
        b2 = s.Backpack("Name", "Color", 10)
        points += self._evalTest(b1==b2,
                                    "Backpack.__eq__() failed (equal objects)")

        for item in ["apple", "banana", "carrot"]:
            b1.put(item); b2.put(item)
        points += self._evalTest(b1==b2,
                                    "Backpack.__eq__() failed (equal objects)")

        # Test Backpack.__str__() on an empty Backpack (2 points).
        b1 =   Backpack("Student", "green", 4)
        b2 = s.Backpack("Student", "green", 4)
        if str(b1) != str(b2):
            print("\nCorrect output:"); print(b1)
            print("\nStudent output:"); print(b2)
            points += self._grade(2,
                            "Incorrect Backpack.__str__():\n{}\n".format(b2))
        else:
            points += 2

        # Test Backpack.__str__() on a Backpack with contents (3 points).
        b1 =   Backpack("Master Yoda", "tan", 7)
        b2 = s.Backpack("Master Yoda", "tan", 7)
        if str(b1) != str(b2):
            for item in ["Crystal", "Lightsaber", "Commlink", "Banana"]:
                b1.put(item); b2.put(item)
            print("\nCorrect output:"); print(b1)
            print("\nStudent output:"); print(b2)
            points += self._grade(3,
                            "Incorrect Backpack.__str__():\n{}\n".format(b2))
        else:
            points += 3

        return points

    @_timeout(5)
    def problem4(self, s):
        """Test the ComplexNumber class. 25 points."""

        # Check for cheating.
        if s.ComplexNumber is complex:
            print("CHECK FOR CHEATING (ComplexNumber is complex)")
            return 0

        points = 0

        # Test the constructor (0 points).
        a, b = randint(-50, 50, 2)
        cn = s.ComplexNumber(a, b)
        if not hasattr(cn, "real") or not hasattr(cn, "imag"):
            self.feedback += '\nComplexNumber class must have attributes '
            self.feedback += '"real" and "imag"'
            return 0
        self._eqTest(a, cn.real,"ComplexNumber.__init__() failed on real part")
        self._eqTest(b, cn.imag,"ComplexNumber.__init__() failed on imag part")

        # Test ComplexNumber.conjugate() (1 points).
        cn2 = cn.conjugate()
        if not isinstance(cn2, s.ComplexNumber):
            self.feedback += "ComplexNumber.conjugate() should return a "
            self.feedback += "new ComplexNumber object."
        else:
            points += .5*self._eqTest(a, cn2.real,
                        "ComplexNumber.conjugate() failed on real part")
            points += .5*self._eqTest(-1*b, cn2.imag,
                        "ComplexNumber.conjugate() failed on imag part")

        # Test ComplexNumber.__abs__() (1 point).
        a, b = randint(-50, 50, 2)
        cn = s.ComplexNumber(a, b)
        points += self._eqTest(sqrt(a**2 + b**2), abs(cn),
                                        "ComplexNumber.__abs__() failed")

        # Test ComplexNumber.__lt__() (1 point).
        cn1, cn2 = s.ComplexNumber(5, 7), s.ComplexNumber(1, 2)
        points += .5*self._evalTest(not cn1 < cn2,
                                "ComplexNumber.__lt__() failed")
        points += .5*self._evalTest(cn2 < cn1,
                                "ComplexNumber.__lt__() failed")

        # Test ComplexNumber.__gt__() (1 point).
        cn1, cn2 = s.ComplexNumber(1, 2), s.ComplexNumber(3, 4)
        points += .5*self._evalTest(not cn1 > cn2,
                                "ComplexNumber.__gt__() failed")
        points += .5*self._evalTest(cn2 > cn1,
                                "ComplexNumber.__gt__() failed")

        # Test ComplexNumber.__eq__() (1 point).
        cn1, cn2 = s.ComplexNumber(2, 3), s.ComplexNumber(3, 2)
        points += .5*self._evalTest(not cn1 == cn2,
                        "ComplexNumber.__eq__() failed on nonequal")
        cn1, cn2 = s.ComplexNumber(2, 3), s.ComplexNumber(2, 3)
        points += .5*self._evalTest(cn2 == cn1,
                        "ComplexNumber.__eq__() failed on equal")

        # Test ComplexNumber.__ne__() (1 point).
        cn1, cn2 = s.ComplexNumber(2, 3), s.ComplexNumber(3, 2)
        points += .5*self._evalTest(cn1 != cn2,
                        "ComplexNumber.__ne__() failed on nonequal")
        cn1, cn2 = s.ComplexNumber(2, 3), s.ComplexNumber(2, 3)
        points += .5*self._evalTest(not cn2 != cn1,
                        "ComplexNumber.__ne__() failed on equal")

        # Test ComplexNumber.__add__() (1 point).
        a, b, c, d = randint(-50, 50, 4)
        cn = s.ComplexNumber(a, b) + s.ComplexNumber(c, d)
        points += .5*self._eqTest(a+c, cn.real,
                    "ComplexNumber.__add__() failed on real part")
        points += .5*self._eqTest(b+d, cn.imag,
                    "ComplexNumber.__add__() failed on imag part")

        # Test ComplexNumber.__sub__() (1 point).
        a, b, c, d = randint(-50, 50, 4)
        cn = s.ComplexNumber(a, b) - s.ComplexNumber(c, d)
        points += .5*self._eqTest(a-c, cn.real,
                    "ComplexNumber.__sub__() failed on real part")
        points += .5*self._eqTest(b-d, cn.imag,
                    "ComplexNumber.__sub__() failed on real part")

        # Test ComplexNumber.__mul__() (1 points).
        a, b, c, d = randint(-50, 50, 4)
        cn1 = (a + 1j*b) * (c + 1j*d)
        cn2 = s.ComplexNumber(a, b) * s.ComplexNumber(c, d)
        points += .5*self._eqTest(round(cn1.real, 6), round(cn2.real, 6),
                                "ComplexNumber.__mul__() failed on real part")
        points += .5*self._eqTest(round(cn1.imag, 6), round(cn2.imag, 6),
                                "ComplexNumber.__mul__() failed on imag part")

        # Test ComplexNumber.__div__() (1 points).
        a, b, c, d = randint(-50, 50, 4)
        cn1 = (a + 1.0j*b) / (c + 1.0j*d)
        cn2 = s.ComplexNumber(a, b) / s.ComplexNumber(c, d)
        points += .5*self._eqTest(round(cn1.real, 6), round(cn2.real, 6),
                                "ComplexNumber.__div__() failed on real part")
        points += .5*self._eqTest(round(cn1.imag, 6), round(cn2.imag, 6),
                                "ComplexNumber.__div__() failed on imag part")

        return int(points)

# Main Routine ================================================================

def test(student_module, total=40):
    """Grade a student's entire solutions file.

    10 points for problem 1: Backpack constructor, put(), and dump()
    10 points for problem 2: Jetpack constructor, fly(), and dump().
    10 points for problem 3: Backpack __eq__() and __str__().
    10 points for problem 4: ComplexNumber class.

    Inputs:
        student_module: the imported module for the student's file.
        total (int): the total possible score.

    Returns:
        score (int): the student's score, out of 'total'.
        feedback (str): a printout of results for the student.
    """
    tester = TestDriver()
    tester.test_all(student_module, total)
    return tester.score, tester.feedback

# Validation ==================================================================

if __name__ == '__main__':
    import solutions
    test(solutions)
