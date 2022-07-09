from src.Parser import convert_to_prefix
def test_is_operand():
    assert not is_operand('1')
    assert is_operand('+')
    assert is_operand('-')
    assert is_operand('*')
    assert is_operand('/')
    assert is_operand('^')

    
"""  Added support for Modulo operation. The used operator for the operation is '%'. Acceptance criteria: The following equations are supported now: 1 % 2 = 1 2 % 3 = 2 10 % 5 = 0 1 + 10 % 3 = 2 """

    
def testModulo():   
# Generate asserts for the acceptance criteria
    assert convert_to_prefix('1 % 2') == ['%', '1', '2']
    assert convert_to_prefix('2 % 3') == ['%', '2', '3']
    assert convert_to_prefix('10 % 5') == ['%', '10' ,'5']
    assert convert_to_prefix('1 + 10 % 3') == ['+','1','%','10','3']

    
#def testModuloWithBrackets(): 
