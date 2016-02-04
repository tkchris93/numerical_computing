import solutions
import pytest

#problem 1 test the operator function from solutions.py
def test_addition():
    pass

#problem 2 test the division and operator functions from solutions.py
def test_operator():
    pass

def test_divide():
    assert solutions.divide(1,2) == .5
    assert solutions.divide(5,4) == 1.25
    with pytest.raises(Exception) as excinfo:
        solutions.divide(4,0)
    excinfo.typename == 'ValueError'
    assert excinfo.value.args[0] == "You can't give a zero for b, that breaks this function"

#problem 3 finish testing the complex number class
@pytest.fixture
def set_up_complex_nums():
    number_1 = solutions.ComplexNumber(1, 2)
    number_2 = solutions.ComplexNumber(5, 5)
    number_3 = solutions.ComplexNumber(2, 9)
    return number_1, number_2, number_3

def test_complex_addition(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 + number_2 == solutions.ComplexNumber(6, 7)
    assert number_1 + number_3 == solutions.ComplexNumber(3, 11)
    assert number_2 + number_3 == solutions.ComplexNumber(7, 14)
    assert number_3 + number_3 == solutions.ComplexNumber(4, 18)
def test_complex_multiplication(set_up_complex_nums):
    number_1, number_2, number_3 = set_up_complex_nums
    assert number_1 * number_2 == solutions.ComplexNumber(-5, 15)
    assert number_1 * number_3 == solutions.ComplexNumber(-16, 13)
    assert number_2 * number_3 == solutions.ComplexNumber(-35, 55)
    assert number_3 * number_3 == solutions.ComplexNumber(-77, 36)

#problem 4 test the linked list class from solutions.py
def test_linked_list_node_init():
    pass
