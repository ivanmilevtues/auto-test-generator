from src import MultiplyOperator
from src.Calculator import Calculator
from src.PlusOperator import PlusOperator
from src.MultiplyOperator import MultiplyOperator

def test_multiply():
    calc = Calculator([MultiplyOperator()])
    result = calc.calculate("5 * 5")
    assert result == 25

def test_multiply_operations():
    calc = Calculator([PlusOperator(), MultiplyOperator()])
    result = calc.calculate("1 + 3 * 2")
    assert result == 7
    result = calc.calculate("2 * 2 + 10")
    assert result == 24