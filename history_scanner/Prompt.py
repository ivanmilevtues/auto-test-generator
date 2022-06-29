import ast
from math import floor

from transformers import GPT2TokenizerFast

from history_scanner.commit_file import CommitFile


class Prompt:

    MAX_TOKENS = 8000
    TOKENIZER = GPT2TokenizerFast.from_pretrained("gpt2")

    def __init__(self, context_file: CommitFile, commit_msg: str, python_version: str = "3", test_lib: str = "pytest"):
        self.context_file = context_file
        self.commit_msg = commit_msg
        self.python_version = python_version
        self.test_lib = test_lib

    def to_prompts(self):
        base_msg = f'###Python{self.python_version}\n{self.context_file.source}'

        if len(self.context_file.related_source) == 0:
            test_description = f'''import {self.test_lib}
"""
The tests are testing: {self.commit_msg}
"""
def test_'''
            yield self.reduce_tokens(base_msg, test_description)

        for token, expr in self.context_file.related_source:
            test_description = f'''import {self.test_lib}
"""
{self.commit_msg}
The tests are testing: {self.__expr_to_string(expr)} {expr.name}
"""
def test_'''
            yield self.reduce_tokens(base_msg, test_description)

    def reduce_tokens(self, reducible_msg, addition):
        percent = 1.0
        while len(Prompt.TOKENIZER(reducible_msg + addition)['input_ids']) > Prompt.MAX_TOKENS:
            percent -= 0.1
            context_length = floor(len(self.context_file.source) * percent)
            reducible_msg = f'###Python{self.python_version}\n{self.context_file.source[:context_length]}'
        return reducible_msg + addition

    @staticmethod
    def __expr_to_string(expr):
        if isinstance(expr, ast.ClassDef):
            return "class"
        elif isinstance(expr, ast.FunctionDef):
            return "function"
        raise RuntimeError(f"Unsupported expr to string {expr}")

    def __str__(self):
        return f"Prompt for {self.commit_msg} and {self.context_file}"
