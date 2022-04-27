import re
import shlex
import subprocess

def get_commit_log():
    output = subprocess.check_output(shlex.split('git log --pretty=%s --color'),
        stderr=subprocess.STDOUT)
    output = output.decode('ascii')
    output = output.split('\n')
    return output


def strip_commits(commits):
    output = []
    for line in commits:
        if re.findall(r"(feat|fix|refactor|test|cli)", line):
            output.append(line)
    return output

def overwrite_changelog(commits):
    print("Going to write the following commits: \n{}".format(commits))
    with open("./CHANGELOG.md", "w+") as f:
        f.write("# CHANGELOG \n\n ## Features:\n\n")
        for feat in commits:
            if re.findall(r"^feat", feat):
                f.write("* {}\n".format(feat))
        f.write("\n## Bugs:\n\n")
        for fix in commits:
            if re.findall(r"^fix", fix):
                f.write("* {}\n".format(fix))
        f.write("\n## Others:")
        for other in commits:
            if re.findall(r"^(refactor|test|cli)", other):
                f.write("* {}\n".format(other))
        f.write("\n\n\n> Generated with Github actions")

def main():
    commits = get_commit_log()
    commits = strip_commits(commits)
    overwrite_changelog(commits)

if __name__ == "__main__":
    main()