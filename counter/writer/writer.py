import csv

from typing import List
from counter.models.data_by_comuna import DataComuna

class Writer:
    def __init__(self):
        pass

    @staticmethod
    def write_to_file(header, data, output_file_path, mapper):
        with open(output_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(header)
            for row in data:
                mapped_row = mapper(row)
                writer.writerow(mapped_row)

    def write_by_comuna(self, processed_comuna: List[DataComuna], output_file_path):
        header = ["comuna", "region", "year", "month", "day", "str_date", "n_contadores", "count_1", "count_2"]

        def inner_mapper(data: DataComuna):
            return [data.comuna, data.region, data.year, data.month, data.day, data.str_date, data.n_counters, data.count_1, data.count_2]

        self.write_to_file(header=header, data=processed_comuna, output_file_path=output_file_path, mapper=inner_mapper)