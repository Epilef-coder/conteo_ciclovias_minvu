from counter.models.data_counter import DataCounter
from counter.models.counters import Counter
from counter.models.data_by_comuna import DataComuna
from counter.parser.parser import Parser

from typing import List


class DataParser(Parser):
    def __init__(self):
        pass

    def parser_counter_data(self, input_file) -> List[DataCounter]:
        def mapper(row):
            return DataCounter(row[0], row[1], row[2], row[3], int(row[4]), row[5], int(row[6]))

        return self.parse_data(input_file, mapper, ",", True)

    def parser_counter(self, input_file) -> List[Counter]:
        def mapper(row):
            return Counter(row[0], row[1], row[2], row[3], row[4], row[5], float(row[6]), float(row[7]))

        return self.parse_data(input_file, mapper, ";", True)

    def parser_comuna_data(self, input_file) -> List[DataComuna]:
        def mapper(row):
            return DataComuna(row[0], row[1], int(row[2]), int(row[3]), int(row[4]), row[5], int(row[6]), int(row[7]), int(row[8]))

        return self.parse_data(input_file, mapper, ";", True)
