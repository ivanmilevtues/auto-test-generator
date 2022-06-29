import subprocess
from pathlib import Path
import re

import pandas as pd
from util.subprocess_utils import try_run


class RuntimeEvaluator:
    def __init__(self, repository, setup_command):
        self.repository = repository
        self.setup_command = setup_command
        self.df = pd.DataFrame(
            {
                "Filename": [],
                "Python compilation": [],
                "Pytest fails": [],
                "Pytest passes": [],
                "Pytest warnings": [],
                "Pytest errors": []
            })
        self.failed_re = re.compile(r'=.+((?P<number>\d)+ failed)')
        self.passed_re = re.compile(r'=.+((?P<number>\d+) passed)')
        self.warning_re = re.compile(r'=.+((?P<number>\d+) warning)')
        self.error_re = re.compile(r'=.+((?P<number>\d+) error)')

    def evaluate(self, file):
        self.run_subprocess(f'{self.setup_command}')
        compile_result = self.run_subprocess(f'python {file}')
        test_result = self.run_subprocess(f'{self.setup_command} & pytest {file}')
        fails, passes, warnings, errors = self.parse_result(test_result)
        print("Runtime eval:", compile_result, fails, passes, warnings, errors)
        self.df = self.df.append(
            {
                "Filename": str(file),
                "Python compilation": str(compile_result),
                "Pytest fails": fails,
                "Pytest passes": passes,
                "Pytest warnings": warnings,
                "Pytest errors": errors
            },
            ignore_index=True)

    def parse_result(self, out):
        return self.__get_number(self.failed_re, out), self.__get_number(self.passed_re, out), \
               self.__get_number(self.warning_re, out), self.__get_number(self.error_re, out)

    def run_subprocess(self, command):
        try:
            return try_run(command, cwd=self.repository, throw=True)
        except subprocess.CalledProcessError as e:
            print("Failed to run command: ", e)
        except Exception as e:
            print("Generic exception while runtime evaluation: ", e)
        if '&' in command:
            print("Retrying evaluation")
            return self.run_subprocess(command.split('&')[-1].strip())
        return 0

    def export(self, filename="compiler_evaluation.csv"):
        self.df.to_csv(filename)

    @staticmethod
    def __get_number(regex, out):
        matches = regex.search(out)
        if matches:
            return str(matches.groups('number')[1])
        return '0'


if __name__ == '__main__':
    evaluator = RuntimeEvaluator("C:\\Users\\Ivan\\PycharmProjects\\auto-test-generator\\dataset_repos\\flask",
                                 "env\\Scripts\\activate")
    evaluator.evaluate(
        Path('C:\\Users\\Ivan\\PycharmProjects\\auto-test-generator\\dataset_repos\\flask\\tests\\test_views.py'))
    print(evaluator.df)
    evaluator.export()
