import ast
import pickle
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

from pydriller import Repository, ModificationType
from history_scanner.CommitData import CommitData
from history_scanner.commit_file import CommitFile


class GitHistoryDataSetParser:
    def __init__(self, repository_path="./", branch="main", only_last_commit=False):
        self.commit_msg_tokens = []
        self.parsed_data = []
        self.stemmer = SnowballStemmer(language='english')
        self.only_last_commit = only_last_commit
        if only_last_commit:
            self.git_repo = Repository(repository_path, only_in_branch=branch,
                                       only_modifications_with_file_types=[".py"],
                                       include_deleted_files=False,
                                       order='reverse')
        else:
            self.git_repo = Repository(repository_path, only_in_branch=branch,
                                       only_modifications_with_file_types=[".py"],
                                       include_deleted_files=False)

    def parse_data(self):
        if self.only_last_commit:
            commits = [next(self.git_repo.traverse_commits())]
            self.parsed_data = list(filter(None, [self.process_commit(commit)
                                                  for commit in commits]))
        else:
            self.parsed_data = list(filter(None, [self.process_commit(commit)
                                                  for commit in self.git_repo.traverse_commits()]))

    def get_parsed_data(self):
        if not self.parsed_data:
            self.parse_data()
        return self.parsed_data

    def process_commit(self, commit) -> CommitData:
        print("Processing commit", commit.msg)
        commit_msg_tokens = word_tokenize(commit.msg)
        self.commit_msg_tokens = [self.stemmer.stem(w) for w in commit_msg_tokens]

        py_files, test_files = self.__get_edited_files_source(commit)
        if len(py_files) > 0 and (self.only_last_commit or len(test_files) > 0):
            commit_data = CommitData(commit.hash, commit.msg, py_files, test_files)
            print(commit_data)
            return commit_data

    def __get_edited_files_source(self, commit) -> [str]:
        if not self.__has_test_additions(commit):
            return []
        py_files = []
        test_files = []

        for file in commit.modified_files:
            if file.filename.endswith(".py") and file.change_type != ModificationType.DELETE:
                parsed_file = CommitFile(file.filename, file.source_code)
                self.__populate_words_usages(parsed_file, parsed_file.source_ast)
                if self.__is_test_file(file):
                    if parsed_file.source_ast is not None:
                        test_files.append(parsed_file)
                elif self.__has_additions(file):
                    if parsed_file.source_ast is not None:
                        py_files.append(parsed_file)
                elif len(parsed_file.related_source) > 0:
                    py_files.append(parsed_file)

        return py_files, test_files

    def save_parsed_data(self, file_path):
        if not self.parsed_data:
            raise Exception("Parsed data is not initialized. Please run parse_data before saving.")
        with open(file_path, "wb") as f:
            pickle.dump(self.parsed_data, f)

    def load_data(self, file_path):
        with open(file_path, "rb") as f:
            self.parsed_data = pickle.load(f)
        return self.parsed_data

    def __has_test_additions(self, commit) -> bool:
        return len([self.__has_additions(file) for file in commit.modified_files]) != 0

    @staticmethod
    def __has_additions(modified_file) -> bool:
        return len(modified_file.methods) > len(modified_file.methods_before)

    @staticmethod
    def __is_test_file(modified_file):
        return modified_file.new_path is not None and "test" in modified_file.new_path and \
               "__init__" not in modified_file.new_path

    def __populate_words_usages(self, parsed_file, ast_parse):
        if ast_parse is None:
            return

        for expr in ast_parse.body:
            if isinstance(expr, ast.ClassDef):
                token, expr = self.__is_expr_related_to_code(expr)
                if token and expr:
                    parsed_file.relate_source(token, expr)
                self.__populate_words_usages(parsed_file, expr)
            elif isinstance(expr, ast.FunctionDef):
                token, expr = self.__is_expr_related_to_code(expr)
                if token and expr:
                    parsed_file.relate_source(token, expr)

    def __is_expr_related_to_code(self, expr):
        for token in self.commit_msg_tokens:
            if token in expr.name:
                return token, expr
        return None, None


if __name__ == "__main__":
    repo_parser = GitHistoryDataSetParser("../dataset_repos/flask")
    repo_parser.parse_data()
    repo_parser.save_parsed_data("../dataset_repos/data/flask_reference_commits.dat")
    print("flask", len(repo_parser.get_parsed_data()))

    repo_parser = GitHistoryDataSetParser("../dataset_repos/pydriller", branch="master")
    repo_parser.parse_data()
    repo_parser.save_parsed_data("../dataset_repos/data/pydriller_reference_commits.dat")
    print("pydriller", len(repo_parser.get_parsed_data()))

    repo_parser = GitHistoryDataSetParser("../dataset_repos/httpie", branch="master")
    repo_parser.parse_data()
    repo_parser.save_parsed_data("../dataset_repos/data/httpie_reference_commits.dat")
    print("httpie", len(repo_parser.get_parsed_data()))
