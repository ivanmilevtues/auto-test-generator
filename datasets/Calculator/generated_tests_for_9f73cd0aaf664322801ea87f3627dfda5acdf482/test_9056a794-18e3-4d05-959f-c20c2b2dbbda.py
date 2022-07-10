from src.ModuloOperator import ModuloOperator
def test_modulo_operations():

    assert 1 == ModuloOperator().handle(1, 2)

    assert 2 == ModuloOperator().handle(2, 3)

    assert 0 == ModuloOperator().handle(10, 5)

def test_addition_with_modulo():

    addition = Addition()

    modulo = ModuloOperator()

    assert 2 == addition.handle(1, modulo.handle(10, 3))

 

import pytest

# Generate asserts for all operators

"""

The tests are testing: Added support for Modulo operation. The used operator for the operation is '%'.

Acceptance criteria:

The following equations are supported now:

1 % 2 = 1

2 % 3 = 2

10 % 5 = 0

1 + 10 % 3 = 2

"""
