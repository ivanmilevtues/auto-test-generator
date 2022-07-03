class Operator:
    def can_handle(self, operator: str) -> bool:
        pass

    def handle(self, left_operand, right_operand) -> int:
        pass