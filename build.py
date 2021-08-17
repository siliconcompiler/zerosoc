import argparse
import siliconcompiler as sc
import os
import importlib
import shutil

from sources import add_sources

from asic.sky130.floorplan import core, padring

def init_chip(start, stop):
    chip = sc.Chip()

    # Prevent us from erroring out on lint warnings during import
    chip.set('relax', 'true')

    # hack to work around fact that $readmemh now runs in context of build
    # directory and can't load .mem files using relative paths
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    chip.add('define', f'MEM_ROOT={cur_dir}')

    chip.set('start', start)
    chip.set('stop', stop)

    return chip

def configure_asic_core(chip):
    chip.add('design', 'asic_core')
    chip.target('skywater130_svasicflow')

    add_sources(chip)

    # TODO: can use this logic once flowgraph schema is used properly
    # # Modify flow for SV synthesis:
    # # - Use morty for import (since Verilator is not SV-friendly)
    # # - Insert sv2v convert step in between import and syn stages
    # chip.cfg['flowgraph']['value']
    # chip.set('flowgraph', 'import', 'output', 'convert')
    # chip.set('flowgraph', 'import', 'tool', 'morty')
    # chip.set('flowgraph', 'convert', 'output', 'syn')
    # chip.set('flowgraph', 'convert', 'tool', 'sv2v')

    chip.set('constraint', 'asic/asic_core.sdc')

    chip.add('define', 'PRIM_DEFAULT_IMPL="prim_pkg::ImplSky130"')
    chip.add('define', 'RAM_DEPTH=512')

    chip.add('source', 'hw/asic_core.v')
    chip.set('asic', 'def', 'asic_core.def')

    # Need to configure IO macro libs so that floorplan generation can determine
    # cell dimensions
    macro = 'io'
    chip.add('asic', 'macrolib', macro)
    chip.add('macro', macro, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/io/sky130_dummy_io.lib')
    chip.set('macro', macro, 'lef', 'asic/sky130/io/sky130_ef_io.lef')
    chip.add('macro', macro, 'gds', 'asic/sky130/io/sky130_ef_io.gds')
    chip.set('macro', macro, 'cells', 'gpio', 'sky130_ef_io__gpiov2_pad')
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

    macro = 'ram'
    chip.add('asic', 'macrolib', macro)
    chip.add('macro', macro, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    chip.add('macro', macro, 'lef', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    chip.add('macro', macro, 'gds', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds')
    chip.set('macro', macro, 'cells', 'ram', 'sky130_sram_2kbyte_1rw1r_32x512_8')
    chip.add('source', 'hw/prim/sky130/prim_sky130_ram_1p.v')
    chip.add('source', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.bb.v')

def configure_asic_top(chip):
    chip.add('design', 'asic_top')
    chip.target('skywater130_physasicflow')

    # Hack: pass in empty constraint file to get rid of KLayout post-process
    # error (must have same name as design)
    chip.set('constraint', 'asic/asic_top.sdc')

    chip.add('source', 'hw/asic_top.v')
    chip.add('source', 'hw/asic_core.bb.v')
    chip.add('source', 'oh/padring/hdl/oh_padring.v')
    chip.add('source', 'oh/padring/hdl/oh_pads_domain.v')
    chip.add('source', 'oh/padring/hdl/oh_pads_corner.v')

    chip.add('source', 'asic/sky130/io/asic_iobuf.v')
    chip.add('source', 'asic/sky130/io/asic_iovdd.v')
    chip.add('source', 'asic/sky130/io/asic_iovddio.v')
    chip.add('source', 'asic/sky130/io/asic_iovss.v')
    chip.add('source', 'asic/sky130/io/asic_iovssio.v')
    chip.add('source', 'asic/sky130/io/asic_iocorner.v')

    chip.set('asic', 'def', 'asic_top.def')

    macro = 'core'
    chip.add('asic', 'macrolib', macro)
    chip.set('macro', macro, 'lef', 'asic_core.lef')
    chip.set('macro', macro, 'gds', 'asic_core.gds')
    chip.set('macro', macro, 'cells', 'asic_core', 'asic_core')

    macro = 'io'
    chip.add('asic', 'macrolib', macro)
    chip.add('macro', macro, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/io/sky130_dummy_io.lib')
    chip.set('macro', macro, 'lef', 'asic/sky130/io/sky130_ef_io.lef')
    # Need both of these GDS files to get corner cell to look correct
    chip.add('macro', macro, 'gds', 'asic/sky130/io/sky130_ef_io.gds')
    chip.add('macro', macro, 'gds', 'asic/sky130/io/sky130_fd_io.gds')
    chip.set('macro', macro, 'cells', 'gpio', 'sky130_ef_io__gpiov2_pad')
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

    macro = 'ram'
    chip.add('asic', 'macrolib', macro)
    chip.add('macro', macro, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    chip.add('macro', macro, 'lef', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    chip.add('macro', macro, 'gds', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds')
    chip.set('macro', macro, 'cells', 'ram', 'sky130_sram_2kbyte_1rw1r_32x512_8')
    chip.add('source', 'hw/prim/sky130/prim_sky130_ram_1p.v')
    chip.add('source', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.bb.v')

def configure_fpga(chip):
    chip.add('design', 'top_icebreaker')
    chip.target('target', 'ice40_fpgaflow')

    add_sources(chip)

    chip.add('source', 'hw/top_icebreaker.v')
    chip.set('constraint', 'fpga/icebreaker.pcf')

def build_fpga(start='import', stop='bitstream'):
    chip = init_chip(start, stop)
    configure_fpga(chip)
    run_build(chip)

def build_core(start='import', stop='export'):
    chip = init_chip(start, stop)
    configure_asic_core(chip)
    core.generate_floorplan(chip)
    run_build(chip)

    # copy out GDS for top-level integration
    if stop == 'export':
        design = chip.get('design')
        jobdir = (chip.get('build_dir') +
                "/" + design + "/" +
                chip.get('jobname') +
                str(chip.get('jobid')))
        shutil.copy(f'{jobdir}/export/outputs/{design}.gds', f'{design}.gds')

def build_top(start='import', stop='drc'):
    # check for necessary files generated by previous steps
    if not (os.path.isfile('asic_core.gds') and os.path.isfile('asic_core.lef')):
        raise Exception("Error building asic_top: can't find asic_core outputs. "
                        "Please re-run build.py without --top-only")

    chip = init_chip(start, stop)
    configure_asic_top(chip)
    padring.generate_floorplan(chip)
    run_build(chip)

def build_floorplans():
    chip = init_chip('import', 'export')
    configure_asic_core(chip)
    core.generate_floorplan(chip)

    chip = init_chip('import', 'export')
    configure_asic_top(chip)
    padring.generate_floorplan(chip)

def run_build(chip):
    chip.set_jobid()
    chip.run()
    chip.summary()

def main():
    parser = argparse.ArgumentParser(description='Build ZeroSoC')
    parser.add_argument('--fpga', action='store_true', default=False, help='Build for ice40 FPGA (build ASIC by default)')
    parser.add_argument('--core-only', action='store_true', default=False, help='Only build ASIC core GDS.')
    parser.add_argument('--top-only', action='store_true', default=False, help='Only integrate ASIC core into padring. Assumes ASIC core already built.')
    parser.add_argument('--floorplan-only', action='store_true', default=False, help='Generate floorplans only.')
    parser.add_argument('-a', '--start', default='import', help='Start step (for single-part builds)')
    parser.add_argument('-z', '--stop', default='drc', help='Stop step (for single-part builds)')
    options = parser.parse_args()

    if options.fpga:
        build_fpga(options.start, options.stop)
    elif options.floorplan_only:
        build_floorplans()
    elif options.core_only:
        build_core(options.start, options.stop)
    elif options.top_only:
        build_top(options.start, options.stop)
    else:
        build_core()
        build_top()

if __name__ == '__main__':
    main()
