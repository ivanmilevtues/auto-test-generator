from src.DivisionOperatora import DivisionOperator
from src.PlusOperator import PlusOperator
from src.MultiplyOperator import MultiplyOperator
from src.MinusOperator import MinusOperator

from src.Calculator import Calculator
from src.Power import PowerOperator


if __name__ == '__main__':
    operators = [PlusOperator(), MultiplyOperator(), MinusOperator(), PowerOperator(), DivisionOperator()]
    print(f"Enter your equation without spaces. Supported operators: {operators}")
    print("To exit, type exit.")
    calc = Calculator(operators)
    while True:
        new_line = input()
        if new_line.lower() == 'exit':
            exit(0)
        result = calc.calculate(new_line)
        print(result)