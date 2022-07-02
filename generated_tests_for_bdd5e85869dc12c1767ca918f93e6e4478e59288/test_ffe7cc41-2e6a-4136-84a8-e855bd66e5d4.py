from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser

import ast
def test_is_test_file():
    parser = GitHistoryDataSetParser()
    
    assert True == parser.__is_test_file(ModifiedFile('tests/files/main.py', None, ModificationType.ADD))

 
"""
End to end second test.
The tests are testing: function __has_additions with empty method list before modification and not empty method list after modification. 
"""  
def test_has_additions():
    modifiedFile = ModifiedFile(None, None, ModificationType.MODIFY) 
# Generate asserts
    modifiedFile.methods_before = []
    modifiedFile.methods = [Method(None, None)]

    parser = GitHistoryDataSetParser()
    
    assert True == parser.__has_additions(modifiedFile) 


"""
End to end second test.
The tests are testing: function __is_expr_related_to_code with a token in the expression name. 
"""  
def test__is_expr_related():
    expr = ast.FunctionDef("test", None, None, None, None)

    commitMsgTokens = ["t"]   