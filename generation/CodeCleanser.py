import os
import re
import uuid

from generation.Compilable import Compilable
from generation.ImportResolver import ImportResolver
from history_scanner.Prompt import Prompt
from util.subprocess_utils import try_run
from util.decorators import time_measuring_decorator


class CodeCleanser:
    def __init__(self, repo_dir: str, environment_command: str, import_resolver: ImportResolver,
                 make_compilable: Compilable):
        self.repo_dir = repo_dir
        self.environment_command = environment_command
        self.import_crawler = import_resolver
        self.name_error_re = re.compile(r"NameError:\sname '(\w+)' is not defined")
        self.compilable = make_compilable

    @time_measuring_decorator
    def cleanse_test(self, test_code: str):
        max_depth = 5
        test_code = f'def test_{test_code}'
        file_path = self.write_code(test_code)

        new_lines, is_edited = self.unclosed_quotes(file_path)
        if is_edited:
            file_path = self.write_code(self.__join_lines(new_lines), path=file_path)

        command = f'{self.environment_command} & python {file_path}' \
            if self.environment_command != '' \
            else f'python {file_path}'

        if try_run(command, cwd=self.repo_dir, return_exit_code=True) != 0:
            with open(file_path, 'r') as f:
                source = f.read()
            fix_source = self.compilable.fix_test(source)
            if len(fix_source) >= len(source) * 0.8:
                source = fix_source
                self.write_code(source, file_path)

        with open(file_path, 'r') as f:
            source = f.read()

        lines_to_import, is_edited = self.missed_imports(file_path)
        while is_edited and max_depth != 0:
            file_path = self.write_code(source, file_path, self.__join_lines(lines_to_import))
            new_lines, is_edited = self.missed_imports(file_path)
            lines_to_import += new_lines
            max_depth -= 1

        with open(file_path, 'r') as f:
            source = f.read()

        os.remove(file_path)
        if os.path.exists(file_path):
            print(f'{file_path} exists.')

        return source

    def write_code(self, code, path=None, prepend_code: str = ''):
        if path is None:
            path = f"{self.repo_dir}/{uuid.uuid4()}.py"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if prepend_code:
            with open(path, 'r') as f:
                code = prepend_code + f.read()
        with open(path, 'w') as f:
            f.write(code)
        return path

    @time_measuring_decorator
    def missed_imports(self, file_path):
        stdout = try_run(f"pytest {file_path}", cwd=self.repo_dir)
        missing_imports = set(self.name_error_re.findall(stdout))
        return self.import_crawler.find_imports(missing_imports)

    @time_measuring_decorator
    def unclosed_quotes(self, file):
        stdout = try_run(f"python {file}", cwd=self.repo_dir)
        edits = False
        lines = []
        if 'SyntaxError: EOF while scanning' in stdout:
            with open(file, 'r') as f:
                lines = f.readlines()
            in_comment = False
            for indx in range(len(lines)):
                line = lines[indx]
                if in_comment and re.match(r'(\s+|)def\s\w+\(', line):
                    lines[indx] = in_comment + '\n' + line
                    in_comment = False
                    edits = True
                elif '"""' in line:
                    in_comment = '"""' if not in_comment else False
                elif "'''" in line:
                    in_comment = "'''" if not in_comment else False
            if in_comment:
                lines.append(in_comment)
        return lines, edits

    @staticmethod
    def __join_lines(lines):
        return '\n'.join([line for line in lines if line != '\n'])
