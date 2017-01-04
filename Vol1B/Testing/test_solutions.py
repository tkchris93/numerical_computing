# test_solutions.py
"""Volume 1B: Testing. Solutionss file (for test_specs.py)."""

import solutions as specs
import pytest
import math

# Problem 1 test the addition and fibonacci functions from specs.py
def test_addition():
    assert specs.addition(1,2) == 3
    assert specs.addition(4,-8) == -4

def test_smallest_factor():
    assert specs.smallest_factor(15) == 3
    assert specs.smallest_factor(1) == 1
    assert specs.smallest_factor(23) == 23

# Problem 2 test the operator function from specs.py
def test_operator():
    assert specs.operator(3,5,'+') == 8
    assert specs.operator(10,6,'-') == 4
    assert specs.operator(3,2,'*') == 6
    assert specs.operator(7,2,'/') == 3.5
    pytest.raises(ValueError, specs.operator, a=1, b=1, oper=1)
    pytest.raises(ValueError, specs.operator, a=1, b=1, oper='++')
    pytest.raises(ValueError, specs.operator, a=1, b=0, oper='/')
    pytest.raises(ValueError, specs.operator, a=1, b=1, oper='%')


# Problem 3 finish testing the complex number class
@pytest.fixture
def set_up_complex_nums():
    number_1 = specs.ComplexNumber(1, 2)
    number_2 = specs.ComplexNumber(5, 5)
    number_3 = specs.ComplexNumber(2, 9)
    return number_1, number_2, number_3

def test_complex_addition(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 + number_2 == specs.ComplexNumber(6, 7)
    assert number_1 + number_3 == specs.ComplexNumber(3, 11)
    assert number_2 + number_3 == specs.ComplexNumber(7, 14)
    assert number_3 + number_3 == specs.ComplexNumber(4, 18)

def test_complex_multiplication(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 * number_2 == specs.ComplexNumber(-5, 15)
    assert number_1 * number_3 == specs.ComplexNumber(-16, 13)
    assert number_2 * number_3 == specs.ComplexNumber(-35, 55)
    assert number_3 * number_3 == specs.ComplexNumber(-77, 36)

def test_complex_subtraction(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 - number_2 == specs.ComplexNumber(-4, -3)
    assert number_2 - number_3 == specs.ComplexNumber(3, -4)
    assert number_3 - number_1 == specs.ComplexNumber(1, 7)
    assert number_3 - number_3 == specs.ComplexNumber(0,0)

def test_complex_conjugate(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1.conjugate() == specs.ComplexNumber(1, -2)
    assert number_2.conjugate() == specs.ComplexNumber(5, -5)
    assert number_3.conjugate() == specs.ComplexNumber(2, -9)

def test_complex_norm(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1.norm() == math.sqrt(5)
    assert number_2.norm() == math.sqrt(50)
    assert number_3.norm() == math.sqrt(85)

def test_complex_division(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    zero = specs.ComplexNumber(0, 0)
    pytest.raises(ValueError, specs.ComplexNumber.__div__, number_1, zero)
    assert number_1 / number_2 == specs.ComplexNumber(0.3, 0.1)
    assert number_2 / number_2 == specs.ComplexNumber(1, 0)
    assert number_2 / number_3 == specs.ComplexNumber(11./17., -7./17.)

def test_complex_equals(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert (number_1 == number_1) == True
    assert (number_2 == number_3) == False
def test_complex_string(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert str(number_1) == '1+2i'
    assert str(number_2) == '5+5i'
    assert str(number_3) == '2+9i'


# Problem 4
def test_read_in_cards():
    # Correctly formated input
    assert specs.read_in_cards("hands/hand1.txt") == ["2001","2101","0120",
        "2012", "1020", "0212", "1112", "2020", "0101", "0221", "1122", "2021"]

    # Invalid file Name
    with pytest.raises(Exception) as excinfo:
        specs.read_in_cards("nofile.txt")
    assert excinfo.typename == "IOError"

    # 12 Cards in each file
    with pytest.raises(Exception) as excinfo:
        specs.read_in_cards("hands/hand8.txt")
    assert excinfo.typename == "ValueError"
    assert excinfo.value.args[0] == "There must be 12 cards in each file"

    # Card has wrong length
    with pytest.raises(Exception) as excinfo:
        specs.read_in_cards("hands/hand2.txt")
    assert excinfo.typename == "ValueError"
    assert excinfo.value.args[0] == "10111 is invalid: wrong number of characters"

    # Cards have wrong characters
    with pytest.raises(Exception) as excinfo:
        specs.read_in_cards("hands/hand3.txt")
    assert excinfo.typename == "ValueError"
    assert excinfo.value.args[0] == "20a1 can only contain the digits 0, 1 and 2"

    # Duplicate cards
    with pytest.raises(Exception) as excinfo:
        specs.read_in_cards("hands/hand4.txt")
    assert excinfo.typename == "ValueError"
    assert excinfo.value.args[0] == "There may not be any duplicate cards"

def test_is_set():
    assert specs.is_set("0000", "1111", "2222") == True
    assert specs.is_set("0000", "1111", "2220") == False
    assert specs.is_set("0120", "1201", "2012") == True
    assert specs.is_set("1221", "1012", "2120") == False
    assert specs.is_set("1000", "2000", "0000") == True

def test_count_matches():
    assert specs.count_matches("hands/hand1.txt") == 5
    assert specs.count_matches("hands/hand5.txt") == 2
    assert specs.count_matches("hands/hand6.txt") == 0
    assert specs.count_matches("hands/hand7.txt") == 12
