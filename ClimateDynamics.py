import logging
import matplotlib as mpl
# mpl.use('Qt5Agg')

logging.basicConfig(level=logging.INFO, format='%(levelname)s\t%(asctime)s\t%(name)s\t%(threadName)s\t%(message)s')

from modules.climatedynamics import ClimateDynamics


def main():
    cd = ClimateDynamics()
    cd.run()


if __name__ == '__main__':
    main()
