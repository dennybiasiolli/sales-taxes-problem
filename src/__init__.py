from .file_parser import FileParser

def parse_files(input_paths):
    for path in input_paths:
        p = FileParser(path)
        p.parse()
        print()
