import argparse
import siliconcompiler as sc
import os
import importlib
import shutil

from sources import add_sources

from floorplan_template import generate_core_floorplan, generate_top_floorplan

def init_chip(jobid=0):
    chip = sc.Chip()

    # Prevent us from erroring out on lint warnings during import
    chip.set('relax', 'true')
    chip.set('quiet', 'true')

    # hack to work around fact that $readmemh now runs in context of build
    # directory and can't load .mem files using relative paths
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    chip.add('define', f'MEM_ROOT={cur_dir}')

    return chip

def configure_svflow(chip, start=None, stop=None, verify=True):
    flowpipe = [('import', 'morty'),
                ('convert', 'sv2v'),
                ('syn', 'yosys'),
                ('floorplan', 'openroad'),
                ('place', 'openroad'),
                ('cts', 'openroad'),
                ('route', 'openroad'),
                ('dfm', 'openroad'),
                ('export', 'klayout')]

    for i, (step, tool) in enumerate(flowpipe):
        if i > 0:
            input_step, _ = flowpipe[i-1]
            chip.add('flowgraph', step, '0', 'input', input_step + '0')
        chip.set('flowgraph', step, '0', 'tool', tool)

    if verify:
        chip.set('flowgraph', 'extspice', '0', 'tool', 'magic')
        chip.add('flowgraph', 'extspice', '0', 'input', 'export0')

        chip.set('flowgraph', 'lvsjoin', '0', 'function', 'step_join')
        chip.add('flowgraph', 'lvsjoin', '0', 'input', 'dfm0')
        chip.add('flowgraph', 'lvsjoin', '0', 'input', 'extspice0')

        chip.set('flowgraph', 'lvs', '0', 'tool', 'netgen')
        chip.add('flowgraph', 'lvs', '0', 'input', 'lvsjoin0')

        chip.set('flowgraph', 'drc', '0', 'tool', 'magic')
        chip.add('flowgraph', 'drc', '0', 'input', 'export0')

        chip.set('flowgraph', 'signoff', '0', 'function', 'step_join')
        chip.add('flowgraph', 'signoff', '0', 'input', 'lvs0')
        chip.add('flowgraph', 'signoff', '0', 'input', 'drc0')

    # steps = [step for step, _ in flowpipe]
    # startidx = steps.index(start) if start else 0
    # stopidx = steps.index(stop) + 1 if stop else len(steps)
    # chip.set('steplist', steps[startidx:stopidx])

    # Make sure errors are reported in summary()
    for step in chip.getkeys('flowgraph'):
        chip.set('flowgraph', step, '0', 'weight', 'errors', 1.0)

    chip.set('showtool', 'def', 'klayout')
    chip.set('showtool', 'gds', 'klayout')

def configure_physflow(chip, start=None, stop=None):
    chip.set('flowgraph', 'import', '0', 'tool', 'verilator')

    chip.set('flowgraph', 'syn', '0', 'tool', 'yosys')
    chip.add('flowgraph', 'syn', '0', 'input', 'import0')

    chip.set('flowgraph', 'export', '0', 'tool', 'klayout')

    chip.set('flowgraph', 'extspice', '0', 'tool', 'magic')
    chip.add('flowgraph', 'extspice', '0', 'input', 'export0')

    chip.set('flowgraph', 'lvsjoin', '0', 'function', 'step_join')
    chip.add('flowgraph', 'lvsjoin', '0', 'input', 'syn0')
    chip.add('flowgraph', 'lvsjoin', '0', 'input', 'extspice0')

    chip.set('flowgraph', 'lvs', '0', 'tool', 'netgen')
    chip.add('flowgraph', 'lvs', '0', 'input', 'lvsjoin0')

    chip.set('flowgraph', 'drc', '0', 'tool', 'magic')
    chip.add('flowgraph', 'drc', '0', 'input', 'export0')

    chip.set('flowgraph', 'signoff', '0', 'function', 'step_join')
    chip.add('flowgraph', 'signoff', '0', 'input', 'lvs0')
    chip.add('flowgraph', 'signoff', '0', 'input', 'drc0')

    # Make sure errors are reported in summary()
    for step in chip.getkeys('flowgraph'):
        chip.set('flowgraph', step, '0', 'weight', 'errors', 1.0)

    chip.set('showtool', 'def', 'klayout')
    chip.set('showtool', 'gds', 'klayout')

