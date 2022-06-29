from pathlib import Path
import uuid

from eval.RuntimeEvaluator import RuntimeEvaluator
from generation.CodeCleanser import CodeCleanser
from generation.GeneratedTestSaver import GeneratedTestSaver
from generation.Generator import Generator
from generation.ImportResolver import ImportResolver
from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser
from eval.BLEUEvaluator import BLEUEvaluator


def main():
    path = Path("dataset_repos/httpie")
    setup_command = "python -m venv --prompt httpie venv " + \
                    "& venv\\Scripts\\activate " + \
                    "& python -m pip install --upgrade -e .[dev]"
    bleu = BLEUEvaluator()
    compiler = RuntimeEvaluator(path, setup_command)
    parser = GitHistoryDataSetParser(str(path.absolute()), branch="master")

    data = parser.load_data("dataset_repos/data/httpie_reference_commits.dat")
    print(f"Generating tests for {len(data)} commits")

    generator = Generator(CodeCleanser(str(path.absolute()), setup_command, ImportResolver(str(path))))

    for commit in data:
        saver = GeneratedTestSaver(str(path.absolute()),
                                   commit.commit_id, main_branch="master",
                                   directory_for_generation="gen_tests_imports")
        saver.goto_commit()
        for prompt in commit.construct_prompt():
            try:
                tests = generator.generate(prompt)
                save_and_eval(tests, saver, bleu, compiler, commit)
            except Exception as e:
                print(f"Tests for {prompt} not saved", e)
        saver.commit_files()
        saver.clean_state()
    bleu.export('blue_httpie_imports.csv')
    compiler.export('compile_httpie_imports.csv')


def save_and_eval(tests, saver, bleu, compiler, commit):
    for test in tests:
        file_path = saver.save_test_file(test, f'test_{uuid.uuid4()}')
        bleu.evaluate(test, [f.source for f in commit.test_files], commit.commit_id)
        compiler.evaluate(file_path)


if __name__ == "__main__":
    main()
