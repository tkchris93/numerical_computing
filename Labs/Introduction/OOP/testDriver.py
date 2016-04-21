from numpy.random import randint

# Test script
def test(student_module):
    """Test script. Import the student's solutions file as a module.
    
    10 points for problem 1. (?)
    10 points for problem 2. (?)
    10 points for problem 3. (?)
    10 points for problem 4. (?)
    10 points for problem 5. (?)
    
    Inputs:
        student_module: the imported module for the student's file.
    
    Returns:
        score (int): the student's score, out of 60.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback

# Test Driver
class _testDriver(object):
    """Class for testing a student's work. See test.__doc__ for more info.

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
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine ------------------------------------------------------------
    def test_all(self, student_module, total=60):
        """Grade the provided module on each problem and compile feedback."""
        self.feedback = ""
        self.score = 0

        def test_one(problem, number, total):
            try:
                self.feedback += "\n\nProblem %d (%d points):"%(number, total)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += %d"%points
            except BaseException as e:
                self.feedback += "\n%s: %s"%(self._errType(e),e)

        test_one(self.problem1, 1, 10)  # Problem 1: 10 points.
        test_one(self.problem2, 2, 10)  # Problem 2: 10 points.
        test_one(self.problem3, 3, 15)  # Problem 3: 15 points.
        test_one(self.problem4, 4, 25)  # Problem 4: 25 points.

        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: %d/%d = %s%%"%(
                                    self.score, total, percentage)
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += "\n\n\nComments:\n\t%s"%comments

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        if isinstance(error, BaseException):
            return str(type(error)).lstrip("<type 'exceptions.").rstrip("'>")
        else:
            return str(error)

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' == 'student'."""
        if correct == student:
            return 1
        else:
            self.feedback += "\n%s"%message
            self.feedback += "\n\tCorrect response: %s"%correct
            self.feedback += "\n\tStudent response: %s"%student
            return 0

    def _evalTest(self, expression, correct, message):
        """Test a boolean to see if it is correct."""
        if expression is correct:
            return 1
        else:
            self.feedback += "\n%s"%message
            return 0

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score."""
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of %d: "%points))
            except:
                credit = -1
        if credit != points:
            # Add comments (optionally),
            comments = raw_input("Comments: ")
            if len(comments) > 0:
                self.feedback += "\n%s"%comments
            # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n%s"%message
        return credit

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test the Backpack class. 10 points."""

        # Test the constructor.
        b1 = Backpack("Teacher", "silver")
        try:
            b2 = s.Backpack("Student", "green")
        except TypeError as e:
            raise NotImplementedError("Problem 1 Incomplete: %s"%e)
        points = 2

        # Test put() (no going over the limit).
        for item in ['this', 'is', 'a', 'test', '...']:
            b1.put(item); b2.put(item)
        points += self._eqTest(b1.contents, b2.contents,
            "Backpack.put() failed to update Backpack.contents correctly")
        print("\nTest that Backpack.put() doesn't go over the max_size.")
        print("Correct output:\t"),; b1.put('this should not fit')
        print("Student output:\t"),; b2.put('this should not fit')
        points += self._grade(1,
                        "'No Room!' failed to print (check Backpack.put())")
        points += self._eqTest(b1.contents, b2.contents,
            "Backpack.put() failed to update Backpack.contents correctly")
        b1.max_size = 1; b1.dump(); b2 = s.Backpack("Student", "green", 1)
        b1.put("Testing..."); b2.put("Testing...")
        print("\nTest that Backpack.put() doesn't go over the max_size.")
        print("Correct output:\t"),; b1.put('this should not fit')
        print("Student output:\t"),; b2.put('this should not fit')
        points += self._grade(1,
                        "'No Room!' failed to print (check Backpack.dump())")
        points += 2*self._eqTest(b1.contents, b2.contents,
            "Backpack.put() failed to update Backpack.contents correctly")

        # Test dump().
        b1.dump(); b2.dump()
        points += 2*self._eqTest(b1.contents, b2.contents,
                            "Backpack.dump() failed to empty contents")
        return points

    def problem2(self, s):
        """Test the Jetpack class. 10 Points."""
        if not hasattr(s, "Jetpack"):
            raise NotImplementedError("Problem 2 Incomplete")

        # Test the constructor.
        j1, j2 = Jetpack("Teacher", "silver"), s.Jetpack("Student", "green")
        points = 2

        # Test put() (no going over the limit).
        for item in ['Testing', 'testing']:
            j1.put(item); j2.put(item)
        points += self._eqTest(j1.contents, j2.contents,
                                            "Jetpack.put() failed.")
        print("\nTest that Jetpack.put() doesn't go over the max_size.")
        print("Correct output:\t"),; j1.put('this should not fit')
        print("Student output:\t"),; j2.put('this should not fit')
        points += self._grade(1,
                        "'No Room!' failed to print (check Jetpack.put()")
        points += self._eqTest(j1.contents, j2.contents,
            "Jetpack.put() failed to update Jetpack.contents correctly")
        j1.max_size = 1; j1.dump(); j2 = s.Jetpack("Student", "green", 1)
        j1.put("Testing..."); j2.put("Testing...")
        print("\nTest that Jetpack.put() doesn't go over the max_size.")
        print("Correct output:\t"),; j1.put('this should not fit')
        print("Student output:\t"),; j2.put('this should not fit')
        points += self._grade(1,
                        "'No Room!' failed to print (check Jetpack.put())")
        points += self._eqTest(j1.contents, j2.contents,
            "Jetpack.put() failed to update Jetpack.contents correctly")

        # Test fly().
        print("\nTest that fly(amount) doesn't work if amount > fuel.")
        print("Correct output:\t"),; j1.fly(11)
        print("Student output:\t"),; j2.fly(11)
        points += self._grade(1,
                "'Not Enough Fuel!' failed to print (check Jetpack.fly())")
        
        # Test dump().
        j1.dump(); j2.dump()
        print("\nTest that Jetpack.dump() sets the fuel to zero.")
        print("Correct output:\t"),; j1.fly(1)
        print("Student output:\t"),; j2.fly(1)
        points += 2*self._grade(1,
                "'Not Enough Fuel!' failed to print (check Jetpack.dump())")

        if not issubclass(s.Jetpack, s.Backpack):
            self.feedback += "The Jetpack class must inherit from the "
            self.feedback += "Backpack class!"
            points = 0

        return points

    def problem3(self, s):
        """Test the Backpack class's magic methods. 15 points."""
        
        # Test Backpack.__eq__() in False case (4 points).
        try:
            b1 = s.Backpack("Name1", "Color", 10)
        except TypeError as e:
            raise NotImplementedError("Problem 3 Incomplete: %s"%e)
        b2 = s.Backpack("Name2", "Color", 10)
        points = self._evalTest(b1==b2, False,
                    "Backpack.__eq__() failed on different names")
        
        b1 = s.Backpack("Name", "Color1", 10)
        b2 = s.Backpack("Name", "Color2", 10)
        points += self._evalTest(b1==b2, False,
                    "Backpack.__eq__() failed on different colors")

        b1 = s.Backpack("Name", "Color", 10)
        b2 = s.Backpack("Name", "Color", 10)
        for item in [1, 2, 3]:
            b1.put(item); b2.put(item)
        b2.put(4)
        points += self._evalTest(b1==b2, False,
                    "Backpack.__eq__() failed on different contents")
        b1.put(5)
        points += self._evalTest(b1==b2, False,
                    "Backpack.__eq__() failed on different contents")

        # Test Backpack.__eq__() in True case (3 points).
        b1 = s.Backpack("Name", "Color", 100)
        b2 = s.Backpack("Name", "Color", 10)
        points += self._evalTest(b1==b2, True,
                    "Backpack.__eq__() failed on equal objects.")
        
        for item in ["apple", "banana", "carrot"]:
            b1.put(item); b2.put(item)
        points += self._evalTest(b1==b2, True,
                    "Backpack.__eq__() failed on equal objects.")

        b1.put("mango"); b1.put("salsa"); b2.put("salsa"); b2.put("mango")
        points += self._evalTest(b1==b2, True,
                    "Backpack.__eq__() failed on equal objects.")
        if not b1==b2:
            self.feedback += "\n\t(Hint: Backpack1.contents: %s"%b1.contents
            self.feedback += "\n\t       Backpack2.contents: %s)"%b2.contents
        
        # Test Backpack.__str__() on an empty Backpack (4 points).
        b1 =   Backpack("Student", "green", 4)
        b2 = s.Backpack("Student", "green", 4)
        print("\nTest Backpack.__str__() on a Backpack with no contents.")
        print("\nCorrect output:"); print(b1)
        print("\nStudent output:"); print(b2)
        points += self._grade(4, "Incorrect Backpack.__str__():\n\n%s\n\n"%b2)
        
        # Test Backpack.__str__() on a Backpack with contents (4 points).
        b1 =   Backpack("Master Yoda", "tan", 7)
        b2 = s.Backpack("Master Yoda", "tan", 7)
        for item in ["Crystal", "Lightsaber", "Commlink", "Banana"]:
            b1.put(item); b2.put(item)
        print("\nTest Backpack.__str__() on a Backpack with some contents.")
        print("\nCorrect output:"); print(b1)
        print("\nStudent output:"); print(b2)
        points += self._grade(4, "Incorrect Backpack.__str__():\n\n%s\n\n"%b2)

        return points

    def problem4(self, s):
        """Test the ComplexNumber class. 25 points."""
        if not hasattr(s, "ComplexNumber"):
            raise NotImplementedError("Problem 4 Incomplete")

        # Test the constructor (2 points).
        a, b = randint(-50, 50, 2)
        cn = s.ComplexNumber(a, b)
        if not hasattr(cn, "real") or not hasattr(cn, "imag"):
            self.feedback += "ComplexNumber class must have attributes "
            self.feedback += "'real' and 'imag'!"
            return 0
        points  = self._eqTest(a, cn.real, "ComplexNumber.real failed")
        points += self._eqTest(b, cn.imag, "ComplexNumber.imag failed")

        # Check for cheating.
        if s.ComplexNumber is complex:
            print("Check solutions file; ComplexNumber is complex.")
            return 0

        # Test ComplexNumber.conjugate() (2 points).
        cn2 = cn.conjugate()
        if not isinstance(cn2, s.ComplexNumber):
            self.feedback += "ComplexNumber.conjugate() should return a "
            self.feedback += "new ComplexNumber object."
        else:
            points += self._eqTest(a, cn2.real,
                        "ComplexNumber.conjugate() failed on real part")
            points += self._eqTest(-1*b, cn2.imag,
                        "ComplexNumber.conjugate() failed on imag part")

        # Test ComplexNumber.__abs__() (1 point).
        a, b = randint(-50, 50, 2)
        cn = s.ComplexNumber(a, b)
        points += self._eqTest(sqrt(a**2 + b**2), abs(cn),
                                        "ComplexNumber.__abs__() failed")

        # Test ComplexNumber.__lt__() (2 points).
        cn1, cn2 = s.ComplexNumber(5, 7), s.ComplexNumber(1, 2)
        points += self._evalTest(cn1 < cn2, False,
                                "ComplexNumber.__lt__() failed")
        points += self._evalTest(cn2 < cn1, True,
                                "ComplexNumber.__lt__() failed")

        # Test ComplexNumber.__gt__() (2 points).
        cn1, cn2 = s.ComplexNumber(1, 2), s.ComplexNumber(3, 4)
        points += self._evalTest(cn1 > cn2, False,
                                "ComplexNumber.__gt__() failed")
        points += self._evalTest(cn2 > cn1, True,
                                "ComplexNumber.__gt__() failed")

        # Test ComplexNumber.__eq__() (2 points).
        cn1, cn2 = s.ComplexNumber(2, 3), s.ComplexNumber(3, 2)
        points += self._evalTest(cn1 == cn2, False,
                        "ComplexNumber.__eq__() failed on nonequal")
        cn1, cn2 = s.ComplexNumber(2, 3), s.ComplexNumber(2, 3)
        points += self._evalTest(cn2 == cn1, True,
                        "ComplexNumber.__eq__() failed on equal")

        # Test ComplexNumber.__ne__() (2 points).
        cn1, cn2 = s.ComplexNumber(2, 3), s.ComplexNumber(3, 2)
        points += self._evalTest(cn1 != cn2, True,
                        "ComplexNumber.__ne__() failed on nonequal")
        cn1, cn2 = s.ComplexNumber(2, 3), s.ComplexNumber(2, 3)
        points += self._evalTest(cn2 != cn1, False,
                        "ComplexNumber.__ne__() failed on equal")

        # Test ComplexNumber.__add__() (2 points).
        a, b, c, d = randint(-50, 50, 4)
        cn = s.ComplexNumber(a, b) + s.ComplexNumber(c, d)
        points += self._eqTest(a+c, cn.real,
                    "ComplexNumber.__add__() failed on real part")
        points += self._eqTest(b+d, cn.imag,
                    "ComplexNumber.__add__() failed on imag part")

        # Test ComplexNumber.__sub__() (2 points).
        a, b, c, d = randint(-50, 50, 4)
        cn = s.ComplexNumber(a, b) - s.ComplexNumber(c, d)
        points += self._eqTest(a-c, cn.real,
                    "ComplexNumber.__sub__() failed on real part")
        points += self._eqTest(b-d, cn.imag,
                    "ComplexNumber.__sub__() failed on real part")

        # Test ComplexNumber.__mul__() (4 points).
        a, b, c, d = randint(-50, 50, 4)
        cn1 =   ComplexNumber(a, b) *   ComplexNumber(c, d)
        cn2 = s.ComplexNumber(a, b) * s.ComplexNumber(c, d)
        points += 2*self._eqTest(cn1.real, cn2.real,
                    "ComplexNumber.__mul__() failed on real part")
        points += 2*self._eqTest(cn1.imag, cn2.imag,
                    "ComplexNumber.__mul__() failed on imag part")
        
        # Test ComplexNumber.__div__() (4 points).
        a, b, c, d = randint(-50, 50, 4)
        cn1 =   ComplexNumber(a, b) /   ComplexNumber(c, d)
        cn2 = s.ComplexNumber(a, b) / s.ComplexNumber(c, d)
        points += 2*self._eqTest(cn1.real, cn2.real,
                    "ComplexNumber.__div__() failed on real part")
        points += 2*self._eqTest(cn1.imag, cn2.imag,
                    "ComplexNumber.__div__() failed on imag part")

        return points

if __name__ == '__main__':
    import solutions as sol
    score, feedback = test(sol)

# END OF FILE =================================================================