def dump_flowgraphs():
    chip = init_chip()
    configure_svflow(chip)
    chip.writegraph('svflow.svg')

    chip = init_chip()
    configure_physflow(chip)
    chip.writegraph('physflow.svg')

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
    chip.set('library', libname, 'site', [])

    libname = 'ram'
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'type', 'component')
    chip.add('library', libname, 'nldm', 'typical', 'lib', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    chip.add('library', libname, 'lef', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    chip.add('library', libname, 'gds', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds')
    chip.set('library', libname, 'site', [])

    # Ignore cells in these libraries during DRC, they violate the rules but are
    # foundry-validated
    chip.set('exclude', ['ram', 'io'])

def configure_asic_core(chip, start, stop, verify=True):
    chip.set('design', 'asic_core')
    chip.target('skywater130')
    configure_svflow(chip, start, stop, verify)
    chip.set('eda', 'openroad', 'place', '0', 'option', 'place_density', ['0.15'])
    configure_libs(chip)

    add_sources(chip)

    chip.set('constraint', 'asic/asic_core.sdc')

    chip.add('define', 'PRIM_DEFAULT_IMPL="prim_pkg::ImplSky130"')
    chip.add('define', 'RAM_DEPTH=512')

    chip.add('source', 'hw/asic_core.v')
    chip.set('asic', 'def', 'asic_core.def')

    chip.add('source', 'hw/prim/sky130/prim_sky130_ram_1p.v')
    chip.add('source', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.bb.v')

    chip.add('source', 'hw/prim/sky130/prim_sky130_clock_gating.v')

def configure_asic_top(chip, start, stop):
    chip.set('design', 'asic_top')
    chip.target('skywater130')
    configure_physflow(chip, start, stop)
    configure_libs(chip)

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

    # Dummy blackbox modules just to get synthesis to pass (these aren't
    # acutally instantiated)
    chip.add('source', 'asic/sky130/io/asic_iopoc.v')
    chip.add('source', 'asic/sky130/io/asic_iocut.v')

    chip.add('source', 'asic/sky130/io/sky130_io.blackbox.v')

    chip.set('asic', 'def', 'asic_top.def')

    libname = 'core'
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'lef', 'asic_core.lef')
    chip.set('library', libname, 'gds', 'asic_core.gds')
    chip.set('library', libname, 'site', [])
    chip.set('library', libname, 'cells', 'asic_core', 'asic_core')
    chip.set('library', libname, 'netlist', 'verilog', 'asic_core.vg')

def configure_fpga(chip):
    chip.set('design', 'top_icebreaker')
    chip.target('target', 'ice40_fpgaflow')

    add_sources(chip)

    chip.add('source', 'hw/top_icebreaker.v')
    chip.set('constraint', 'fpga/icebreaker.pcf')

def build_fpga(start='import', stop='bitstream'):
    chip = init_chip()
    configure_fpga(chip)
    run_build(chip)

def build_core(start='import', stop='lvs', verify=True):
    chip = init_chip()
    configure_asic_core(chip, start, stop, verify)
    generate_core_floorplan(chip)
    run_build(chip)

    # copy out GDS for top-level integration
    gds = chip.find_result('gds', step='export')
    netlist = chip.find_result('vg', step='dfm')
    shutil.copy(gds, os.path.basename(gds))
    shutil.copy(netlist, os.path.basename(netlist))

def build_top(start='import', stop='drc'):
    # check for necessary files generated by previous steps
    if not (os.path.isfile('asic_core.gds') and
            os.path.isfile('asic_core.lef') and
            os.path.isfile('asic_core.vg')):
        raise Exception("Error building asic_top: can't find asic_core outputs. "
                        "Please re-run build.py without --top-only")

    chip = init_chip()
    configure_asic_top(chip, start, stop)
    generate_top_floorplan(chip)
    run_build(chip)

def build_floorplans():
    chip = init_chip()
    configure_asic_core(chip, 'import', 'export')
    generate_core_floorplan(chip)

    chip = init_chip()
    configure_asic_top(chip, 'import', 'export_hack')
    generate_top_floorplan(chip)

def run_build(chip):
    chip.run()
    chip.summary()

def main():
    parser = argparse.ArgumentParser(description='Build ZeroSoC')
    parser.add_argument('--fpga', action='store_true', default=False, help='Build for ice40 FPGA (build ASIC by default)')
    parser.add_argument('--core-only', action='store_true', default=False, help='Only build ASIC core GDS.')
    parser.add_argument('--top-only', action='store_true', default=False, help='Only integrate ASIC core into padring. Assumes ASIC core already built.')
    parser.add_argument('--floorplan-only', action='store_true', default=False, help='Generate floorplans only.')
    parser.add_argument('--dump-flowgraph', action='store_true', default=False, help='Dump diagram of flowgraphs only.')
    parser.add_argument('--no-verification', action='store_true', default=False, help="Don't run DRC or LVS.")
    parser.add_argument('-a', '--start', default='import', help='Start step (for single-part builds)')
    parser.add_argument('-z', '--stop', default='drc', help='Stop step (for single-part builds)')
    options = parser.parse_args()

    if options.fpga:
        build_fpga(options.start, options.stop)
    elif options.floorplan_only:
        build_floorplans()
    elif options.dump_flowgraph:
        dump_flowgraphs()
    elif options.core_only:
        build_core(options.start, options.stop)
    elif options.top_only:
        build_top(options.start, options.stop)
    elif options.no_verification:
        build_core(verify=False)
        build_top(stop='export')
    else:
        build_core(verify=False)
        build_top(stop='lvs')

if __name__ == '__main__':
    main()
