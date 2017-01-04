# test_driver.py
"""Introductory Labs: Intro to Python. Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _timeout

from numpy.random import randint
from solutions import *


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 2
    10 points for problem 3
     5 points for problem 4
     5 points for problem 5
    10 points for problem 6
     5 points for problem 7

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.problems = [   (self.problem2, "Problem 2",  5),
                            (self.problem3, "Problem 3", 10),
                            (self.problem4, "Problem 4",  5),
                            (self.problem5, "Problem 5",  5),
                            (self.problem6, "Problem 6", 10),
                            (self.problem7, "Problem 7",  5)    ]

    # Problems ----------------------------------------------------------------
    @_timeout(5)
    def problem2(self, s):
        """Test sphere_volume(). 5 Points."""
        if s.sphere_volume(1) is None:
            raise NotImplementedError("sphere_volume() returned nothing")

        points  = 2*self._eqTest(sphere_volume(5), s.sphere_volume(5),
                                            "sphere_volume(5) failed")
        points += 3*self._eqTest(sphere_volume(3.14), s.sphere_volume(3.14),
                                            "sphere_volume(3.14) failed")
        return points

    @_timeout(5)
    def problem3(self, s):
        """Test first_half() and backward(). 10 points."""
        if s.first_half("abcde") is None:
            raise NotImplementedError("first_half() returned nothing")
        if s.backward("abcde") is None:
            raise NotImplementedError("backward() returned nothing")

        points  = 2*self._eqTest(first_half("abcde"), s.first_half("abcde"),
                                            "first_half('abcde') failed")
        points += 3*self._eqTest(first_half("TK421"), s.first_half("TK421"),
                                            "first_half('TK421') failed")
        points += 2*self._eqTest(backward("abcde"), s.backward("abcde"),
                                            "backward('abcde') failed")
        points += 3*self._eqTest(backward("TK421"), s.backward("TK421"),
                                            "backward('TK421') failed")
        return points

    @_timeout(5)
    def problem4(self, s):
        """Test list_ops(). 5 points."""
        if s.list_ops() is None:
            raise NotImplementedError("list_ops() returned nothing")

        return 5*self._eqTest(list_ops(), s.list_ops(), "list_ops() failed")

    @_timeout(5)
    def problem5(self, s):
        """Test pig_latin(). 5 points."""
        if s.pig_latin("piglatin") is None:
            raise NotImplementedError("pig_latin() returned nothing")

        points = 2*self._eqTest(  pig_latin("college"),
                                s.pig_latin("college"),
                                            "pig_latin('college') failed")
        points += 3*self._eqTest(  pig_latin("university"),
                                 s.pig_latin("university"),
                                        "pig_latin('university') failed")
        return points

    @_timeout(10)
    def problem6(self, s):
        """Test palindrome(). 5 points."""
        if s.palindrome() is None:
            raise NotImplementedError("palindrome() returned nothing")

        correct, student = palindrome(), s.palindrome()
        if correct > student:
            self.feedback += "\npalindrome() failed: {} is too low".format(
                                                                    student)
        elif correct < student:
            self.feedback += "\npalindrome() failed: {} is too high".format(
                                                                    student)
        return 10 if correct == student else 0

    @_timeout(5)
    def problem7(self, s):
        """Test alt_harmonic(). 10 points."""
        if s.alt_harmonic(10) is None:
            raise NotImplementedError("alt_harmonic() returned nothing")

        points = 2*self._eqTest(alt_harmonic(100), s.alt_harmonic(100),
                                            "alt_harmonic(100) failed")
        points += 3*self._eqTest(alt_harmonic(5000), s.alt_harmonic(5000),
                                            "alt_harmonic(5000) failed")
        return points

# Main Routine ================================================================

def test(student_module, total=40):
    """Grade a student's entire solutions file.

     5 points for problem 2
    10 points for problem 3
     5 points for problem 4
     5 points for problem 5
    10 points for problem 6
     5 points for problem 7

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
