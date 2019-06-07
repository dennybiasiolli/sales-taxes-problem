import math
import re

from .constants import NO_TAX_PRODUCTS


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
            print(f'Output: {input_match.groups()[0]}')
            self.lines_in_section = 0
            self.taxes = 0
            self.total = 0
            return

        # standard line
        self.parse_product_line(line)
        self.lines_in_section += 1
        # print(line)

    def print_summary(self):
        print(f'Sales Taxes: {round(self.taxes, 2)}')
        print(f'Total: {round(self.total, 2)}')

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
        self.get_prices(quantity, description, is_imported, price)

    def get_prices(self, quantity, product, is_imported, price):
        """
        Basic sales tax is applicable at a rate of 10% on all goods,
        except books, food, and medical products that are exempt.
        Import duty is an additional sales tax applicable on all imported goods
        at a rate of 5%, with no exemptions.
        """
        tax = 0.10
        if any(p in product for p in NO_TAX_PRODUCTS):
            tax = 0
        if is_imported:
            tax += 0.05
        total_price = price * quantity
        total_tax = self.round_005(round(total_price * tax, 2))
        total = total_price + total_tax
        self.taxes += total_tax
        self.total += total
        print(f'{quantity} {product}: {round(total, 2)}')

    def round_005(self, val):
        (d, _) = math.modf(val * 10)
        if d > 0.0:
            return round((math.floor(val * 10) / 10) + 0.05, 2)
        return val
