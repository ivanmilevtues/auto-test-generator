from src.Parser import convert_to_prefix
def test_is_operand():
    assert is_operand('+') == True
    assert is_operand('-') == True
    assert is_operand('/') == True
    assert is_operand('*') == True
    assert is_operand('^') == True
def test_convert2prefix():

	assert convert_to_prefix("5 + 6")==['5', '6', '+']

	assert convert_to_prefix("3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3")==['3','4','2','*','1','5','-','2','3','^','^','/', '+' ] 

	assert convert_to_prefix("a - b / c * d % e = f")==['a',"b","c","/", "d", "e", "%", "*" ,"-" ,"f" , "="]
# Generate asserts for all the test cases given in description
def test_convert2prefix():

	assert convert_to_prefix("5 + 6")==['5', '6', '+']

	assert convert_to_prefix("3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3")==['3','4','2','*','1','5','-','2','3','^','^','/', '+' ] 

	assert convert_to_prefix("a - b / c * d % e = f")==['a',"b","c","/", "d", "e", "%", "*" ,"-" ,"f" , "="]
