# test_solutions.py
"""Volume 1B: Testing.
<Name>
<Class>
<Date>
"""

import solutions as soln
import pytest
import math

# Problem 1: Test the addition and fibonacci functions from solutions.py
def test_addition():
    assert soln.addition(1,3) == 4
    assert soln.addition(-1,3) == 2
    assert soln.addition(-5,-7) == -12
    pass

def test_smallest_factor():
    assert soln.smallest_factor(1) == 1
    assert soln.smallest_factor(7) == 7
    assert soln.smallest_factor(9) == 3
    pass

# Problem 2: Test the operator function from solutions.py
def test_operator():
    assert soln.operator(1,1,"+") == 2
    assert soln.operator(1,1,"-") == 0
    assert soln.operator(1,1,"/") == 1
    assert soln.operator(1,1,"*") == 1

    with pytest.raises(Exception) as excinfo:
        soln.operator(1,1,7)
        assert excinfo.typename == 'ValueError'
        assert excinfo.value.args[0] == "Oper should be a string"

    with pytest.raises(Exception) as excinfo:
        soln.operator(1,1,"a")
        assert excinfo.typename =='ValueError'
        assert excinfo.value.args[0] == "Oper can only be: '+', '/', '-', or '*'"

    with pytest.raises(Exception) as excinfo:
        soln.operator(1,1,"ab")
        assert excinfo.typename == 'ValueError'
        assert excinfo.value.args[0] == "Oper should be one character"

    with pytest.raises(Exception) as excinfo:
        soln.operator(1,0,"/")
        assert excinfo.typename == 'ValueError'
        assert excinfo.value.args[0] == "You can't divide by zero!"
    pass

# Problem 3: Finish testing the complex number class
@pytest.fixture
def set_up_complex_nums():
    number_1 = soln.ComplexNumber(1, 2)
    number_2 = soln.ComplexNumber(5, 5)
    number_3 = soln.ComplexNumber(2, 9)
    number_4 = soln.ComplexNumber(0,0)
    return number_1, number_2, number_3, number_4

def test_complex_addition(set_up_complex_nums):
    number_1, number_2, number_3, number_4 = set_up_complex_nums
    assert number_1 + number_2 == soln.ComplexNumber(6, 7)
    assert number_1 + number_3 == soln.ComplexNumber(3, 11)
    assert number_2 + number_3 == soln.ComplexNumber(7, 14)
    assert number_3 + number_3 == soln.ComplexNumber(4, 18)

def test_complex_multiplication(set_up_complex_nums):
    number_1, number_2, number_3, number_4 = set_up_complex_nums
    assert number_1 * number_2 == soln.ComplexNumber(-5, 15)
    assert number_1 * number_3 == soln.ComplexNumber(-16, 13)
    assert number_2 * number_3 == soln.ComplexNumber(-35, 55)
    assert number_3 * number_3 == soln.ComplexNumber(-77, 36)

def test_conjugate(set_up_complex_nums):
    number_1, number_2, number_3, number_4 = set_up_complex_nums
    assert number_1.conjugate() == soln.ComplexNumber(1,-2)

def test_norm(set_up_complex_nums):
    number_1, number_2, number_3, number_4 = set_up_complex_nums
    assert number_1.norm() == math.sqrt(5)

def test_complex_subtraction(set_up_complex_nums):
    number_1, number_2, number_3, number_4 = set_up_complex_nums
    assert number_1 - number_2 == soln.ComplexNumber(-4, -3)
    assert number_1 - number_3 == soln.ComplexNumber(-1, -7)
    assert number_2 - number_3 == soln.ComplexNumber(3, -4)
    assert number_3 - number_3 == soln.ComplexNumber(0, 0)

def test_complex_str(set_up_complex_nums):
    number_1, number_2, number_3, number_4 = set_up_complex_nums
    assert str(number_1) == "1+2i"
    assert str(number_1.conjugate()) == "1-2i"


# Problem 4: Write test cases for the Set game.
