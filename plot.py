import argparse
import logging
import os
import sys
from time import process_time

from counter.constants import TMP_DIR
from counter.parser.data_parser import DataParser
from counter.utils.histograms import Histogram

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(argv):
    """
         Generar vistas de estadísticas de bicicletas por comuna
    """

    t_start = process_time()

    parser = argparse.ArgumentParser(description='Generar vistas de estadísticas de bicicletas por comuna')

    args = parser.parse_args(argv[1:])

    input_file = os.path.join(TMP_DIR, "conteo_por_comuna.csv")

    comuna_data = DataParser().parser_comuna_data(input_file)

    histogram_obj = Histogram(comuna_data)

    histogram_obj.plot_dash()

    t_end = process_time()
    logger.info("Tarea finalizada en  {} [s]".format(t_end - t_start))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
