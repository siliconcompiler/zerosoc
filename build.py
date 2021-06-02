import argparse
import siliconcompiler as sc

def configure_general(chip):
    chip.add('source', 'zerosoc.v')
    # Prevent us from erroring out on lint warnings during import
    chip.set('relax', 'true')

def configure_asic(chip):
    chip.add('design', 'top_asic')
    chip.add('source', 'hw/top_asic.v')
    chip.add('source', 'hw/pad.v')
    chip.set('target', 'freepdk45')
    chip.set('asic', 'floorplan', 'asic/floorplan.py')
    chip.set('constraint', 'asic/constraints.sdc')

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


if __name__ == '__main__':
    main()
