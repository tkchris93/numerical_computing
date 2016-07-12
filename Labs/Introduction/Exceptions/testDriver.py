# solution.py
"""Introductory Labs: Exceptions and File I/O. Test Driver."""

import signal
from os import remove as rm

def test(student_module):
    """Test script. Import the student's solutions file as a module.

    5  points for problem 1: arithmagic()
    5  points for problem 2: random_walk()
    5  points for problem 3: ContentFilter.__init__()
    25 points for problem 4: ContentFilter methods.

    Inputs:
        student_module: the imported module for the student's file.

    Returns:
        score (int): the student's score, out of 40.
        feedback (str): a printout of test results for the student.
    """
    tester = _testDriver()
    tester.test_all(student_module)
    return tester.score, tester.feedback


class _testDriver(object):
    """Class for testing a student's work.

    Attributes:
        Score (int)
        Feedback (str)
    """

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        self.feedback = ""

    # Main routine ------------------------------------------------------------
    def test_all(self, student_module, total=40):
        """Grade the provided module on each problem and compile feedback."""
        # Reset feedback and score.
        self.feedback = ""
        self.score = 0

        def test_one(problem, label, value):
            """Test a single problem, checking for errors."""
            try:
                self.feedback += "\n\n{} ({} points):".format(label, value)
                points = problem(student_module)
                self.score += points
                self.feedback += "\nScore += {}".format(points)
            except BaseException as e:
                self.feedback += "\n{}: {}".format(self._errType(e), e)

        # Grade each problem.
        test_one(self.problem1, "Problem 1",  5)   # Problem 1:  5 points.
        test_one(self.problem2, "Problem 2",  5)   # Problem 2:  5 points.
        test_one(self.problem3, "Problem 3",  5)   # Problem 3:  5 points.
        test_one(self.problem4, "Problem 4", 25)   # Problem 4: 25 points.

        # Report final score.
        percentage = (100. * self.score) / total
        self.feedback += "\n\nTotal score: {}/{} = {}%".format(
                                    self.score, total, round(percentage, 2))
        if   percentage >=  98: self.feedback += "\n\nExcellent!"
        elif percentage >=  90: self.feedback += "\n\nGreat job!"

        # Add comments (optionally).
        print(self.feedback)
        comments = str(raw_input("Comments: "))
        if len(comments) > 0:
            self.feedback += '\n\n\nComments:\n\t{}'.format(comments)

    # Helper Functions --------------------------------------------------------
    @staticmethod
    def _errType(error):
        """Get just the name of the exception 'error' in string format."""
        return str(type(error).__name__)

    def _eqTest(self, correct, student, message):
        """Test to see if 'correct' and 'student' are equal.
        Report the given 'message' if they are not.
        """
        if correct == student:
            return 1
        else:
            self.feedback += "\n{}".format(message)
            self.feedback += "\n\tCorrect response: {}".format(correct)
            self.feedback += "\n\tStudent response: {}".format(student)
            return 0

    def _grade(self, points, message=None):
        """Manually grade a problem worth 'points'. Return the score.
        If full points are not earned, get feedback on the problem.
        """
        credit = -1
        while credit > points or credit < 0:
            try:
                credit = int(input("\nScore out of {}: ".format(points)))
            except:
                credit = -1
        if credit != points:
            # Add comments (optionally),
            comments = raw_input("Comments: ")
            if len(comments) > 0:
                self.feedback += "\n{}".format(comments)
            # Or add a predetermined error message.
            elif message is not None:
                self.feedback += "\n{}".format(message)
        return credit

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test arithmagic(). 5 points."""

        def test_arithmagic(entries):
            try:
                print("\nEnter the following sequence: {}".format(entries))
                s.arithmagic()
            except ValueError as e:
                print("\nStudent Error message: {}".format(e))
                return self._grade(1, "Use a more informative error message")
            except BaseException as e:
                self.feedback += "\narithmagic() failed to raise a ValueError "
                self.feedback += "(got {} instead)".format(self._errType(e))
                self.feedback += "\n\tError message: {}".format(e)
            else:
                self.feedback += "\narithmagic() failed to raise a ValueError"
            return 0

        points  = test_arithmagic([1234])
        points += test_arithmagic([121])
        points += test_arithmagic([123, 323])
        points += test_arithmagic([123, 321, 111])
        points += test_arithmagic([123, 321, 198, 899])

        return points

    def problem2(self, s):
        """Test Problem 2. 5 points."""
        def _handle(signum, frame):
            raise KeyboardInterrupt("Arificial KeyboardInterrupt")

        # Test forever(), letting it run to completion (2 points).
        print("\nCorrect Output:\tProcess Completed\nStudent Output:\t"),
        points = self._eqTest(s.forever(10),10,
                                "forever() returned incorrect value")
        points += self._grade(1, "'Process Completed' failed to print")

        # Test forever(), interrupting it with a KeyboardInterrupt (3 points).
        print("\nCorrect Output:\tProcess Interrupted\nStudent Output:\t"),
        signal.signal(signal.SIGALRM, _handle); signal.alarm(1)
        try:
            x = s.forever(1000000000)
        except KeyboardInterrupt:
            self.feedback += "\nKeyboardInterrupt not caught in forever()"
        else:
            points += 2
        points += self._grade(1, "'Process Interrupted' failed to print")

        return points

    def problem3(self, s):
        """Test ValueError. 5 points."""
        if not hasattr(s, "ValueError"):
            raise NotImplementedError("Problem 3 Incomplete")

        # Check that ValueError inherits from Exception (1 point).
        points = 0
        if issubclass(s.ValueError, Exception):
            points += 1

        # Check that ValueError behaves like Exception (4 points).
        try:
            raise s.ValueError("This", "is", "a", "test")
        except s.ValueError as e:
            points += 4
        except BaseException as e:
            self.feedback += "\nFailed to raise an ValueError "
            self.feedback += "(got a %s instead)"%self._errType(e)

        return points

    def problem4(self, s):
        """Test ContentFilter.__init__(). 5 points."""

        if not hasattr(s, "ContentFilter"):
            raise NotImplementedError("Problem 4 Incomplete")
        points = 0

        # Test faulty initialization (2 points).
        try:
            x = s.ContentFilter(123456789)
        except TypeError as e:
            points += 2
        except BaseException as e:
            self.feedback += "\nFailed to raise a TypeError "
            self.feedback += "(got a %s instead)"%self._errType(e)
        else:
            self.feedback += "\nFailed to raise a TypeError"

        # Test proper initialization (3 points).
        x = s.ContentFilter("contentfilter_test.txt")
        return points + 3

    def problem5(self, s, sourcefile="contentfilter_test.txt"):
        """Test the ContentFilter class's methods. 20 points."""
        if not hasattr(s, "ContentFilter"):
            raise NotImplementedError("Problem 5 Incomplete")
        sFilter = s.ContentFilter(sourcefile)

        def test_bad(x, statement, method):
            """Test that eval(statement) raises an ValueError."""
            try:
                eval(statement)
            except s.ValueError:
                return 1
            except BaseException as e:
                self.feedback += "\nContentFilter.%s() "%method
                self.feedback += "failed to raise an ValueError "
                self.feedback += "(got a %s instead)"%self._errType(e)
            else:
                self.feedback += "\nContentFilter.%s() "%method
                self.feedback += "failed to raise an ValueError"
            return 0

        # Test that each method raises an ValueError for bad 'mode'.
        points  = test_bad(sFilter, 'x.hyphenate("out.txt", mode="z")',
                                                                "hyphenate")
        points += test_bad(sFilter, 'x.uniform("out.txt", mode="z")',
                                                                "uniform")
        points += test_bad(sFilter, 'x.reverse("out.txt", mode="z")',
                                                                "reverse")
        points += test_bad(sFilter, 'x.transpose("out.txt", mode="z")',
                                                                "transpose")

        # Test that uniform() and reverse() raise ValueErrors correctly
        points += test_bad(sFilter, 'x.uniform("out.txt", case="middle")',
                                                                    'uniform')
        points += test_bad(sFilter, 'x.reverse("out.txt", unit="chunk")',
                                                                    'reverse')

        def test_good(x, statement, method, value):
            """Test a ContentFilter method with correct usage."""
            print("\nOutput of ContentFilter.%s:\n"%method)
            filename = "temporary_outfile.txt"
            eval(statement)
            with open(filename, 'r') as f:
                for line in f:
                    print(line.rstrip())
            return self._grade(value, "ContentFilter.%s failed"%method)

        # Test each method with correct usage (11 points).
        print("\nSource file for testing ContentFilter class:\n")
        with open(sourcefile) as f:
            for line in f:
                print(line.rstrip())

        points += test_good(sFilter, 'x.hyphenate(filename, mode="w")',
                                                        'hyphenate()', 2)
        points += test_good(sFilter,
                            'x.uniform(filename, mode="w", case="upper")',
                                                'uniform(case="upper")', 1)
        points += test_good(sFilter,
                            'x.uniform(filename, mode="w", case="lower")',
                                                'uniform(case="lower")', 1)
        points += test_good(sFilter,
                            'x.reverse(filename, mode="w", unit="word")',
                                                'reverse(unit="word")', 2)
        points += test_good(sFilter,
                            'x.reverse(filename, mode="w", unit="line")',
                                                'reverse(unit="line")', 2)
        points += test_good(sFilter, 'x.transpose(filename, mode="w")',
                                                        'transpose()', 3)
        rm("temporary_outfile.txt")

        # Test ContentFilter.__str__() (3 points).
        template = ContentFilter(sourcefile)
        print("\nCorrect ContentFilter.__str__() output:\n")
        print(template)
        print("\nStudent ContentFilter.__str__() output:\n")
        print(sFilter)
        points += self._grade(3,
                        "ContentFilter.__str__() failed:\n\n%s\n"%sFilter)
        return points


# Validation ==================================================================

if __name__ == '__main__':
    import solutions
    test(solutions)
