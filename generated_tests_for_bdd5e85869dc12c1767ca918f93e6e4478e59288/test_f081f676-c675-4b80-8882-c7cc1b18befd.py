from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser
def test_is_expr_related_to_code():
    repo = GitHistoryDataSetParser("../dataset_repos/flask", branch="main")
    parsed_data = repo.load_data("../dataset_repos/data/flask_reference_commits.dat")

    
# Generate asserts for the test
    for commit in parsed_data:
        for file in commit.py_files:

            assert isinstance(file, CommitFile)

            if len(file.related_source) > 0: 
                token = list(file.related_source)[0]
                expr = file.related_source[token][0] 