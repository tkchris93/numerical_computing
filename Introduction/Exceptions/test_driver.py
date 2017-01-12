# test_driver.py
"""Introductory Labs: Exceptions and File I/O. Test Driver."""

import sys
sys.path.insert(1, "../..")
from base_test_driver import BaseTestDriver

import signal
from os import remove as rm
from solutions import ContentFilter


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1: arithmagic()
     5 points for problem 2: random_walk()
     5 points for problem 3: ContentFilter.__init__()
    25 points for problem 4: ContentFilter methods.

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    data_file = "__contentfilter_test__.txt"

    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize the feedback attribute."""
        BaseTestDriver.__init__(self)
        self.total = 40
        self.problems = [   (self.problem1, "Problem 1",  5),
                            (self.problem2, "Problem 2",  5),
                            (self.problem3, "Problem 3",  5),
                            (self.problem4, "Problem 4", 25)    ]

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

         5 points for problem 1: arithmagic()
         5 points for problem 2: random_walk()
         5 points for problem 3: ContentFilter.__init__()
        25 points for problem 4: ContentFilter methods.

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Problems ----------------------------------------------------------------
    def problem1(self, s):
        """Test arithmagic(). 5 points."""

        def _test(entries, err):
            standard_in = sys.stdin
            standard_out = sys.stdout
            try:

                with open("__IN__.txt", 'w') as f:
                    f.writelines([str(i) + '\n' for i in entries])
                sys.stdin = open("__IN__.txt", 'r')     # Redirect std in.
                sys.stdout = open("__OUT__.txt", 'w')   # Redirect std out.
                message = "\narithmagic() failed to raise a ValueError "

                try:
                    s.arithmagic()
                except ValueError as e:
                    sys.stdin = standard_in             # Reset std in.
                    sys.stdout = standard_out           # Reset std out.
                    print("\nCorrect Error message: {}".format(err))
                    print("Student Error message: {}".format(e))
                    return self._grade(1, "Poor error message")
                except Exception as e:
                    self.feedback += message
                    self.feedback +="(got {} instead)".format(self._objType(e))
                    self.feedback += "\n\tError message: {}".format(e)
                else:
                    self.feedback += message
                return 0
            finally:
                sys.stdin = standard_in                 # Reset std in.
                sys.stdout = standard_out               # Reset std out.
                rm("__IN__.txt")
                rm("__OUT__.txt")

        points  = _test([1234], "Input must be 3 digits")
        points += _test([121],
                            "First and last digit must differ by 2 or more")
        points += _test([123, 323], "Incorrect reversal")
        points += _test([123, 321, 111], "Incorrect difference")
        points += _test([123, 321, 198, 899], "Incorrect reversal")

        return points

    def problem2(self, s):
        """Test random_walk(). 5 points."""

        points = 0
        def _handle(signum, frame):
            raise KeyboardInterrupt("Arificial KeyboardInterrupt")

        # Let random_walk() it run to completion (2 points).
        print("\nCorrect Output:\tProcess Completed\nStudent Output:\t"),
        if s.random_walk(10000) is None:
            self.feedback += "\nrandom_walk() failed to return a value"
        else:
            points += 1
        points += self._grade(1,
                        "random_walk() failed to print 'Process Completed'")

        # Interrupt random_walk() it with a KeyboardInterrupt (3 points).
        print("\nCorrect Output:\tProcess Interrupted at iteration <i>")
        print("Student Output:\t"),
        signal.signal(signal.SIGALRM, _handle)
        signal.alarm(1)
        try:
            s.random_walk(1e12)
        except KeyboardInterrupt:
            self.feedback += "\nrandom_walk() failed to handle the "
            self.feedback += "KeyboardInterrupt"
        else:
            points += 2
        points += self._grade(1,
                        "random_walk() failed to print 'Process Interrupted'")

        return points

    def problem3(self, s):
        """Test ContentFilter.__init__(). 5 points."""
        points = 0

        # Test faulty initialization (2 points).
        try:
            x = s.ContentFilter(123456789)
        except TypeError as e:
            points += 2
        except Exception as e:
            self.feedback += "\nContentFilter.__init__() failed to raise a "
            self.feedback += "TypeError (got {} instead)".format(
                                                            self._objType(e))
        else:
            self.feedback += "\nFailed to raise a TypeError"

        # Test proper initialization (3 points).
        with open(self.data_file, 'w') as testfile:
            testfile.write("simple test")
        x = s.ContentFilter(self.data_file)
        rm(self.data_file)
        return points + 3

    def problem4(self, s):
        """Test the ContentFilter class's methods. 25 points."""

        with open(self.data_file, 'w') as testfile:
            testfile.write("A b C d E f G\nh I j K l M n\n"
                           "O p Q r S t U\nv W x Y z Z z")

        def _test_bad(cf, method, *args, **kwargs):
            """Test that eval(statement) raises an ValueError."""
            ags = ["'{}'".format(arg) for arg in args]
            kwgs = ["{}='{}'".format(key, val) for key,val in kwargs.items()]
            message = "\nContentFilter.{}({}, {}) failed to raise a ValueError".format(method, ", ".join(ags), ", ".join(kwgs))
            try:
                eval("cf.{}(*args, **kwargs)".format(method))
            except ValueError:
                return 1
            except Exception as e:
                self.feedback += message
                self.feedback +="\n\t(got {} instead)".format(self._objType(e))
            else:
                self.feedback += message
            return 0

        def _test_good(cf, method, value, *args, **kwargs):
            ags = ["'{}'".format(arg) for arg in args]
            kwgs = ["{}='{}'".format(key, val) for key,val in kwargs.items()]
            message = "ContentFilter.{}({}, {})".format(
                                    method, ", ".join(ags), ", ".join(kwgs))
            eval("cf.{}(*args, **kwargs)".format(method))
            print("\n{}:\n".format(message))
            with open(args[0], 'r') as f:
                print(f.read())
            return self._grade(value, message + " failed")

        CF = s.ContentFilter(self.data_file)

        # Test that each method raises an ValueError for bad 'mode' (3 points).
        points  = _test_bad(CF, "uniform",   "_OUT_", mode='z')
        points += _test_bad(CF, "reverse",   "_OUT_", mode='z')
        points += _test_bad(CF, "transpose", "_OUT_", mode='z')

        # Test that uniform() and reverse() raise ValueErrors (2 points).
        points += _test_bad(CF, "uniform", "_OUT_", case="middle")
        points += _test_bad(CF, "reverse", "_OUT_", unit="chunk")

        print("\nSource file:\n")
        with open(self.data_file) as f:
            print(f.read())

        # Test each method with correct usage (15 points).
        points += _test_good(CF, "uniform", 3, "_OUT_", mode='w', case="upper")
        points += _test_good(CF, "uniform", 3, "_OUT_", mode='w', case="lower")
        points += _test_good(CF, "reverse", 3, "_OUT_", mode="w", unit="word")
        points += _test_good(CF, "reverse", 3, "_OUT_", mode="w", unit="line")
        points += _test_good(CF, "transpose", 3, "_OUT_", mode="w")
        rm("_OUT_")

        # Test ContentFilter.__str__() (5 points).
        if str(ContentFilter(self.data_file)) != str(CF):
            print("\nCorrect ContentFilter.__str__() output:\n")
            print(ContentFilter(self.data_file))
            print("\nStudent ContentFilter.__str__() output:\n")
            print(CF)
            points += self._grade(5,
                        "ContentFilter.__str__() failed:\n\n{}\n".format(CF))
        else:
            points += 5

        rm(self.data_file)
        return points

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
