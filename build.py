#!/usr/bin/env python3

import argparse
import copy
import siliconcompiler
import os

from sources import add_sources

from floorplan import generate_core_floorplan, generate_top_floorplan

def setup_options(chip):
    '''Helper to setup common options for each build.'''
    chip.set('option', 'loglevel', 'INFO')

    # Prevent us from erroring out on lint warnings during import
    chip.set('option', 'relax', True)
    chip.set('option', 'quiet', True)

    # hack to work around fact that $readmemh now runs in context of build
    # directory and can't load .mem files using relative paths
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    chip.add('option', 'define', f'MEM_ROOT={cur_dir}')

def build_fpga():
    chip = siliconcompiler.Chip('top_icebreaker')
    setup_options(chip)

    chip.set('frontend', 'systemverilog')
    chip.set('fpga', 'partname', 'ice40up5k-sg48')
    chip.load_target('fpgaflow_demo')

    add_sources(chip)

    chip.add('input', 'verilog', 'hw/top_icebreaker.v')
    chip.add('input', 'verilog', 'hw/prim/ice40/prim_ice40_clock_gating.v')
    chip.set('input', 'pcf', 'fpga/icebreaker.pcf')

    chip.add('option', 'define', 'PRIM_DEFAULT_IMPL="prim_pkg::ImplIce40"')

    run_build(chip)

