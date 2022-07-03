from src.Operator import Operator


class PlusOperator(Operator):
    def can_handle(self, operator):
        return '+' == operator
    
    def handle(self, left_operand, righ_operand):
        return left_operand + righ_operand
    
    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return '+'