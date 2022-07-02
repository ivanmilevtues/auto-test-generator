# import uuid
# from pathlib import Path
#
# from generation.CodeCleanser import CodeCleanser
# from generation.Compilable import Compilable
# from generation.GeneratedTestSaver import GeneratedTestSaver
# from generation.Generator import Generator
# from generation.ImportResolver import ImportResolver
# from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser

import os

#
# def generate_test(branch):
#     path = Path('./')
#     setup_command = ''
#     parser = GitHistoryDataSetParser('./', branch=f'origin/{branch}', only_last_commit=True)
#     data = parser.get_parsed_data()
#
#     generator = Generator(CodeCleanser(str(path.absolute()), setup_command, ImportResolver(str(path)), Compilable()))
#
#     for commit in data:
#         saver = GeneratedTestSaver(str(path.absolute()), commit.commit_id, main_branch='master',
#                                    directory_for_generation=f'generated_tests_for_{commit.commit_id}')
#         for prompt in commit.construct_prompt():
#             try:
#                 tests = generator.generate(prompt)
#                 for test in tests:
#                     saver.save_test_file(test, f'{uuid.uuid4()}')
#             except Exception as e:
#                 print(f"Tests for {prompt} not saved", e)
from git import GitCommandError
import subprocess

if __name__ == "__main__":
    branch_name = 'actions-configuration' #os.getenv('GITHUB_HEAD_REF')
    print(branch_name)
    print(os.getenv('OPENAI_API_KEY'))
    from pydriller import Repository

    repo = Repository('./',
                      only_in_branch=branch_name,
                      only_modifications_with_file_types=[".py"],
                      include_deleted_files=False,
                      order='reverse')
    try:
        for commit in repo.traverse_commits():
            print(commit.hash, commit.msg, commit.in_main_branch)
    except GitCommandError as e:
        print('Command', e.command)
        print('Stdout', e.stdout)
        print('Stderr', e.stderr)
        print('Status', e.status)
        print('Args', e.args)
        res = subprocess.run(' '.join(e.command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        print('RESULT: ', res.stdout.decode())

    # with open('test_code.py', 'w') as f:
    #     f.write('print("this is test")')
    # generate_test(branch_name)
