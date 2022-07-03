from src import MultiplyOperator
from src import MinusOperator
from src.Calculator import Calculator
from src.PlusOperator import PlusOperator
from src.MultiplyOperator import MultiplyOperator
from src.MinusOperator import MinusOperator
from src.Power import PowerOperator

def test_power_operation():
    calc = Calculator([PowerOperator()])
    result = calc.calculate("5 ^ 3")
    assert result == 125

def test_power_operations():
    calc = Calculator([PlusOperator(), MultiplyOperator(), MinusOperator(), PowerOperator()])
    result = calc.calculate("1 + 3 * 2 - 5 ^ 2")
    assert result == -68