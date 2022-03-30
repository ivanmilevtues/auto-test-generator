import sys

def make_copy(from_file, to_file):
    lines = None
    with open(from_file) as rf:
        print("reading from " + from_file)
        lines = [next(rf) for _ in range(1000)]
    
    with open(to_file, "a") as wf:
        for item in lines:
            wf.write(f"{item}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("You have to supply 2 parameters: file to read from and file to write to.")
    try:
        print(make_copy(sys.argv[1], sys.argv[2]))
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
