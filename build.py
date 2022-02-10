#!/usr/bin/env python3

import argparse
import siliconcompiler as sc
import os
import shutil

from sources import add_sources

from floorplan import generate_core_floorplan, generate_top_floorplan

def init_chip():
    chip = sc.Chip()

    # Prevent us from erroring out on lint warnings during import
    chip.set('relax', 'true')
    chip.set('quiet', 'true')

    # hack to work around fact that $readmemh now runs in context of build
    # directory and can't load .mem files using relative paths
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    chip.add('define', f'MEM_ROOT={cur_dir}')

    return chip

def configure_physflow(chip, verify=True):
    flow = 'physflow'
    chip.node(flow, 'import', 'surelog')
    chip.node(flow, 'export', 'klayout')
    chip.edge(flow, 'import', 'export')

    if verify:
        chip.node(flow, 'syn', 'yosys')
        chip.edge(flow, 'import', 'syn')
        chip.node(flow, 'extspice', 'magic')
        chip.edge(flow, 'export', 'extspice')

        chip.node(flow, 'lvsjoin', 'join')
        chip.edge(flow, 'syn', 'lvsjoin')
        chip.edge(flow, 'extspice', 'lvsjoin')

        chip.node(flow, 'lvs', 'netgen')
        chip.edge(flow, 'lvsjoin', 'lvs')

        chip.node(flow, 'drc', 'magic')
        chip.edge(flow, 'export', 'drc')

        chip.node(flow, 'signoff', 'join')
        chip.edge(flow, 'lvs', 'signoff')
        chip.edge(flow, 'drc', 'signoff')

    # Make sure errors are reported in summary()
    for step in chip.getkeys('flowgraph', flow):
        chip.set('flowgraph', flow, step, '0', 'weight', 'errors', 1.0)

    chip.set('showtool', 'def', 'klayout')
    chip.set('showtool', 'gds', 'klayout')

    chip.set('flow', flow)

def dump_flowgraphs():
    chip = init_chip()
    configure_physflow(chip)
    chip.write_flowgraph('physflow.svg')

