from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser
def test_end_to_end():
    repo_parser = GitHistoryDataSetParser("../dataset_repos/flask")
    assert len(repo_parser.get_parsed_data()) == 0

    repo_parser.parse_data()

    assert len(repo_parser.get_parsed_data()) > 0

    parsed = repo_parser.load_data("../dataset_repos/data/flask-reference-commits.dat")
    
    assert len(parsed) > 0
# Generate asserts
import pytest
"""
End to end third test.
The tests are testing: class GitHistoryDataSetParser
"""
def test_end_to_end():
    repo_parser = GitHistoryDataSetParser("../dataset_repos/flask", branch="master")

    parsed = repo_parser.load_data("../dataset_repos/data/flask-reference-commits.dat")

    assert len(parsed) > 0
 