def configure_core_chip(remote=False):
    chip = siliconcompiler.Chip('asic_core')

    setup_options(chip)

    chip.set('option', 'frontend', 'systemverilog')
    chip.load_target('skywater130_demo')

    chip.set('tool', 'openroad', 'var', 'place', '0', 'place_density', ['0.15'])
    chip.set('tool', 'openroad', 'var', 'route', '0', 'grt_allow_congestion', ['true'])

    chip.set('asic', 'macrolib', ['sky130sram', 'sky130io'])
    chip.load_lib('sky130sram')
    chip.load_lib('sky130io')

    # Ignore cells in these libraries during DRC, they violate the rules but are
    # foundry-validated
    for step in ('extspice', 'drc'):
        chip.set('tool', 'magic', 'var', step, '0', 'exclude', ['sky130sram', 'sky130io'])
    chip.set('tool', 'netgen', 'var', 'lvs', '0', 'exclude', ['sky130sram', 'sky130io'])

    # Need to copy library files into build directory for remote run so the
    # server can access them
    if remote:
        stackup = chip.get('asic', 'stackup')
        chip.set('library', 'sky130sram', 'model', 'timing', 'nldm', True, field='copy')
        chip.set('library', 'sky130sram', 'model', 'layout', 'lef', stackup, True, field='copy')
        chip.set('library', 'sky130sram', 'model', 'layout', 'gds', stackup, True, field='copy')

        chip.set('option', 'remote', True)

    add_sources(chip)

    chip.clock('we_din\[5\]', period=20)

    chip.add('option', 'define', 'PRIM_DEFAULT_IMPL="prim_pkg::ImplSky130"')
    chip.add('option', 'define', 'RAM_DEPTH=512')

    chip.add('input', 'verilog', 'hw/asic_core.v')
    chip.set('input', 'floorplan.def', 'asic_core.def')

    chip.add('input', 'verilog', 'hw/prim/sky130/prim_sky130_ram_1p.v')
    chip.add('input', 'verilog', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.bb.v')

    chip.add('input', 'verilog', 'hw/prim/sky130/prim_sky130_clock_gating.v')

    return chip

def build_core(verify=True, remote=False):
    chip = configure_core_chip(remote)
    stackup = chip.get('asic', 'stackup')

    generate_core_floorplan(chip)
    chip.set('model', 'layout', 'lef', stackup, 'asic_core.lef')

    # after generating floorplan, we don't need IO in macrolib anymore
    chip.set('asic', 'macrolib', ['sky130sram'])

    run_build(chip)

    if verify:
        run_signoff(chip, 'dfm', 'export')

    # set up pointers to final outputs for integration
    gds = chip.find_result('gds', step='export')
    netlist = chip.find_result('vg', step='dfm')

    chip.set('model', 'layout', 'gds', stackup, gds)
    chip.set('output', 'netlist', netlist)
    chip.write_manifest('asic_core.pkg.json')

    return chip

def configure_top_chip(core_chip):
    chip = siliconcompiler.Chip('asic_top')

    setup_options(chip)

    # TODO: we need a library function to handle this
    chip.import_library(core_chip)

    # Ignore cells in these libraries during DRC, they violate the rules but are
    # foundry-validated
    for step in ('extspice', 'drc',):
        chip.set('tool', 'magic', 'var', step, '0', 'exclude', ['sky130sram', 'sky130io'])
    chip.set('tool', 'netgen', 'var', 'lvs', '0', 'exclude', ['sky130sram', 'sky130io'])

    chip.load_target('skywater130_demo')
    chip.set('option', 'flow', 'asictopflow')

    chip.set('asic', 'macrolib', ['asic_core', 'sky130sram', 'sky130io'])
    chip.load_lib('sky130sram')
    chip.load_lib('sky130io')

    chip.add('input', 'verilog', 'hw/asic_top.v')
    chip.add('input', 'verilog', 'hw/asic_core.bb.v')
    chip.add('input', 'verilog', 'oh/padring/hdl/oh_padring.v')
    chip.add('input', 'verilog', 'oh/padring/hdl/oh_pads_domain.v')
    chip.add('input', 'verilog', 'oh/padring/hdl/oh_pads_corner.v')

    chip.add('input', 'verilog', 'asic/sky130/io/asic_iobuf.v')
    chip.add('input', 'verilog', 'asic/sky130/io/asic_iovdd.v')
    chip.add('input', 'verilog', 'asic/sky130/io/asic_iovddio.v')
    chip.add('input', 'verilog', 'asic/sky130/io/asic_iovss.v')
    chip.add('input', 'verilog', 'asic/sky130/io/asic_iovssio.v')
    chip.add('input', 'verilog', 'asic/sky130/io/asic_iocorner.v')

    # Dummy blackbox modules just to get synthesis to pass (these aren't
    # acutally instantiated)
    chip.add('input', 'verilog', 'asic/sky130/io/asic_iopoc.v')
    chip.add('input', 'verilog', 'asic/sky130/io/asic_iocut.v')

    chip.add('input', 'verilog', 'asic/sky130/io/sky130_io.blackbox.v')

    chip.set('input', 'def', 'asic_top.def')

    return chip

def build_top(core_chip, verify=True):
    chip = configure_top_chip(core_chip)
    generate_top_floorplan(chip)
    run_build(chip)
    if verify:
        run_signoff(chip, 'syn', 'export')

    return chip

def build_floorplans():
    core_chip = configure_core_chip()
    generate_core_floorplan(core_chip)
    stackup = core_chip.get('asic', 'stackup')
    core_chip.set('model', 'layout', 'lef', stackup, 'asic_core.lef')

    top_chip = configure_top_chip(core_chip)
    generate_top_floorplan(top_chip)

def run_build(chip):
    chip.run()
    chip.summary()

def run_signoff(chip, netlist_step, layout_step):
    gds_path = chip.find_result('gds', step=layout_step)
    netlist_path = chip.find_result('vg', step=netlist_step)

    jobname = chip.get('option', 'jobname')
    chip.set('option', 'jobname', f'{jobname}_signoff')
    chip.set('option', 'flow', 'signoffflow')

    chip.set('input', 'gds', gds_path)
    chip.set('input', 'netlist', netlist_path)

    run_build(chip)

def test_zerosoc_build():
    chip = build_core(verify=True)

    assert chip.get('metric', 'lvs', '0', 'errors') == 0
    assert chip.get('metric', 'drc', '0', 'errors') == 0

    # check for timing errors
    assert chip.get('metric', 'route', '0', 'holdslack') >= 0
    assert chip.get('metric', 'route', '0', 'holdwns') >= 0
    assert chip.get('metric', 'route', '0', 'holdtns') >= 0
    assert chip.get('metric', 'route', '0', 'setupslack') >= 0
    assert chip.get('metric', 'route', '0', 'setupwns') >= 0
    assert chip.get('metric', 'route', '0', 'setuptns') >= 0

    chip = build_top(verify=True)

    assert chip.get('metric', 'lvs', '0', 'errors') == 0
    assert chip.get('metric', 'drc', '0', 'errors') == 0

def test_fpga_build():
    build_fpga()

def main():
    parser = argparse.ArgumentParser(description='Build ZeroSoC')
    parser.add_argument('--fpga', action='store_true', default=False, help='Build FPGA bitstream.')
    parser.add_argument('--core-only', action='store_true', default=False, help='Only build ASIC core GDS.')
    parser.add_argument('--top-only', action='store_true', default=False, help='Only integrate ASIC core into padring. Assumes core already built.')
    parser.add_argument('--floorplan-only', action='store_true', default=False, help='Only generate floorplans.')
    parser.add_argument('--no-verify', action='store_true', default=False, help="Don't run DRC and LVS.")
    parser.add_argument('--remote', action='store_true', default=False, help='Run on remote server. Requires SC remote credentials.')
    options = parser.parse_args()

    verify = not options.no_verify

    if options.remote and not options.core_only:
        raise ValueError('--remote flag requires --core-only')

    if options.fpga:
        build_fpga()
    elif options.floorplan_only:
        build_floorplans()
    elif options.core_only:
        build_core(verify=verify, remote=options.remote)
    elif options.top_only:
        chip = siliconcompiler.Chip('asic_core')
        chip.read_manifest('asic_core.pkg.json')
        build_top(chip, verify=verify)
    else:
        core_chip = build_core(verify=False, remote=options.remote)
        build_top(core_chip, verify=verify)

if __name__ == '__main__':
    main()
