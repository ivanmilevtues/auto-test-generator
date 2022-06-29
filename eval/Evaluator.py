import os
import subprocess
from pathlib import Path

from eval.BLEUEvaluator import BLEUEvaluator
from eval.RuntimeEvaluator import RuntimeEvaluator
from history_scanner.CommitData import CommitData
from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser


class Evaluator:
    def __init__(self, repository: Path, branch_prefix: str, setup_command: str, number_of_commits: int,
                 commits: [CommitData]):
        self.compiler_eval = RuntimeEvaluator(repository, setup_command)
        self.bleu_eval = BLEUEvaluator()
        self.repo = repository
        self.number_of_commits = number_of_commits
        self.branch_prefix = branch_prefix
        self.commits = commits

    def evaluate(self, bleu_export_filename: str, compile_export_filename: str):
        try:
            for commit_number in range(self.number_of_commits):
                self.checkout(commit_number)
                repo_path = self.repo.absolute()
                generated_files = [f'{repo_path}/generated_tests/{file}' for file in
                                   os.listdir(f'{repo_path}/generated_tests')
                                   if file.startswith('test_')]

                commit = self.commits[commit_number]
                for file in generated_files:
                    self.evaluate_bleu(file, [f.source for f in commit.test_files], commit.commit_id)
                    self.evaluate_compile(file)
        finally:
            self.bleu_eval.export(bleu_export_filename)
            self.compiler_eval.export(compile_export_filename)

    def checkout(self, commit_number, retry=2):
        try:
            subprocess.run(f'git stash -a & git checkout {self.branch_prefix}_{commit_number}', check=True, shell=True,
                           stdout=subprocess.PIPE, cwd=self.repo)
        except subprocess.CalledProcessError as e:
            print(e)
            if retry >= 0:
                print("Cooldown for one minute")
                time.sleep(60)
                self.checkout(commit_number, retry - 1)
            else:
                print("Failed after 3 retries.")

    def evaluate_bleu(self, file, reference_sources, commit_hash):
        with open(file, 'r') as f:
            code = "\n".join(f.readlines())
            self.bleu_eval.evaluate(code, reference_sources, commit_hash)

    def evaluate_compile(self, file):
        self.compiler_eval.evaluate(file)


if __name__ == '__main__':
    import time

    start_time = time.perf_counter()

    parser = GitHistoryDataSetParser("../dataset_repos/httpie", branch="master")
    commits = parser.load_data("../dataset_repos/data/httpie_commits.dat")
    evaluator = Evaluator(Path("../dataset_repos/httpie"), "generated_tests",
                          "python -m venv --prompt httpie venv " +
                          "& venv\\Scripts\\activate " +
                          "& python -m pip install --upgrade -e .[dev]",
                          103, commits)
    evaluator.evaluate("bleu_httpie_basic.csv", "compile_httpie_basic.csv")
    end_time = time.perf_counter()
    print("Time to evaluate")
    print(end_time - start_time, "seconds")

    # start_time = time.perf_counter()
    #
    # parser = GitHistoryDataSetParser("../dataset_repos/flask", branch="main")
    # commits = parser.load_data("../dataset_repos/data/flask_commits.dat")
    # evaluator = Evaluator(Path("../dataset_repos/flask"), "generated_tests",
    #                       "python -m venv env " +
    #                       "& env\\Scripts\\activate " +
    #                       "& pip install -r requirements/dev.txt & pip install -e",
    #                       72, commits)
    # evaluator.evaluate("bleu_flask_basic.csv", "compile_flask_basic.csv")
    #
    # end_time = time.perf_counter()
    # print("Time to evaluate")
    # print(end_time - start_time, "seconds")
