import ast

from pydriller import Repository, ModificationType
from history_scanner.CommitData import CommitData


class GitHistoryDataSetParser:

    def __init__(self, repository_path: str):
        self.git_repo = Repository(repository_path, only_in_branch="main")

    def get_parsed_data(self):
        commits_data = []
        i = 0
        for commit in self.git_repo.traverse_commits():
            sources = self.__get_edited_files_source(commit)
            i += 1
            if sources:
                commits_data.append(CommitData(commit.msg, self.__try_parse(sources)))
                print(f"Parsed for: {i} commit")
            else:
                print(f"Skip for: {i} commit")
        return commits_data

    # def process_commit(self, commit) -> CommitData:
    #     sources = self.__get_edited_files_source(commit)
    #     return CommitData(commit.msg, self.__try_parse(sources))

    @staticmethod
    def __try_parse(sources):
        res = []
        for source in sources:
            try:
                res.append(ast.parse(source))
            except:
                print(f"Fail for: {source}")
                continue
        return res

    def __get_edited_files_source(self, commit) -> [str]:
        if not self.__has_test_additions(commit):
            return []
        py_files = [file for file in commit.modified_files
                    if file.filename.endswith(".py") and file.change_type != ModificationType.DELETE]
        return [py_file.source_code for py_file in py_files]

    @staticmethod
    def __has_test_additions(commit) -> bool:
        paths = [file.new_path for file in commit.modified_files if file.change_type != ModificationType.DELETE]
        return any([("tests/" in path or "tests\\" in path)
                    for path in paths])


if __name__ == "__main__":
    parsed_data = GitHistoryDataSetParser("../test_folder/flask").get_parsed_data()
    print(parsed_data)
    print(f"{len(parsed_data)}")
