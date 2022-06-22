import subprocess
from pathlib import Path

import pandas as pd


class CompilerEvaluator:
    def __init__(self, repository, setup_command):
        self.repository = repository
        self.setup_command = setup_command
        self.df = pd.DataFrame({"Filename": [], "Python compilation": [], "Pytest run": []})

    def evaluate(self, file):
        compile_result = self.run_subprocess(f'{self.setup_command} & python {file}')
        test_result = self.run_subprocess(f'{self.setup_command} & pytest {file}')
        self.df = self.df.append(
            {
                "Filename": str(file),
                "Python compilation": str(compile_result),
                "Pytest run": str(test_result)
            },
            ignore_index=True)

    def run_subprocess(self, command):
        try:
            return subprocess.run(command, check=True, stdout=subprocess.PIPE, shell=True, cwd=self.repository).stdout
        except subprocess.CalledProcessError as e:
            print("Failed to run command: ", e)
        except Exception as e:
            print("Generic exception while compilation evaluation: ", e)
        if '&' in command:
            print("Retrying evaluation")
            return self.run_subprocess(command.split('&')[-1].strip())
        return 0

    def export(self, filename="compiler_evaluation.csv"):
        self.df.to_csv(filename)


if __name__ == '__main__':
    eval = CompilerEvaluator("C:\\Users\\Ivan\\PycharmProjects\\auto-test-generator\\dataset_repos\\flask",
                             "env\\Scripts\\activate")
    eval.evaluate(
        Path('C:\\Users\\Ivan\\PycharmProjects\\auto-test-generator\\dataset_repos\\flask\\tests\\test_views.py'))
    print(eval.df)
    eval.export()