def configure_libs(chip):
    libname = 'io'
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'type', 'component')
    chip.add('library', libname, 'nldm', 'typical', 'lib', 'asic/sky130/io/sky130_dummy_io.lib')
    chip.set('library', libname, 'lef', 'asic/sky130/io/sky130_ef_io.lef')
    # Need both GDS files: ef relies on fd one
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_ef_io.gds')
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_fd_io.gds')
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_ef_io__gpiov2_pad_wrapped.gds')

    libname = 'ram'
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'type', 'component')
    chip.add('library', libname, 'nldm', 'typical', 'lib', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    chip.add('library', libname, 'lef', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    chip.add('library', libname, 'gds', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds')

    # Ignore cells in these libraries during DRC, they violate the rules but are
    # foundry-validated
    chip.set('asic', 'exclude', ['ram', 'io'])

def configure_asic_core(chip, verify=True, remote=False):
    chip.set('design', 'asic_core')
    if verify:
        chip.set('flowarg', 'verify', ['true'])
    chip.set('frontend', 'systemverilog')
    chip.load_target('skywater130_demo')
    chip.set('eda', 'openroad', 'variable', 'place', '0', 'place_density', ['0.15'])
    chip.set('eda', 'openroad', 'variable', 'route', '0', 'grt_allow_congestion', ['true'])
    configure_libs(chip)

    # Need to copy library files into build directory for remote run so the
    # server can access them
    if remote:
        chip.set('library', 'ram', 'nldm', 'typical', 'lib', True, field='copy')
        chip.set('library', 'ram', 'lef', True, field='copy')
        chip.set('library', 'ram', 'gds', True, field='copy')

    add_sources(chip)

    chip.clock(name='core_clock', pin='we_din\[5\]', period=20)

    chip.add('define', 'PRIM_DEFAULT_IMPL="prim_pkg::ImplSky130"')
    chip.add('define', 'RAM_DEPTH=512')

    chip.add('source', 'hw/asic_core.v')
    chip.set('read', 'def', 'floorplan', '0', 'asic_core.def')

    chip.add('source', 'hw/prim/sky130/prim_sky130_ram_1p.v')
    chip.add('source', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.bb.v')

    chip.add('source', 'hw/prim/sky130/prim_sky130_clock_gating.v')

    if remote:
        chip.set('remote', True)

def configure_asic_top(chip, verify=True):
    chip.set('design', 'asic_top')
    # TODO: this loads a little more than we need, but it makes it easier to
    # get floorplanning to run.
    chip.load_target('skywater130_demo')
    configure_physflow(chip, verify)
    configure_libs(chip)

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

    # Dummy blackbox modules just to get synthesis to pass (these aren't
    # acutally instantiated)
    chip.add('source', 'asic/sky130/io/asic_iopoc.v')
    chip.add('source', 'asic/sky130/io/asic_iocut.v')

    chip.add('source', 'asic/sky130/io/sky130_io.blackbox.v')

    chip.set('read', 'def', 'export', '0', 'asic_top.def')

    libname = 'core'
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'lef', 'asic_core.lef')
    chip.set('library', libname, 'gds', 'asic_core.gds')
    chip.set('library', libname, 'netlist', 'verilog', 'asic_core.vg')

def configure_fpga(chip):
    chip.set('design', 'top_icebreaker')
    chip.set('frontend', 'systemverilog')
    chip.set('fpga', 'partname', 'ice40up5k-sg48')
    chip.load_target('fpgaflow_demo')

    add_sources(chip)

    chip.add('source', 'hw/top_icebreaker.v')
    chip.add('source', 'hw/prim/ice40/prim_ice40_clock_gating.v')
    chip.set('constraint', 'fpga/icebreaker.pcf')

    chip.add('define', 'PRIM_DEFAULT_IMPL="prim_pkg::ImplIce40"')

def build_fpga():
    chip = init_chip()
    configure_fpga(chip)
    run_build(chip)

def build_core(verify=True, remote=False):
    chip = init_chip()
    configure_asic_core(chip, verify, remote)
    generate_core_floorplan(chip)
    # after generating floorplan, we don't need IO in macrolib anymore
    chip.set('asic', 'macrolib', ['ram'])
    run_build(chip)

    # copy out GDS for top-level integration
    gds = chip.find_result('gds', step='export')
    netlist = chip.find_result('vg', step='dfm')
    shutil.copy(gds, os.path.basename(gds))
    shutil.copy(netlist, os.path.basename(netlist))

    return chip

def build_top(verify=True):
    # check for necessary files generated by previous steps
    if not (os.path.isfile('asic_core.gds') and
            os.path.isfile('asic_core.lef') and
            os.path.isfile('asic_core.vg')):
        raise Exception("Error building asic_top: can't find asic_core outputs. "
                        "Please re-run build.py without --top-only")

    chip = init_chip()
    configure_asic_top(chip, verify)
    generate_top_floorplan(chip)
    run_build(chip)

    return chip

def build_floorplans():
    chip = init_chip()
    configure_asic_core(chip)
    generate_core_floorplan(chip)

    chip = init_chip()
    configure_asic_top(chip)
    generate_top_floorplan(chip)

def run_build(chip):
    chip.run()
    chip.summary()

def test_zerosoc_build():
    chip = build_core(verify=True)

    assert chip.get('metric', 'lvs', '0', 'errors', 'real') == 0
    assert chip.get('metric', 'drc', '0', 'errors', 'real') == 0

    # check for timing errors
    assert chip.get('metric', 'route', '0', 'holdslack', 'real') >= 0
    assert chip.get('metric', 'route', '0', 'holdwns', 'real') >= 0
    assert chip.get('metric', 'route', '0', 'holdtns', 'real') >= 0
    assert chip.get('metric', 'route', '0', 'setupslack', 'real') >= 0
    assert chip.get('metric', 'route', '0', 'setupwns', 'real') >= 0
    assert chip.get('metric', 'route', '0', 'setuptns', 'real') >= 0

    chip = build_top(verify=True)

    assert chip.get('metric', 'lvs', '0', 'errors', 'real') == 0
    assert chip.get('metric', 'drc', '0', 'errors', 'real') == 0

def test_fpga_build():
    build_fpga()

def main():
    parser = argparse.ArgumentParser(description='Build ZeroSoC')
    parser.add_argument('--fpga', action='store_true', default=False, help='Build FPGA bitstream.')
    parser.add_argument('--core-only', action='store_true', default=False, help='Only build ASIC core GDS.')
    parser.add_argument('--top-only', action='store_true', default=False, help='Only integrate ASIC core into padring. Assumes core already built.')
    parser.add_argument('--floorplan-only', action='store_true', default=False, help='Only generate floorplans.')
    parser.add_argument('--dump-flowgraph', action='store_true', default=False, help='Only dump diagram of flowgraphs.')
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
    elif options.dump_flowgraph:
        dump_flowgraphs()
    elif options.core_only:
        build_core(verify=verify, remote=options.remote)
    elif options.top_only:
        build_top(verify=verify)
    else:
        build_core(verify=False, remote=options.remote)
        build_top(verify=verify)

if __name__ == '__main__':
    main()
