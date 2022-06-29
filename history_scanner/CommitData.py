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
        ranked_files = self.rank_source_files()
        for file in ranked_files[:TOP_FILES]:
            yield Prompt(file, self.commit_msg)

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

    @staticmethod
    def __remove_comments(token):
        return "".join(re.split(r"#.+\n", token))[:MAX_ALLOWED_TOKENS]

    def __source_str(self):
        sources = ""
        for file in self.source_files:
            if len(sources.split(r'\s')) + len(file.source.split(r'\s')) < MAX_ALLOWED_TOKENS:
                sources += '\n' + file.source
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

    def __repr__(self):
        return self.__str__()
