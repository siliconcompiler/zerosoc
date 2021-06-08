import argparse
import siliconcompiler as sc

def configure_general(chip):
    # Prevent us from erroring out on lint warnings during import
    chip.set('relax', 'true')

def configure_asic(chip):
    chip.add('design', 'zerosoc')
    chip.add('source', 'zerosoc_asic.v')
    #chip.add('source', 'hw/top_asic.v')
    #chip.add('source', 'hw/pad.v')
    chip.set('target', 'freepdk45')
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
    chip.add('source', 'zerosoc_fpga.v')
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

    # TODO: I think 'stop' might not work before target, so can't include it in
    # configure_asic() function
    if not options.fpga:
        chip.set('stop', 'syn')

    chip.run()


if __name__ == '__main__':
    main()
