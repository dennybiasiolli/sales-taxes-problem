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
        self.parse_product_line(line)
        self.lines_in_section += 1
        print(line)

    def print_summary(self):
        print(f'Sales Taxes: {self.taxes}')
        print(f'Total: {self.total}')

    def parse_product_line(self, line):
        input_match = re.search(
            '^([\\d]+) ([a-zA-Z ]+) at ([\\d]+.[\\d]+)$',
            line
        )
        if input_match is None or len(input_match.groups()) != 3:
            raise Exception(f'Line not recognized: "{line}"')

        [str_quantity, description, str_price] = input_match.groups()
        quantity = int(str_quantity)
        price = float(str_price)
        is_imported = False
        if 'imported ' in description:
            is_imported = True
