import ast


class CommitData:
    def __init__(self, commit_msg, file_asts):
        self.commit_msg = commit_msg
        self.file_asts = file_asts

    def __str__(self):
        string = f"{self.commit_msg}: \n"
        string += "\n".join([ast.dump(file_ast) for file_ast in self.file_asts])
        return string
