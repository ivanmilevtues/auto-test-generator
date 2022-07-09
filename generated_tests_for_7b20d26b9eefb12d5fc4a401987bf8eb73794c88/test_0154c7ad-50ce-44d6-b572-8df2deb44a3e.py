def test_modulo_operator():
    """The tests are testing: Added support for Modulo operation. The used operator for the operation is '%'."""
    calculator = setup_calculator()

    result = calculator.calculate('1 % 2')
    assert result == 1, f"Expected 1 but was {result}"

    result = calculator.calculate('2 % 3')
    assert result == 2, f"Expected 2 but was {result}"

    result = calculator.calculate('10 % 5')
    assert result == 0, f"Expected 0 but was {result}"

    
# Generate asserts for the acceptance criteria
def test_modulo_operator():
    """The tests are testing: Added support for Modulo operation. The used operator for the operation is '%'."""
    calculator = setup_calculator()

    result = calculator.calculate('1 % 2')
    assert result == 1, f"Expected 1 but was {result}"

    result = calculator.calculate('2 % 3')
    assert result == 2, f"Expected 2 but was {result}"

    result = calculator.calculate('10 % 5')
    assert result == 0, f"Expected 0 but was {result}"

    
