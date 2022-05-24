import ast
from ast import Import, ImportFrom

from history_scanner.commit_file import CommitFile

MAX_ALLOWED_TOKENS = 4000


class CommitData:
    def __init__(self, commit_msg: str, source_files: [CommitFile], test_files: [CommitFile]):
        self.commit_msg = commit_msg
        self.source_files = source_files
        self.test_files = test_files

    def construct_prompt(self):
        self.rank_source_files()
        return f'''
### Python3
{self.__source_str()}
"""
Test class which tests {self.commit_msg}
"""
class Test'''

    def rank_source_files(self):
        for file in self.source_files:
            for definition in file.source_ast.body:
                if isinstance(definition, Import) or isinstance(definition, ImportFrom):
                    for name in definition.names:
                        if self.is_referencing_file_from_project(name.name):
                            file.rank_up()
        self.source_files = sorted(self.source_files, key=lambda f: (f.ranking_score, len(f.source)), reverse=True)
        return self.source_files

    def is_referencing_file_from_project(self, import_name):
        return bool([file for file in self.source_files if import_name in file.filename])

    def __source_str(self):
        sources = ""
        for file in self.source_files:
            if len(sources.split(r'\s')) + len(file.source.split(r'\s')) < MAX_ALLOWED_TOKENS:
                sources += '\n' + file.source
                # TODO: Think if this is optimal probably I should have more than one test case scenarios
                # Think on how to differentiate different AC: tasks. Probably only the "Controller" or the entry
                # point is to be tested for the purpose of E2E/functional testing
            else:
                break
        return sources

    def __test_str(self):
        return "".join([file_ast for file_ast in self.test_files if file_ast is not None])

    def __str__(self):
        string = f"{self.commit_msg}: \n"
        string += "\n\nSource: \n\n".join([ast.dump(file_ast) for file_ast in self.source_files])
        string += "\n\nTest: \n\n".join([file_ast for file_ast in self.test_files if file_ast is not None])
        return string
