from src import MultiplyOperator
from src import MinusOperator
from src.Calculator import Calculator
from src.PlusOperator import PlusOperator
from src.MultiplyOperator import MultiplyOperator
from src.MinusOperator import MinusOperator

def test_minus_operation():
    calc = Calculator([MinusOperator()])
    result = calc.calculate("10 - 5")
    assert result == 5

    result = calc.calculate("5 - 10")
    assert result == -5

def test_starting_minus():
    calc = Calculator([MinusOperator(), PlusOperator()])
    result = calc.calculate('- 5 + 10')
    assert result == -15

def test_minus_operations():
    calc = Calculator([PlusOperator(), MultiplyOperator(), MinusOperator()])
    result = calc.calculate("1 + 3 * 2 - 5")
    assert result == -8
    result = calc.calculate("- 5 + 2 * 2 + 10")
    assert result == -29