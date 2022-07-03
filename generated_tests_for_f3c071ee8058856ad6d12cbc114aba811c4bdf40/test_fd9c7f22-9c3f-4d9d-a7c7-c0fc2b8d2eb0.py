from src.Parser import convert_to_prefix
def test_convert_to_prefix():
    assert convert_to_prefix("5 + 7") == ['+', '5', '7']
def test_convert_to_prefix1():
    assert convert_to_prefix("5 * 7") == ['*', '5', '7']
def test_convert_to_prefix2():
    assert convert_to_prefix("10 / 5") == ['/','10','5']

# Generate asserts
if __name__ == '__main__':
    pytest.main(['-v', "-s", "question_1"])
