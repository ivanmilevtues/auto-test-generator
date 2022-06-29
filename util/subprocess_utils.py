import subprocess


def try_run(command, cwd, throw=False, depth=5):
    try:
        return subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, shell=True).stdout.decode()
    except Exception as e:
        print("Error while running subprocess:", e)
        if depth == 0 and throw:
            raise e
        if depth != 0:
            return try_run('&'.join(command.split('&')[1:]), cwd, throw, depth - 1)
        return ''
