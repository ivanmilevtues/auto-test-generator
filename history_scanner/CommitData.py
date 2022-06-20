import ast
from ast import Import, ImportFrom, ClassDef
import re

from history_scanner.Prompt import Prompt
from history_scanner.commit_file import CommitFile

MAX_ALLOWED_TOKENS = 2000  # 8K is the limit and 1,5K words are 2K tokens

TOP_FILES = 3


class CommitData:
    def __init__(self, commit_id: str, commit_msg: str, source_files: [CommitFile], test_files: [CommitFile]):
        self.commit_id = commit_id
        self.commit_msg = commit_msg
        self.source_files = source_files
        self.test_files = test_files

    def construct_prompt(self):
        self.rank_source_files()
        ranked_files = [file for file in self.source_files
                        if self.__contains_class(file.source_ast.body)] + self.source_files
        for file in ranked_files[:TOP_FILES]:
            yield Prompt(self.__get_limited_tokens(file.source), self.commit_msg)

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

    def __contains_class(self, ast_body):
        lowered_message = self.commit_msg.lower()
        for element in ast_body:
            if isinstance(element, ClassDef) and element.name.lower() in lowered_message:
                return True
        return False

    def __get_limited_tokens(self, file_source):
        tokens = re.split(r'\s+', file_source)
        if len(tokens) >= MAX_ALLOWED_TOKENS:
            file_source = " ".join([self.__remove_comments(token) for token in tokens])
        return file_source

    @staticmethod
    def __remove_comments(token):
        return "".join(re.split(r"#.+\n", token))[:MAX_ALLOWED_TOKENS]

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
        string += f"{[file.filename for file in self.source_files]}\n"
        string += f"{[file.filename for file in self.test_files]}\n"
        return string
