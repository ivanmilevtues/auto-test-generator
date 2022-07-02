import uuid
from pathlib import Path
import os

from generation.CodeCleanser import CodeCleanser
from generation.Compilable import Compilable
from generation.GeneratedTestSaver import GeneratedTestSaver
from generation.Generator import Generator
from generation.ImportResolver import ImportResolver
from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser


def generate_test(branch):
    path = Path('./')
    setup_command = ''
    parser = GitHistoryDataSetParser(str(path.absolute()), branch=f'{branch}', only_last_commit=True)
    data = parser.get_parsed_data()

    generator = Generator(CodeCleanser(str(path.absolute()), setup_command, ImportResolver(str(path)), Compilable()))

    for commit in data:
        saver = GeneratedTestSaver(str(path.absolute()), commit.commit_id, main_branch='master',
                                   directory_for_generation=f'generated_tests_for_{commit.commit_id}')
        for prompt in commit.construct_prompt():
            try:
                tests = generator.generate(prompt)
                for test in tests:
                    saver.save_test_file(test, f'{uuid.uuid4()}')
            except Exception as e:
                print(f"Tests for {prompt} not saved", e)


if __name__ == "__main__":
    branch_name = os.getenv("GITHUB_HEAD_REF")
    generate_test(branch_name)
