import logging
import matplotlib as mpl
# mpl.use('Qt5Agg')

logging.basicConfig(level=logging.INFO, format='%(levelname)s\t%(asctime)s\t%(name)s\t%(threadName)s\t%(message)s')

from modules.climatedynamics import ClimateDynamics


def main():
    # cd = ClimateDynamics('empty')
    # cd.run()
    cd = ClimateDynamics('dcmip_perturbation')
    cd.run()
    cd = ClimateDynamics('dcmip_no_perturbation')
    cd.run()


if __name__ == '__main__':
    main()
