import os


class ImportResolver:
    def __init__(self, base_dir):
        self.files = self.__get_all_python_files(base_dir)

    def find_imports(self, error_names: set):
        import_lines = []
        for file in self.files:
            with open(file, 'r') as f:
                content = f.readlines()
            for line in content:
                found_strings = []
                for name in error_names:
                    if 'import' in line and name in line:
                        import_lines.append(line)
                        found_strings.append(line)
                [error_names.remove(s) for s in found_strings]

                if len(error_names) == 0:
                    return import_lines
        return import_lines

    @staticmethod
    def __get_all_python_files(base_dir):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(base_dir):
            files += [os.path.join(dirpath, file) for file in filenames if file.endswith(".py")]
        return files
