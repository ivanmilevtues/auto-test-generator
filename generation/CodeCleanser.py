import os
import re
import uuid

from generation.ImportResolver import ImportResolver
from history_scanner.Prompt import Prompt
from util.subprocess_utils import try_run


class CodeCleanser:
    def __init__(self, repo_dir: str, environment_command: str, import_resolver: ImportResolver):
        self.repo_dir = repo_dir
        self.environment_command = environment_command
        self.import_crawler = import_resolver
        self.name_error_re = re.compile(r"NameError:\sname '(\w+)' is not defined")

    def cleanse_test(self, test_code: str, prompt: Prompt):
        max_depth = 5
        try_run(self.environment_command, cwd=self.repo_dir)
        file_path = self.write_code(test_code, prompt)
        imports = self.missed_imports(file_path)
        while len(imports) != 0 and max_depth != 0:
            file_path = self.write_code(test_code, prompt, file_path, '\n'.join(imports))
            imports = self.missed_imports(file_path)
        with open(file_path, 'r') as f:
            source = '\n'.join(f.readlines())

        os.remove(file_path)

        return source

    def write_code(self, test_code, prompt, path=None, imports=''):
        source_code = f'''
{imports}
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
