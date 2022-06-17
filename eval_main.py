from pathlib import Path
import uuid

from generation.Model import Model
from generation.GeneratedTestSaver import GeneratedTestSaver
from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser
from model.message_preparation import PromptsBuilder

model = Model()


def main():
    parser = GitHistoryDataSetParser("dataset_repos/flask")
    data = parser.load_data("history_scanner/test_save.dat")
    print(f"Generating tests for {len(data)} commits")
    messages = PromptsBuilder(data, train=1)

    for commit_id, prompts in messages.create_prompt():
        saver = GeneratedTestSaver(str(Path("dataset_repos/flask").absolute()), commit_id)
        saver.goto_commit()
        for prompt in prompts:
            try:
                test = model.generate_test(str(prompt))
                saver.save_test_file(test, f'test_{uuid.uuid4()}')
            except Exception as e:
                print(e)
        saver.commit_files()
        saver.clean_state()


if __name__ == "__main__":
    main()
