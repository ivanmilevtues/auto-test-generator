def test_has_additions():
    repo = GitRepository("./test_repos/httpie")
    commits = list(repo.get_commits())

    assert not repo._GitHistoryDataSetParser__has_test_additions(commits[0])
    assert not repo._GitHistoryDataSetParser__has_test_additions(commits[1])
    assert not repo._GitHistoryDataSetParser__has_test_additions(commits[2])
    assert not repo._GitHistoryDataSetParser__has_test_additions(commits[3])
    assert   repo._GitHistoryDataSetParser__has_test_additions(commits[4])  
# Generate asserts
    test_file = """
from pydriller import Repository, Commit, ModificationType


class GitRepository:
    def __init__(self, repository_path):
        self.git_repo = Repository(repository_path)

    def get_commits(self): return self.git_repo.traverse_commits()

    def _GitHistoryDataSetParser__has_test_additions(self, commit) -> bool: 
        for file in commit.modified_files: 
            if file.filename is not None and "test" in file.filename \  
                    and len(file.methods) > len(file.methods_before):  return True"""