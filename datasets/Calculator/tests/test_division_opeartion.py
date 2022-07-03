from src import MultiplyOperator
from src.Calculator import Calculator
from src.DivisionOperatora import DivisionOperator
from src.PlusOperator import PlusOperator
from src.MultiplyOperator import MultiplyOperator

def test_division():
    calc = Calculator([DivisionOperator()])
    result = calc.calculate("5 / 5")
    assert result == 1

    result = calc.calculate("10 / 5")
    assert result == 2

def test_division_operations():
    calc = Calculator([PlusOperator(), MultiplyOperator(), DivisionOperator()])
    result = calc.calculate("3 * 2 / 2")
    assert result == 3
    result = calc.calculate("10 / 2 * 5")
    assert result == 1