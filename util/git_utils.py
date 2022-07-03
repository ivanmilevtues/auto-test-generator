import subprocess


def delete_branches(prefix, number_of_branches, base_dir):
    subprocess.run(["git", "checkout", f"main"],
                   stdout=subprocess.PIPE, cwd=base_dir)
    for i in range(number_of_branches):
        subprocess.run(["git", "branch", "--delete", "--force", f"{prefix}{i}"],
                       stdout=subprocess.PIPE, cwd=base_dir)


if __name__ == "__main__":
    delete_branches("gen_tests_evaluation_", 6,
                    'C:\\Users\\Ivan\\PycharmProjects\\auto-test-generator\\dataset_repos\\fake-calculator')
