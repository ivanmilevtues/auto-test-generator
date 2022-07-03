def test_modulo_division():
    from src.ModuloDivisionOperator import ModuloDivisionOperator

    operator = ModuloDivisionOperator()
    assert operator.handle(10, 5) == 0
    assert operator.handle(11, 5) == 1
def test_can_handle():
    from src.ModuloDivisionOperator import ModuloDivisionOperator

    operator = ModuloDivisionOperator()
    assert operator.can_handle('%') is True
# Generate asserts for testing handle method
def generate_asserts(operand1, operand2):
    import sys

    module = __import__('src.ModuloDivisionOperator')
    class_name = getattr(module,'ModuloDivisionOperator')
    class_instance = class_name()

    print("assert class_instance.handle({}, {}) == 0".format(operand1, operand2))
	