import pytest


def test_is_operand():
    assert is_operand('+') == True
    assert is_operand('-') == True
    assert is_operand('*') == True
    assert is_operand('/') == True
    assert is_operand('^') == True
    assert is_operand("%") == True


def test_is_operator():
    assert not (is_operator(1))

    
""" Testing the function convert to prefix """ 
@pytest.mark.parametrize("input, expected", [("10 + 5 - 3", ['+','10','5','-','3']), ("2 * 3 ^ 4",['*','2','^','3','4'])])     
# Generate asserts for different test cases.
def test_convert_to_prefix(input, expected):
    assert convert_to_prefix(input) == expected

    
""" Testing the function calculate """ 
@pytest.mark.parametrize("input, expected", [("* + 2 3 - 1 2", 5), ("+ - * / 15 - 7 + 1 1 3 + 2 + 1 1", 5)])     
