import os
import re
import uuid

from generation.Compilable import Compilable
from generation.ImportResolver import ImportResolver
from history_scanner.Prompt import Prompt
from util.subprocess_utils import try_run


class CodeCleanser:
    def __init__(self, repo_dir: str, environment_command: str, import_resolver: ImportResolver,
                 make_compilable: Compilable):
        self.repo_dir = repo_dir
        self.environment_command = environment_command
        self.import_crawler = import_resolver
        self.name_error_re = re.compile(r"NameError:\sname '(\w+)' is not defined")
        self.compilable = make_compilable

    def cleanse_test(self, test_code: str, prompt: Prompt):
        max_depth = 5
        try_run(self.environment_command, cwd=self.repo_dir)
        file_path = self.write_code(test_code, prompt)

        new_lines, is_edited = self.unclosed_quotes(file_path)
        if is_edited:
            file_path = self.write_code('\n'.join(new_lines), prompt, file_path, full_source=True)

        new_lines, is_edited = self.missed_imports(file_path)
        while is_edited and max_depth != 0:
            file_path = self.write_code(test_code, prompt, file_path, full_source=True)
            new_lines, is_edited = self.missed_imports(file_path)
            max_depth -= 1

        with open(file_path, 'r') as f:
            source = '\n'.join(f.readlines())

        if try_run(f"python {file_path}", cwd=self.repo_dir, return_exit_code=True) != 0:
            source = self.compilable.fix_test(source)

        os.remove(file_path)

        return source

    def write_code(self, test_code, prompt, path=None, full_source=False):
        source_code = test_code if full_source else f'''
import {prompt.test_lib}
def test_{test_code}'''

        if path is None:
            path = f"{self.repo_dir}/{uuid.uuid4()}.py"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(source_code)
        return path

    def missed_imports(self, file_path):
        stdout = try_run(f"pytest {file_path}", cwd=self.repo_dir)
        missing_imports = set(self.name_error_re.findall(stdout))
        return self.import_crawler.find_imports(missing_imports)

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
