from pathlib import Path
import uuid

from eval.RuntimeEvaluator import RuntimeEvaluator
from generation.CodeCleanser import CodeCleanser
from generation.GeneratedTestSaver import GeneratedTestSaver
from generation.Generator import Generator
from generation.ImportResolver import ImportResolver
from generation.Compilable import Compilable
from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser
from eval.BLEUEvaluator import BLEUEvaluator
from util.decorators import time_measuring_decorator


@time_measuring_decorator
def main():
    path = Path("dataset_repos/fake-calculator")
    setup_command = "conda activate diploma"
    bleu = BLEUEvaluator()
    compiler = RuntimeEvaluator(path, setup_command)
    parser = GitHistoryDataSetParser(str(path.absolute()), branch="main")
    data = parser.get_parsed_data()
    # parser.save_parsed_data("dataset_repos/data/calc_reference_commits.dat")
    # data = parser.load_data("dataset_repos/data/calc_reference_commits.dat")

    print(f"Generating tests for {len(data)} commits")

    generator = Generator(CodeCleanser(str(path.absolute()), setup_command, ImportResolver(str(path)), Compilable()))

    for commit in data:
        saver = GeneratedTestSaver(str(path.absolute()),
                                   commit.commit_id, main_branch="main",
                                   directory_for_generation="gen_tests_evaluation")
        saver.goto_commit()
        for prompt in commit.construct_prompt():
            try:
                tests = generator.generate(prompt)
                save_and_eval(tests, saver, bleu, compiler, commit)
                compiler.evaluate_set("gen_tests_evaluation", commit.commit_id)
            except Exception as e:
                print(f"Tests for {prompt} not saved", e)
        saver.commit_files()
        saver.clean_state()
    bleu.export('blue_pydriller_import_fixes.csv')
    compiler.export('compile_pydriller_import_fixes.csv')


def save_and_eval(tests, saver, bleu, compiler, commit):
    for test in tests:
        file_path = saver.save_test_file(test, f'{uuid.uuid4()}')
        bleu.evaluate(test, [f.source for f in commit.test_files], commit.commit_id)
        compiler.evaluate(file_path)


if __name__ == "__main__":
    main()
