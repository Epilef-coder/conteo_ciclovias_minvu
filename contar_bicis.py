import argparse
import logging
import os
import sys
from time import process_time

from counter.constants import INPUT_DIR, COUNTER_DIR
from counter.parser.data_parser import DataParser
from counter.processor.counter_processor import CounterProcess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(argv):
    """
         Generar estadísticas del conteo de bicicletas
    """

    t_start = process_time()

    parser = argparse.ArgumentParser(description='Generar estadísticas del conteo de bicicletas')

    parser.add_argument("input_file",
                        help='nombre del archivo con la información del conteo (ejemplo: ContadoresHoras.csv)')

    parser.add_argument("--fecha_analisis_1",
                        help='fecha analisis 1 en formato "dd/mm/yyyy-dd/mm/yyyy" (ejemplo: "01/01/2019-31/12/2020")')

    parser.add_argument("--fecha_analisis_2",
                        help='fecha analisis 2 en formato dd/mm/yyyy-dd/mm/yyyy (ejemplo: "01/01/2019-31/12/2020")')

    args = parser.parse_args(argv[1:])
    input_file_path = os.path.join(INPUT_DIR, args.input_file)
    info_counters_path = os.path.join(COUNTER_DIR, "contadores.csv")

    fechas_1 = args.fecha_analisis_1
    fechas_2 = args.fecha_analisis_2

    start_date1 = fechas_1.split("-")[0] if fechas_1 is not None else None
    end_date1 = fechas_1.split("-")[1] if fechas_1 is not None else None
    start_date2 = fechas_2.split("-")[0] if fechas_2 is not None else None
    end_date2 = fechas_2.split("-")[1] if fechas_2 is not None else None

    logger.info("Leyendo archivo: {}".format(input_file_path))
    counter_data = DataParser().parser_counter_data(input_file_path)
    counter_info = DataParser().parser_counter(info_counters_path)

    logger.info("Número de filas del documento: {}".format(len(counter_data)))

    counter_process_obj = CounterProcess(counter_data, counter_info, start_date1, end_date1, start_date2, end_date2)

    counter_process_obj.process()

    t_end = process_time()
    logger.info("Tarea finalizada en  {} [s]".format(t_end - t_start))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
