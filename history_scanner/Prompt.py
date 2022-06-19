class Prompt:
    def __init__(self, context_code: str, commit_msg:str, python_version: str = "3", test_lib: str = "pytest"):
        self.context_code = context_code
        self.commit_msg = commit_msg
        self.python_version = python_version
        self.test_lib = test_lib

    def __str__(self):
        return f'''###Python{self.python_version}
import {self.test_lib}
"""
Tests which are using ${self.test_lib}
The tests are testing - {self.commit_msg}
"""
def test_'''
