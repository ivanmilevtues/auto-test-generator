import ast
from ast import Import, ImportFrom

from history_scanner.commit_file import CommitFile


class CommitData:
    def __init__(self, commit_msg: str, source_files: [CommitFile], test_files: [CommitFile]):
        self.commit_msg = commit_msg
        self.source_files = source_files
        self.test_files = test_files

    def construct_prompt(self):
        self.rank_source_files()
        return f"""
### Python3
#
# {self.__source_str()}
#
### Generate tests for {self.commit_msg}
        """

    def rank_source_files(self):
        for file in self.source_files:
            for definition in file.source:
                if isinstance(definition, Import) or isinstance(definition, ImportFrom):
                    for name in definition.names:
                        if self.is_referencing_file_from_project(name):
                            file.rank_up()
        self.source_files = sorted(self.source_files, key=lambda f: f.ranking_score)
        return self.source_files

    def is_referencing_file_from_project(self, import_name):
        return bool([file for file in self.source_files if import_name in file.filename])

    def __source_str(self):
        return "".join([ast.dump(file.source_ast) for file in self.source_files])

    def __test_str(self):
        return "".join([file_ast for file_ast in self.test_files if file_ast is not None])

    def __str__(self):
        string = f"{self.commit_msg}: \n"
        string += "\n\nSource: \n\n".join([ast.dump(file_ast) for file_ast in self.source_files])
        string += "\n\nTest: \n\n".join([file_ast for file_ast in self.test_files if file_ast is not None])
        return string
