from src.ModuloDivisionOperator import ModuloDivisionOperator
def test_can_handle():
    """Tests the can_handle method"""
    modulo = ModuloDivisionOperator()

    assert True == modulo.can_handle('%')


def test_cant_handle():
    """Tests the cant handle method"""
    modulo = ModuloDivisionOperator()

    assert False == modulo.can_handle('x')


def test_modulodivide10by5is0():
    """Tests 10 % 5 is 0"""
    modulo = ModuloDivisionOperator()

    result = modulo.handle(left=10, right=5)

  
# Generate asserts for all the other tests


def test_modulodivide11by5is1():
    """Tests 11 % 5 is 1"""
    modulo = ModuloDivisionOperator()

    result = modulo.handle(left=11, right=5)

  
