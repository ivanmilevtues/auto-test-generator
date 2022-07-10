def test_modulo_operator():
    calculator = setup_calculator()
    assert calculator.calculate('1%2') == 1, "The result is not equal to one."
    assert calculator.calculate('2%3') == 2, "The result is not equal to two."
    assert calculator.calculate('10%5') == 0, "The result is not equal to zero."


""" The tests are testing: Added support for power operation. The used operator for the operation is '^'.  """


def test_power_operator():
    calculator = setup_calculator()
    assert calculator.calculate('1^0') == 1, 'the result of 1^0 should be 1'


def test_division_operator():
    pass
# Generate asserts
    calculator = setup_calculator()
    assert calculator.calculate('1/2') == 0.5, "The result is not equal to one."


def test_plus_operator():
    
