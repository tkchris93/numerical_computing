# test_driver.py
"""Introductory Labs: Intro to Matplotlib. Test Driver."""

import sys
sys.path.insert(0, "../..")
from base_test_driver import BaseTestDriver, _autoclose


class TestDriver(BaseTestDriver):
    """Class for testing a student's work.

     5 points for problem 1
     5 points for problem 2
     5 points for problem 3
     5 points for problem 4
    10 points for problem 5
    10 points for problem 6

    Grade the entire lab assignment at once via test_all(), or grade one
    problem at a time via the different problemX() methods.
    """
    # Constructor -------------------------------------------------------------
    def __init__(self):
        """Initialize attributes."""
        BaseTestDriver.__init__(self)
        self.total = 40
        self.problems = [   (self.problem1, "Problem 1",  5),
                            (self.problem2, "Problem 2",  5),
                            (self.problem3, "Problem 3",  5),
                            (self.problem4, "Problem 4",  5),
                            (self.problem5, "Problem 5", 10),
                            (self.problem6, "Problem 6", 10)    ]

    # Main Routine ------------------------------------------------------------
    @staticmethod
    def main(student_module):
        """Grade a student's entire solutions file.

         5 points for problem 1
         5 points for problem 2
         5 points for problem 3
         5 points for problem 4
        10 points for problem 5
        10 points for problem 6

        Inputs:
            student_module: the imported module for the student's file.

        Returns:
            score (int): the student's score.
            feedback (str): a printout of results for the student.
        """
        return TestDriver().test_all(student_module)

    # Problems ----------------------------------------------------------------
    @_autoclose
    def problem1(self, s):
        """Test prob1(). 5 points."""
        s.prob1()
        print("""\nSpecifications:
        1. The single line should decrease exponentially to zero (5 points)
        (Graph may be bumpy)
        (Title and axis labels unnecessary)""")
        return self._grade(5, "prob1() plot does not match specifications")

    @_autoclose
    def problem2(self, s):
        """Test prob1(). 5 points."""
        s.prob2()
        print("""\nSpecifications:
        1. Three lines: sin(x), cos(x), arctan(x)       (3 points)
        2. Line domain is [-2pi, 2pi]                   (2 points)
        (Window domain doesn't need to be [-2pi, 2pi])
        (Title, axis labels, and legend unnecessary)""")
        return self._grade(5, "prob2() plot does not match specifications")

    @_autoclose
    def problem3(self, s):
        """Test prob1(). 5 points."""
        s.prob3()
        print("""\nSpecifications:
        1. Discontinuous line plotted over x-domain [-2,6]  (2 points)
        2. Think, magenta, dotted line                      (2 points)
        3. y-axis limits are exactly [-6,6]                 (1 point)
        (Title, axis labels, and legend unnecessary)""")
        return self._grade(5, "prob3() plot does not match specifications")

    @_autoclose
    def problem4(self, s):
        """Test prob1(). 5 points."""
        s.prob4()
        print("""\nSpecifications:
        1. Square grid of four subplots, each with one line.     (1 point)
        2. Each subplot has window limits [0, 2pi]x[-2, 2]       (1 point)
        3. Each subplot has a title                              (1 point)
        4. The overall figure has a title                        (1 point)
        5. The plots have the following colors and line styles:  (1 point)
            - sin(x): plain green line
            - sin(2x): red dashed line
            - 2sin(x): blue dashed line
            - 2sin(2x): magenta dotted line
        (Axis labels and legends unnecessary)""")
        return self._grade(5, "prob4() plot does not match specifications")

    @_autoclose
    def problem5(self, s):
        s.prob5()
        print("""\nSpecifications:
        1. Scatter plot in one subplot                          (1 point)
            - Clearly maps the United States                    (2 points)
            - Uses black pixel markers                          (1 point)
            - Both axes are labeled                             (1 point)
        2. Histogram in other subplot                           (1 point)
            - Low point at 4, peak at 18                        (1 point)
            - One bin per integer over [0, 23]                  (1 point)
            - x-axis limits are about [-.5, 23.5]               (1 point)
            - x-axis is labeled                                 (1 point)
        (Titles and legends unnecessary)
        (Aspect ratio may not be perfect)""")
        return self._grade(10, "prob5() plot does not match specification")

    @_autoclose
    def problem6(self, s):
        s.prob6()
        print("""\nSpecifications:
        1. Plots f(x,y) = sin(x)sin(y)/xy, which has one main   (3 points)
            hill in the middle and valleys on all four sides.
        2. Two subplots: one heat map, one contour plot         (2 points)
        3. Each subplot has limits [-2pi, 2pi]x[-2pi, 2pi]      (2 points)
        4. Non-default / non-horrible color scheme              (2 points)
        5. Each subplot has a colorbar                          (1 point)
        (Titles and axis labels unnecessary)
        (Equal aspect unnecessary -- might appear vertically squished""")
        return self._grade(10, "prob6() plot does not match specifications")

# Validation ==================================================================

if __name__ == '__main__':
    """Validate TestDriver by testing the solutions file."""
    import solutions
    # If using IPython, include the appropriate line:
    # reload(solutions)             # Python 2.7
    # from imp import reload        # Python 3.0-3.3
    # from importlib import reload  # Python 3.4+
    TestDriver.main(solutions)
