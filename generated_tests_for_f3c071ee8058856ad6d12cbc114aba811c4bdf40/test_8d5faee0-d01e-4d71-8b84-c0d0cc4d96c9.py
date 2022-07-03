def test_modulo_division_operator():
    from src.Operator import Operator

    class ModuloDivisionOperator(Operator):
        def can_handle(self, operator):
            return '%' == operator

        def handle(self, left_operand, righ_operand):
            return left_operand % righ_operand

        def __str__(self) -> str:
            return self.__repr__()

        def __repr__(self) -> str:
            return '%'

    assert ModuloDivisionOperator().can_handle('%') is True
# Generate asserts for all the acceptance criteria
def test_modulo_division_operator():
    from src.Operator import Operator

    class ModuloDivisionOperator(Operator):
        def can_handle(self, operator):
            return '%' == operator

        def handle(self, left_operand, righ_operand):
            return left_operand % righ_operand

        def __str__(self) -> str:
            return self.__repr__()

        def __repr__(self) -> str:
            return '%'

    assert ModuloDivisionOperator().can_handle('%') is True