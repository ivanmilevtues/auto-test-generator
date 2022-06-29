import os


class ImportResolver:
    def __init__(self, base_dir):
        self.files = self.__get_all_python_files(base_dir)

    def find_imports(self, error_names: set):
        import_lines = []
        lines = []
        for file in self.files:
            try:
                with open(file, 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    found_strings = []
                    for name in error_names:
                        if 'import' in line and name in line:
                            import_lines.append(line)
                            found_strings.append(name)
                    for s in found_strings:
                        error_names.remove(s)

                    if len(error_names) == 0:
                        return import_lines + lines, len(import_lines) > 0
            except FileNotFoundError as e:
                print("FileNotFoundError ", e)
        return import_lines + lines, len(import_lines) > 0,

    @staticmethod
    def __get_all_python_files(base_dir):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(base_dir):
            files += [os.path.join(dirpath, file) for file in filenames if file.endswith(".py")]
        return files
