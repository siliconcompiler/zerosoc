import argparse
import siliconcompiler as sc
import os
import importlib

from sources import add_sources

def configure_general(chip, start, stop):
    # Prevent us from erroring out on lint warnings during import
    chip.set('relax', 'true')

    # hack to work around fact that $readmemh now runs in context of build
    # directory and can't load .mem files using relative paths
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    chip.add('define', f'MEM_ROOT={cur_dir}')

    add_sources(chip)

    chip.set('start', start)
    chip.set('stop', stop)

def configure_asic(chip):
    chip.add('design', 'asic_core')
    chip.target('skywater130_svasicflow')

    # TODO: can use this logic once flowgraph schema is used properly
    # # Modify flow for SV synthesis: 
    # # - Use morty for import (since Verilator is not SV-friendly)
    # # - Insert sv2v convert step in between import and syn stages
    # chip.cfg['flowgraph']['value']
    # chip.set('flowgraph', 'import', 'output', 'convert')
    # chip.set('flowgraph', 'import', 'tool', 'morty')
    # chip.set('flowgraph', 'convert', 'output', 'syn')
    # chip.set('flowgraph', 'convert', 'tool', 'sv2v')

    chip.set('constraint', 'asic/constraints.sdc')

    chip.add('define', 'PRIM_DEFAULT_IMPL="prim_pkg::ImplSky130"')
    chip.add('define', 'RAM_DEPTH=512')

    chip.add('source', 'hw/asic_core.v')
    chip.set('asic', 'floorplan', 'asic/sky130/floorplan/core.py')

    macro = 'ram'
    chip.add('asic', 'macrolib', macro)
    chip.add('macro', macro, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    chip.add('macro', macro, 'lef', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    chip.add('macro', macro, 'gds', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds')
    chip.set('macro', macro, 'cells', 'ram', 'sky130_sram_2kbyte_1rw1r_32x512_8')
    chip.add('source', 'hw/prim/sky130/prim_sky130_ram_1p.v')
    chip.add('source', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.bb.v')

    macro = 'io'
    chip.add('asic', 'macrolib', macro)
    chip.add('macro', macro, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/io/sky130_dummy_io.lib')
    chip.set('macro', macro, 'lef', f'asic/sky130/io/sky130_ef_io.lef')
    chip.set('macro', macro, 'cells', 'gpio', 'sky130_ef_io__gpiov2_pad_wrapped')
    chip.set('macro', macro, 'cells', 'vdd', 'sky130_ef_io__vccd_hvc_pad')
    chip.set('macro', macro, 'cells', 'vddio', 'sky130_ef_io__vddio_hvc_pad')
    chip.set('macro', macro, 'cells', 'vss', 'sky130_ef_io__vssd_hvc_pad')
    chip.set('macro', macro, 'cells', 'vssio', 'sky130_ef_io__vssio_hvc_pad')
    chip.set('macro', macro, 'cells', 'corner', 'sky130_ef_io__corner_pad')
    chip.set('macro', macro, 'cells', 'fill1',  'sky130_ef_io__com_bus_slice_1um')
    chip.set('macro', macro, 'cells', 'fill5',  'sky130_ef_io__com_bus_slice_5um')
    chip.set('macro', macro, 'cells', 'fill10', 'sky130_ef_io__com_bus_slice_10um')
    chip.set('macro', macro, 'cells', 'fill20', 'sky130_ef_io__com_bus_slice_20um')
    chip.add('source', 'asic/sky130/io/sky130_io.blackbox.v')

def configure_fpga(chip):
    chip.add('design', 'top_icebreaker')
    chip.target('target', 'ice40_fpgaflow')

    chip.add('source', 'hw/top_icebreaker.v')
    chip.set('constraint', 'fpga/icebreaker.pcf')

def main():
    parser = argparse.ArgumentParser(description='Build ZeroSoC')
    parser.add_argument('--fpga', action='store_true', default=False, help='Build for ice40 FPGA (build ASIC by default)')
    parser.add_argument('-a', '--start', default='import', help='Start step')
    parser.add_argument('-z', '--stop', default='export', help='Stop step')
    options = parser.parse_args()

    chip = sc.Chip()
    configure_general(chip, options.start, options.stop)

    if options.fpga:
        configure_fpga(chip)
    else:
        configure_asic(chip)

    chip.set_jobid()

    chip.run()
    chip.summary()

if __name__ == '__main__':
    main()
