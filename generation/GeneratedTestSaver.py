import subprocess
import os


class GeneratedTestSaver:
    BRANCH_ID = 0

    def __init__(self, repository_path: str, commit_id: str, directory_for_generation: str = 'generated_tests',
                 main_branch="main"):
        self.repository_path = repository_path
        self.commit_id = commit_id
        self.generated_code_directory = directory_for_generation
        self.main_branch = main_branch

    def init_module(self):
        init_module = f"{self.repository_path}/{self.generated_code_directory}/__init__.py"
        os.makedirs(os.path.dirname(init_module), exist_ok=True)
        open(init_module, "a").close()

    def save_test_file(self, test_code, filename):
        path = f"{self.repository_path}/{self.generated_code_directory}/test_{filename}.py"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print(f"Saving tests to '{path}'.")
        with open(path, "w") as f:
            f.write(test_code)
        return path

    def goto_commit(self):
        subprocess.run(["git", "checkout", "-b", f"{self.generated_code_directory}_{GeneratedTestSaver.BRANCH_ID}",
                        self.commit_id],
                       check=True, stdout=subprocess.PIPE, cwd=self.repository_path)
        self.init_module()

    def commit_files(self):
        subprocess.run(["git", "add", f"{self.generated_code_directory}/*"],
                       check=True, stdout=subprocess.PIPE, cwd=self.repository_path)
        subprocess.run(["git", "commit", "-m", '"Committing generated tests."', "--no-verify", "-n"],
                       check=True, stdout=subprocess.PIPE, cwd=self.repository_path)
        GeneratedTestSaver.BRANCH_ID += 1

    def clean_state(self):
        # If the state is very bad run the following command:
        # git branch | grep -v "main" | xargs git branch -D
        # This will delete all branches without the one for the parameter of -v
        subprocess.run(["git", "checkout", self.main_branch], check=True, stdout=subprocess.PIPE,
                       cwd=self.repository_path)

    @staticmethod
    def reset_branch_id():
        GeneratedTestSaver.BRANCH_ID = 0
