import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s\t%(asctime)s\t%(name)s\t%(threadName)s\t%(message)s')

from modules.climatedynamics import ClimateDynamics


def main():
    for n in ('improved_dcmip_no_perturbation', 'improved_dcmip_perturbation', 'dcmip_no_perturbation_less_irradiance_slab_surface', 'dcmip_perturbation_less_irradiance_slab_surface',
              'improved_no_perturbation', 'dcmip_no_perturbation_less_irradiance', 'dcmip_perturbation_less_irradiance'):
        cd = ClimateDynamics(n, True)
        cd.run()


if __name__ == '__main__':
    main()
