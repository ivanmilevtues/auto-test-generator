import ast


class CommitData:
    def __init__(self, commit_msg, source_file_asts, test_file_asts):
        self.commit_msg = commit_msg
        self.source_file_asts = source_file_asts
        self.test_file_asts = test_file_asts

    def construct_prompt(self):
        return f"""
### Python3
#
# {self.__source_str()}
#
### Generate tests for {self.commit_msg}
        """

    def __source_str(self):
        return "".join([ast.dump(file_ast) for file_ast in self.source_file_asts])

    def __test_str(self):
        return "".join([file_ast for file_ast in self.test_file_asts if file_ast is not None])

    def __str__(self):
        string = f"{self.commit_msg}: \n"
        string += "\n\nSource: \n\n".join([ast.dump(file_ast) for file_ast in self.source_file_asts])
        string += "\n\nTest: \n\n".join([file_ast for file_ast in self.test_file_asts if file_ast is not None])
        return string
