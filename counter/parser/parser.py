import csv


class Parser:

    @staticmethod
    def parse_data(input_file, data_mapper, delimiter, header: bool = False):
        """
            to parse a input file with a specific structure data  give by data_mapper
        """
        results = []

        with open(input_file, newline='', encoding="utf8") as contents:

            reader = csv.reader(contents, delimiter=delimiter)
            # this skips first row of csv file
            if header:
                next(reader)

            for raw_row in reader:
                if len(raw_row) == 0:  # skip extra empty lines in file
                    continue

                results.append(data_mapper(raw_row))

        return results
