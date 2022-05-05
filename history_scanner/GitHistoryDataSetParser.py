import ast
import pickle
from pydriller import Repository, ModificationType
from history_scanner.CommitData import CommitData


class GitHistoryDataSetParser:

    def __init__(self, repository_path: str):
        self.git_repo = Repository(repository_path, only_in_branch="main", only_modifications_with_file_types=[".py"],
                                   include_deleted_files=False, num_workers=10)
        self.parsed_data = []

    def parse_data(self):
        self.parsed_data = list(filter(None, [self.process_commit(commit) for commit in self.git_repo.traverse_commits()]))

    def get_parsed_data(self):
        if not self.parsed_data:
            self.parsed_data = list(filter(None, [self.process_commit(commit) for commit in self.git_repo.traverse_commits()]))
        return self.parsed_data

    def process_commit(self, commit) -> CommitData:
        sources = self.__get_edited_files_source(commit)
        if sources:
            return CommitData(commit.msg, self.__try_parse(sources))

    @staticmethod
    def __try_parse(sources):
        res = []
        for source in sources:
            try:
                res.append(ast.parse(source))
            except:
                continue
        return res

    def __get_edited_files_source(self, commit) -> [str]:
        if not self.__has_test_additions(commit):
            return []
        py_files = [file for file in commit.modified_files
                    if file.filename.endswith(".py") and file.change_type != ModificationType.DELETE]
        return [py_file.source_code for py_file in py_files]

    def __has_test_additions(self, commit) -> bool:
        return len([self.__modified_file_is_test(file) for file in commit.modified_files]) != 0

    @staticmethod
    def __modified_file_is_test(modified_file) -> bool:
        if modified_file.new_path is None or \
                ("tests/" not in modified_file.new_path and "tests\\" not in modified_file.new_path):
            return False
        return len(modified_file.methods) > len(modified_file.methods_before)

    def save_parsed_data(self, file_path):
        if not self.parsed_data:
            raise Exception("Parsed data is not initialized. Please run parse_data before saving.")
        with open(file_path, "wb") as f:
            pickle.dump(self.parsed_data, f)

    def load_data(self, file_path):
        with open(file_path, "rb") as f:
            self.parsed_data = pickle.load(f)


if __name__ == "__main__":
    repo_parser = GitHistoryDataSetParser("../test_folder/flask")
    repo_parser.load_data("test_save.dat")
    print(len(repo_parser.get_parsed_data()))
