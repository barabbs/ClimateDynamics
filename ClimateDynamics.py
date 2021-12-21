import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s\t%(asctime)s\t%(name)s\t%(threadName)s\t%(message)s')

from modules.climatedynamics import ClimateDynamics


def main():
    for n in ('30-min_dcmip_no-pert', '30-min_dcmip_pert', 'slab-surf_dcmip_no-pert', 'slab-surf_dcmip_pert', 'dcmip_no-pert', '200-irr_dcmip_no-pert', '200-irr_slab-surf_dcmip_no-pert',
              '100-irr_dcmip_no-pert', '100-irr_slab-surf_dcmip_no-pert'):  # ('empty', 'dcmip_pert', '200-irr_dcmip_pert', '200-irr_slab-surface_dcmip_pert', '100-irr_dcmip_pert', '100-irr_slab-surface_dcmip_pert', 'impr', 'impr_dcmip_pert', 'impr_dcmip_no-pert'):
        cd = ClimateDynamics(n, True)
        cd.run()


if __name__ == '__main__':
    main()
