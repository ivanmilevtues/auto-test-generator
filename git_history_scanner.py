import ast

from pydriller import Repository, ModificationType


class GitHistoryDataSetParser:

    def __init__(self, repository_path: str):
        self.git_repo = Repository(repository_path)

    def get_parsed_data(self):
        commits_data = []
        for commit in self.git_repo.traverse_commits():
            sources = self._get_edited_files_source(commit)
            commits_data.append(CommitData(commit.msg, [ast.parse(source) for source in sources]))
        return commits_data

    @staticmethod
    def _get_edited_files_source(commit) -> [str]:
        print([file.filename for file in commit.modified_files])
        py_files = [file for file in commit.modified_files
                    if file.filename.endswith(".py") and file.change_type != ModificationType.DELETE]
        return [py_file.source_code for py_file in py_files]


class CommitData:
    def __init__(self, commit_msg, file_asts):
        self.commit_msg = commit_msg
        self.file_asts = file_asts

    def __str__(self):
        string = f"{self.commit_msg}: \n"
        string += "\n".join([ast.dump(file_ast) for file_ast in self.file_asts])
        return string


if __name__ == "__main__":
    for p in GitHistoryDataSetParser("./").get_parsed_data():
        print(p)
