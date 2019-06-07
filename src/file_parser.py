import re


class FileParser:
    lines_in_section = 0
    taxes = 0
    total = 0

    def __init__(self, path):
        self.path = path

    def parse(self):
        with open(self.path) as file:
            for line in file:
                self.parse_line(line.replace('\n', ''))
            self.print_summary()

    def parse_line(self, line):
        # excluding empty lines
        if line == '':
            return

        # check if is 'Input x:' line
        input_match = re.search('^Input (\\d+):$', line)
        if input_match:
            if self.lines_in_section > 0:
                self.print_summary()
                print()
            print(f'Output: ${input_match.groups()[0]}')
            self.lines_in_section = 0
            self.taxes = 0
            self.total = 0
            return

        # standard line
        self.lines_in_section += 1
        print(line)

    def print_summary(self):
        print(f'Sales Taxes: {self.taxes}')
        print(f'Total: {self.total}')
