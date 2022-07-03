import os


class ImportResolver:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def find_imports(self, error_names: set):
        print('error names', error_names)
        import_lines = []
        files = self.__get_all_python_files()
        print(files)
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
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
                        return import_lines, len(import_lines) > 0
            except FileNotFoundError as e:
                print("FileNotFoundError ", e)
        return import_lines, len(import_lines) > 0,

    def __get_all_python_files(self):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(self.base_dir):
            files += [os.path.join(dirpath, file) for file in filenames if file.endswith(".py")]
        return files
