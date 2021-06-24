import argparse
import siliconcompiler as sc
import os

from sources import add_sources

def configure_general(chip):
    # Prevent us from erroring out on lint warnings during import
    chip.set('relax', 'true')

    # hack to work around fact that $readmemh now runs in context of build
    # directory and can't load .mem files using relative paths
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    chip.add('define', f'MEM_ROOT={cur_dir}')

    add_sources(chip)

def configure_asic(chip):
    chip.add('design', 'top_asic')

    chip.add('source', 'hw/top_asic.v')
    chip.add('source', 'oh/padring/hdl/oh_padring.v')
    chip.add('source', 'oh/padring/hdl/oh_pads_corner.v')
    chip.add('source', 'oh/padring/hdl/oh_pads_domain.v')
    chip.add('source', 'oh/padring/hdl/oh_pads_gpio.v')

    chip.add('define', 'PRIM_DEFAULT_IMPL="prim_pkg::ImplFreePdk45"')

    chip.set('target', 'freepdk45_asic-sv2v')
    #chip.set('asic', 'floorplan', 'asic/floorplan.py')
    chip.set('constraint', 'asic/constraints.sdc')

    # TODO: floorplan library will handle this, but hard-code tinyRocket size
    # for now
    chip.set('asic', 'diesize', '0 0 924.92 799.4')
    chip.set('asic', 'coresize', '10.07 9.8 914.85 789.6')

    macro = 'sram_32x2048_1rw'
    chip.add('asic', 'macrolib', macro)
    chip.add('macro', macro, 'model', 'typical', 'nldm', 'lib', f'hw/prim/freepdk45/{macro}.lib')
    chip.add('macro', macro, 'lef', f'hw/prim/freepdk45/{macro}.lef')

def configure_fpga(chip):
    chip.add('design', 'top_icebreaker')

    chip.add('source', 'hw/top_icebreaker.v')
    chip.set('target', 'ice40_nextpnr')
    chip.set('constraint', 'fpga/icebreaker.pcf')

def main():
    parser = argparse.ArgumentParser(description='Build ZeroSoC')
    parser.add_argument('--fpga', action='store_true', default=False, help='Build for ice40 FPGA (build ASIC by default)')
    options = parser.parse_args()

    chip = sc.Chip()
    configure_general(chip)

    if options.fpga:
        configure_fpga(chip)
    else:
        configure_asic(chip)

    chip.set_jobid()
    chip.target()

    chip.run()

    chip.summary()

if __name__ == '__main__':
    main()
