from functools import reduce
from ast import Import, ImportFrom
import pandas as pd

from history_scanner.CommitData import CommitData


class FineTuningGenerator:
    def __init__(self, commits: [CommitData]):
        self.prompts = None
        self.commits = commits

    def save(self, filename: str):
        if self.prompts is None:
            raise Exception("Prompt is not generated. Please run generate_prompt_lines before calling the save method.")
        self.prompts.to_json(filename, orient='records', lines=True)

    def generate_prompt_lines(self):
        prompts = [self.__generate_prompts(commit) for commit in self.commits]
        self.prompts = pd.DataFrame(reduce(list.__add__, prompts), columns=['prompt', 'completion'])
        return self.prompts

    def __generate_prompts(self, commit: CommitData):
        prompts = []
        for test_file in commit.test_files:
            related_source_files = self.__connected_source_files(commit.source_files, test_file)
            for source_file in related_source_files:
                prompts.append(self.__generate_prompt(commit.commit_msg, source_file, test_file))
        return prompts

    def __connected_source_files(self, source_files, test_file):
        related_files = []
        for definition in test_file.source_ast.body:
            if isinstance(definition, Import) or isinstance(definition, ImportFrom):
                for name in definition.names:
                    related_files += self.__is_referencing_file_from_project(source_files, name.name)
        return related_files

    @staticmethod
    def __generate_prompt(message, source_file, test_file):
        return (f'''Python3
{source_file.source}
"""
Generate tests which test: {message}
"""
''', ' ' + test_file.source)

    @staticmethod
    def __is_referencing_file_from_project(source_files, import_name):
        return [file for file in source_files if import_name in file.filename]


if __name__ == '__main__':
    from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser
    parser = GitHistoryDataSetParser("./")
    coms = parser.load_data("test_save.dat")
    fine_tuner = FineTuningGenerator(coms)
    fine_tuner.generate_prompt_lines()
    fine_tuner.save('first_test.jsonl')
