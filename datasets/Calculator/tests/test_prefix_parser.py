from src.Parser import convert_to_prefix

def test_single_digit():
    prefix = convert_to_prefix('1 + 2 + 3 + 5')
    assert prefix == ['+', '1', '+', '2', '+', '3', '5']

def test_multi_digit():
    prefix = convert_to_prefix('1 + 20 + 3 + 5')
    assert prefix == ['+', '1', '+', '20', '+', '3', '5']

def test_multi_operators():
    prefix = convert_to_prefix('1 + 20 * 3 + 5')
    assert prefix == ['+', '1', '*', '20', '+', '3', '5']