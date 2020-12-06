import datetime
import logging
import os
from collections import defaultdict
from typing import List

from counter.constants import TMP_DIR
from counter.models.counters import Counter
from counter.models.data_by_comuna import DataComuna
from counter.models.data_counter import DataCounter
from counter.writer.writer import Writer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CounterProcess:
    def __init__(self, list_data: List[DataCounter], list_counters=List[Counter], start_date1=None, end_date1=None,
                 start_date2=None, end_date2=None):
        self.data = list_data
        self.counter = list_counters
        self.start_date = datetime.datetime.strptime(start_date1, "%d/%m/%Y") if start_date1 is not None else None
        self.end_date = datetime.datetime.strptime(end_date1, "%d/%m/%Y") if end_date1 is not None else None

        self.start_date2 = datetime.datetime.strptime(start_date2, "%d/%m/%Y") if start_date2 is not None else None
        self.end_date2 = datetime.datetime.strptime(end_date2, "%d/%m/%Y") if end_date2 is not None else None

    def process(self):
        logger.info("Procesando información")
        info_group_by_comuna, info_group_by_counter = self.group_by()

        logger.info("Fin del procesamiento")

        logger.info("Escribir archivo de salida")

        data_write_comuna = self.get_group_by_output_to_write(info_group_by_comuna, info_group_by_counter)

        output_file = os.path.join(TMP_DIR, "conteo_por_comuna.csv")

        Writer().write_by_comuna(data_write_comuna, output_file)

        return info_group_by_comuna, info_group_by_counter

    def get_dic_counters(self):
        output = defaultdict(None)
        for counter in self.counter:
            if counter.id is not None:
                output[counter.id] = counter
        return output

    def group_by(self):

        dic_counters = self.get_dic_counters()

        output_year_month_day_region_comuna = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(None)))))

        output_year_month_day_region_comuna_counter = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(None))))))

        for data in self.data:

            str_date = data.str_date
            str_time = data.str_time

            date = datetime.datetime.strptime(str_date, "%m/%d/%y")

            # filtramos por tiempo
            if self.start_date is not None:
                if date < self.start_date:
                    continue

            if self.end_date is not None:
                if date > self.end_date:
                    continue

            try:
                time = datetime.datetime.strptime(str_time, "%H:%M:%S")
            except ValueError:
                time = datetime.datetime.strptime(str_time, "%H:%M")

            year = date.year
            month = date.month
            day = date.day

            if dic_counters.get(data.id_prov):
                info_counter: Counter = dic_counters[data.id_prov]

                region = info_counter.region
                comuna = info_counter.comuna
                counter = data.id_prov

                if output_year_month_day_region_comuna_counter[year][month][day][region][comuna].get(counter):
                    prev_counter_counter1, prev_counter_counter2 = \
                        output_year_month_day_region_comuna_counter[year][month][day][region][comuna][counter]
                else:
                    prev_counter_counter1, prev_counter_counter2 = (0, 0)

                if output_year_month_day_region_comuna[year][month][day][region].get(comuna):
                    prev_counter_comuna1, prev_counter_comuna2 = \
                        output_year_month_day_region_comuna[year][month][day][region][comuna]
                else:
                    prev_counter_comuna1, prev_counter_comuna2 = (0, 0)

                output_year_month_day_region_comuna_counter[year][month][day][region][comuna][counter] = (
                    prev_counter_counter1 + data.counter, prev_counter_counter2)
                output_year_month_day_region_comuna[year][month][day][region][comuna] = (
                    prev_counter_comuna1 + data.counter, prev_counter_comuna2)

            else:
                logger.info("id counter {} not found".format(data.id_prov))

        if self.start_date2 is None and self.end_date2 is None:
            return output_year_month_day_region_comuna, output_year_month_day_region_comuna_counter

        for data in self.data:

            str_date = data.str_date
            str_time = data.str_time

            date = datetime.datetime.strptime(str_date, "%m/%d/%y")

            # filtramos por tiempo
            if self.start_date2 is not None:
                if date < self.start_date2:
                    continue

            if self.end_date2 is not None:
                if date > self.end_date2:
                    continue

            try:
                time = datetime.datetime.strptime(str_time, "%H:%M:%S")
            except ValueError:
                time = datetime.datetime.strptime(str_time, "%H:%M")

            year = date.year
            month = date.month
            day = date.day

            if dic_counters.get(data.id_prov):
                info_counter: Counter = dic_counters[data.id_prov]

                region = info_counter.region
                comuna = info_counter.comuna
                counter = data.id_prov

                if output_year_month_day_region_comuna_counter[year][month][day][region][comuna].get(counter):
                    prev_counter_counter1, prev_counter_counter2 = \
                        output_year_month_day_region_comuna_counter[year][month][day][region][comuna][counter]
                else:
                    prev_counter_counter1, prev_counter_counter2 = (0, 0)

                if output_year_month_day_region_comuna[year][month][day][region].get(comuna):
                    prev_counter_comuna1, prev_counter_comuna2 = \
                        output_year_month_day_region_comuna[year][month][day][region][comuna]
                else:
                    prev_counter_comuna1, prev_counter_comuna2 = (0, 0)

                output_year_month_day_region_comuna_counter[year][month][day][region][comuna][counter] = (
                    prev_counter_counter1, prev_counter_counter2 + data.counter)
                output_year_month_day_region_comuna[year][month][day][region][comuna] = (
                    prev_counter_comuna1, prev_counter_comuna2 + data.counter)

            else:
                logger.info("id counter {} not found".format(data.id_prov))

        return output_year_month_day_region_comuna, output_year_month_day_region_comuna_counter

    def log_group_by(self, output_group_by, output_group_by_counter):
        for year in output_group_by:
            logger.info("Año {}".format(year))
            for month in output_group_by[year]:
                logger.info("\tMes {}".format(month))
                for day in output_group_by[year][month]:
                    logger.info("\t\tDía {}".format(day))
                    for region in output_group_by[year][month][day]:
                        for comuna in output_group_by[year][month][day][region]:
                            count1, count2 = output_group_by[year][month][day][region][comuna]
                            n_counters = len(output_group_by_counter[year][month][day][region][comuna])
                            logger.info(
                                "\t\t\tRegión {} - Comuna {}: {} [contadores], count1 {} [bicis], count2 {} [bicis]".format(
                                    region,
                                    comuna,
                                    n_counters,
                                    count1,
                                    count2))

    def get_group_by_output_to_write(self, output_group_by, output_group_by_counter) -> List[DataComuna]:

        output = []
        for year in output_group_by:

            for month in output_group_by[year]:

                for day in output_group_by[year][month]:

                    for region in output_group_by[year][month][day]:
                        for comuna in output_group_by[year][month][day][region]:
                            count1, count2 = output_group_by[year][month][day][region][comuna]
                            n_counters = len(output_group_by_counter[year][month][day][region][comuna])
                            output.append(
                                DataComuna(comuna, region, year, month, day, "{}-{}-{}".format(day, month, year),
                                           n_counters, count1, count2))
        return output
