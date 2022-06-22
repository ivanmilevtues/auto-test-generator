import pickle
from pydriller import Repository, ModificationType
from history_scanner.CommitData import CommitData
from history_scanner.commit_file import CommitFile


class GitHistoryDataSetParser:

    def __init__(self, repository_path="./", branch="main"):
        self.git_repo = Repository(repository_path, only_in_branch=branch, only_modifications_with_file_types=[".py"],
                                   include_deleted_files=False)
        self.parsed_data = []

    def parse_data(self):
        self.parsed_data = list(filter(None, [self.process_commit(commit)
                                              for commit in self.git_repo.traverse_commits()]))

    def get_parsed_data(self):
        if not self.parsed_data:
            self.parsed_data = list(filter(None, [self.process_commit(commit)
                                                  for commit in self.git_repo.traverse_commits()]))
        return self.parsed_data

    def process_commit(self, commit) -> CommitData:
        py_files, test_files = self.__get_edited_files_source(commit)
        if len(py_files) > 0 and len(test_files) > 0:
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
                if self.__is_test_file(file):
                    parsed_file = CommitFile(file.filename, file.source_code)
                    if parsed_file.source_ast is not None:
                        test_files.append(parsed_file)
                elif self.__has_additions(file):
                    parsed_file = CommitFile(file.filename, file.source_code)
                    if parsed_file.source_ast is not None:
                        py_files.append(parsed_file)

        return py_files, test_files

    def __has_test_additions(self, commit) -> bool:
        return len([self.__has_additions(file) for file in commit.modified_files]) != 0

    @staticmethod
    def __has_additions(modified_file) -> bool:
        return len(modified_file.methods) > len(modified_file.methods_before)

    @staticmethod
    def __is_test_file(modified_file):
        return modified_file.new_path is not None and "test" in modified_file.new_path and \
               "__init__" not in modified_file.new_path

    def save_parsed_data(self, file_path):
        if not self.parsed_data:
            raise Exception("Parsed data is not initialized. Please run parse_data before saving.")
        with open(file_path, "wb") as f:
            pickle.dump(self.parsed_data, f)

    def load_data(self, file_path):
        with open(file_path, "rb") as f:
            self.parsed_data = pickle.load(f)
        return self.parsed_data


if __name__ == "__main__":
    repo_parser = GitHistoryDataSetParser("../dataset_repos/flask")
    repo_parser.parse_data()
    repo_parser.save_parsed_data("test_save.dat")
    print(len(repo_parser.get_parsed_data()))
