from math import floor
from transformers import GPT2TokenizerFast


class Prompt:

    MAX_TOKENS = 8000
    TOKENIZER = GPT2TokenizerFast.from_pretrained("gpt2")

    def __init__(self, context_code: str, commit_msg: str, python_version: str = "3", test_lib: str = "pytest"):
        self.context_code = context_code
        self.commit_msg = commit_msg
        self.python_version = python_version
        self.test_lib = test_lib
        self.message = f'''###Python{self.python_version}
{self.context_code}
import {self.test_lib}
"""
The tests are testing - {self.commit_msg}
"""
def test_'''

    def reduce_tokens(self):
        percent = 1.0
        while len(Prompt.TOKENIZER(self.message)['input_ids']) > Prompt.MAX_TOKENS:
            percent -= 0.1
            context_length = floor(len(self.context_code) * percent)
            self.message = f'''###Python{self.python_version}
{self.context_code[:context_length]}
import {self.test_lib}
"""
The tests are testing - {self.commit_msg}
"""
def test_'''

    def __str__(self):
        self.reduce_tokens()
        return self.message
