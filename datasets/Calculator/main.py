from src.DivisionOperatora import DivisionOperator
from src.PlusOperator import PlusOperator
from src.MultiplyOperator import MultiplyOperator
from src.MinusOperator import MinusOperator
from src.ModuloOperator import ModuloOperator

from src.Calculator import Calculator
from src.Power import PowerOperator


def setup_calculator():
    operators = [PlusOperator(), MultiplyOperator(), MinusOperator(), PowerOperator(), DivisionOperator(),
                 ModuloOperator()]
    return Calculator(operators)


def main():
    calculator = setup_calculator()
    print(f"Enter your equation without spaces. Supported operators: {calculator.operators}")
    print("To exit, type exit.")
    while True:
        new_line = input()
        if new_line.lower() == 'exit':
            exit(0)
        result = calculator.calculate(new_line)
        print(result)

if __name__ == '__main__':
    main()
