#!/usr/bin/env python3

import siliconcompiler

import argparse
import os
import sys

# Libraries
from lambdapdk.sky130.libs import sky130sram, sky130io
from siliconcompiler.targets import skywater130_demo

from siliconcompiler.tools.openroad import openroad
from siliconcompiler.tools._common import get_tool_tasks

from floorplan import generate_core_floorplan, generate_top_floorplan, generate_top_flat_floorplan
import zerosoc_core
import zerosoc_top

ASIC_CORE_CFG = 'zerosoc_core.pkg.json'


def configure_remote(chip):
    chip.set('option', 'remote', True)

    for library in chip.getkeys('library'):
        if library in ['sky130hd', 'sky130io']:
            # No need to copy library
            continue
        for fileset in chip.getkeys('library', library, 'output'):
            for filetype in chip.getkeys('library', library, 'output', fileset):
                # Need to copy library files into build directory for remote run so the
                # server can access them
                chip.hash_files('library', library, 'output', fileset, filetype)
                chip.set('library', library, 'output', fileset, filetype, True, field='copy')

    for tool in chip.getkeys('tool'):
        for task in chip.getkeys('tool', tool, 'task'):
            for file_var in chip.getkeys('tool', tool, 'task', task, 'file'):
                # Need to copy tool files into build directory for remote run so the
                # server can access them
                chip.hash_files('tool', tool, 'task', task, 'file', file_var)
                chip.set('tool', tool, 'task', task, 'file', file_var, True, field='copy')


def build_fpga():
    chip = siliconcompiler.Chip('top_icebreaker')

    chip.set('fpga', 'partname', 'ice40up5k-sg48')
    chip.load_target('fpgaflow_demo')

    chip.use(zerosoc_core)

    chip.input('hw/top_icebreaker.v', package='zerosoc')
    chip.input('hw/prim/ice40/prim_ice40_clock_gating.v', package='zerosoc')
    chip.input('fpga/icebreaker.pcf', package='zerosoc')

    chip.add('option', 'define', 'PRIM_DEFAULT_IMPL="prim_pkg::ImplIce40"')

    run_build(chip)


def configure_core_chip():
    chip = siliconcompiler.Chip('zerosoc_core')
    chip.set('option', 'entrypoint', 'asic_core')

    chip.load_target(skywater130_demo)

    chip.add('option', 'define', 'SYNTHESIS')
    chip.use(zerosoc_core)

    chip.use(sky130sram)
    chip.swap_library('lambdalib_ramlib', 'lambdalib_sky130sram')

    chip.set('asic', 'macrolib', ['sky130_sram_1rw1r_64x256_8'])

    # Ignore cells in these libraries during DRC, they violate the rules but are
    # foundry-validated
    for task in ('extspice', 'drc'):
        chip.add('tool', 'magic', 'task', task, 'var', 'exclude', 'sky130_sram_1rw1r_64x256_8')
    chip.add('tool', 'netgen', 'task', 'lvs', 'var', 'exclude', 'sky130_sram_1rw1r_64x256_8')

    chip.set('tool', 'openroad', 'task', 'export', 'var', 'ord_abstract_lef_bloat_layers', 'false')

    chip.clock(r'we_din\[5\]', period=66)

    return chip


def setup_core():
    chip = configure_core_chip()

    chip.set('tool', 'openroad', 'task', 'floorplan', 'var', 'rtlmp_enable', 'true')
    chip.set('tool', 'openroad', 'task', 'place', 'var', 'place_density', '0.40')
    chip.set('tool', 'openroad', 'task', 'route', 'var', 'grt_macro_extension', '0')
    chip.set('tool', 'openroad', 'task', 'export', 'var', 'write_cdl', 'false')

    generate_core_floorplan(chip)

    return chip


def setup_core_module(chip):
    # set up pointers to final outputs for integration
    # Set physical outputs
    stackup = chip.get('option', 'stackup')
    chip.set('output', stackup, 'gds', chip.find_result('gds', step='write_gds'))
    chip.set('output', stackup, 'lef', chip.find_result('lef', step='write_data'))

    # Set output netlist
    chip.set('output', 'netlist', 'verilog', chip.find_result('vg', step='write_data'))

    # Set timing libraries
    for scenario in chip.getkeys('constraint', 'timing'):
        corner = chip.get('constraint', 'timing', scenario, 'libcorner')[0]
        lib = chip.find_result(f'{corner}.lib', step='write_data')
        chip.set('output', corner, 'nldm', lib)

    # Set pex outputs
    for scenario in chip.getkeys('constraint', 'timing'):
        corner = chip.get('constraint', 'timing', scenario, 'pexcorner')
        spef = chip.find_result(f'{corner}.spef', step='write_data')
        chip.set('output', corner, 'spef', spef)

    # Hash output files
    for fileset in chip.getkeys('output'):
        for filetype in chip.getkeys('output', fileset):
            chip.hash_files('output', fileset, filetype)

    chip.write_manifest(ASIC_CORE_CFG)


def build_core(verify=True, remote=False, resume=False, floorplan=False):
    chip = setup_core()
    chip.set('option', 'clean', not resume)
    chip.set('option', 'breakpoint', floorplan and not remote, step='floorplan')

    run_build(chip, remote)

    if verify:
        run_signoff(chip, 'dfm', 'export')

    setup_core_module(chip)

    return chip


def configure_top_flat_chip():
    chip = siliconcompiler.Chip('zerosoc')
    chip.set('option', 'entrypoint', 'asic_top')

    chip.load_target(skywater130_demo)
    chip.set('option', 'flow', 'asicflow')

    chip.add('option', 'define', 'SYNTHESIS')
    chip.use(zerosoc_top)
    chip.use(zerosoc_core)

    chip.use(sky130io)
    chip.use(sky130sram)
    chip.set('asic', 'macrolib', ['sky130_sram_1rw1r_64x256_8', 'sky130io'])
    chip.swap_library('lambdalib_ramlib', 'lambdalib_sky130sram')
    chip.swap_library('lambdalib_iolib', 'lambdalib_sky130io')

    # Ignore cells in these libraries during DRC, they violate the rules but are
    # foundry-validated
    for task in ('extspice', 'drc'):
        chip.add('tool', 'magic', 'task', task, 'var', 'exclude', 'sky130io')
    chip.add('tool', 'netgen', 'task', 'lvs', 'var', 'exclude', 'sky130io')

    # OpenROAD settings
    chip.set('tool', 'openroad', 'task', 'floorplan', 'var', 'rtlmp_enable', 'true')
    chip.set('tool', 'openroad', 'task', 'route', 'var', 'grt_macro_extension', '0')
    for task in get_tool_tasks(chip, openroad):
        chip.add('tool', 'openroad', 'task', task, 'var', 'psm_skip_nets', 'ioring*')
        chip.add('tool', 'openroad', 'task', task, 'var', 'psm_skip_nets', 'v*io')

    chip.clock(r'padring.iwest.ipad\[3\].gbidir.i0.gpio/IN', period=60)

    return chip


def configure_top_chip(core_chip=None):
    chip = siliconcompiler.Chip('zerosoc_top')

    if not core_chip:
        if not os.path.exists(ASIC_CORE_CFG):
            print(f"'{ASIC_CORE_CFG}' has not been generated.", file=sys.stderr)
            return
        core_chip = siliconcompiler.Library(chip, 'zerosoc_core')
        core_chip.read_manifest(ASIC_CORE_CFG)
        core_chip.set('design', 'asic_zerosoc_core')

    chip = siliconcompiler.Chip('zerosoc_top')
    chip.set('option', 'entrypoint', 'asic_top')

    chip.load_target(skywater130_demo)
    chip.set('option', 'flow', 'asicflow')

    chip.use(core_chip)
    chip.use(zerosoc_top)
    chip.use(sky130io)
    chip.set('asic', 'macrolib', [core_chip.design, 'sky130io'])
    chip.swap_library('lambdalib_iolib', 'lambdalib_sky130io')
    chip.swap_library('zerosoc_core', None)

    # Ignore cells in these libraries during DRC, they violate the rules but are
    # foundry-validated
    for task in ('extspice', 'drc'):
        chip.add('tool', 'magic', 'task', task, 'var', 'exclude', 'sky130io')
    chip.add('tool', 'netgen', 'task', 'lvs', 'var', 'exclude', 'sky130io')

    for tool in core_chip.getkeys('tool'):
        for task in core_chip.getkeys('tool', tool, 'task'):
            if core_chip.valid('tool', tool, 'task', task, 'var', 'exclude'):
                exclude = core_chip.get('tool', tool, 'task', task, 'var', 'exclude')
                chip.set('tool', tool, 'task', task, 'var', 'exclude', exclude)

    # OpenROAD settings
    chip.set('tool', 'openroad', 'task', 'route', 'var', 'grt_macro_extension', '0')

    for met, adj in (('met2', 0.2),
                     ('met3', 0.1),
                     ('met4', 0.1),
                     ('met5', 0.1)):
        chip.set('pdk', 'skywater130', 'var', 'openroad', f'{met}_adjustment', '5M1LI', str(adj))

    for task in get_tool_tasks(chip, openroad):
        chip.add('tool', 'openroad', 'task', task, 'var', 'psm_skip_nets', 'ioring*')
        chip.add('tool', 'openroad', 'task', task, 'var', 'psm_skip_nets', 'v*io')

    return chip


def setup_top_flat():
    chip = configure_top_flat_chip()
    generate_top_flat_floorplan(chip)

    return chip


def setup_top_hier(core_chip):
    chip = configure_top_chip(core_chip)
    generate_top_floorplan(chip)

    return chip


def build_top_flat(verify=True, resume=False, remote=False, floorplan=False):
    chip = setup_top_flat()
    chip.set('option', 'clean', not resume)

    chip.set('option', 'breakpoint', floorplan and not remote, step='floorplan')

    run_build(chip, remote)
    if verify:
        run_signoff(chip, 'syn', 'export')

    return chip


def build_top(core_chip=None, verify=True, resume=False, remote=False, floorplan=False):
    chip = setup_top_hier(core_chip)

    chip.set('option', 'clean', not resume)
    chip.set('option', 'breakpoint', floorplan and not remote, step='floorplan')

    run_build(chip, remote)
    if verify:
        run_signoff(chip, 'syn', 'export')

    return chip


def run_build(chip, remote):
    if remote:
        configure_remote(chip)

    chip.run()
    chip.summary()


def run_signoff(chip, netlist_step, layout_step):
    gds_path = chip.find_result('gds', step=layout_step)
    netlist_path = chip.find_result('vg', step=netlist_step)

    jobname = chip.get('option', 'jobname')
    chip.set('option', 'jobname', f'{jobname}_signoff')
    chip.set('option', 'flow', 'signoffflow')

    # Hack: workaround the fact that remote runs alter the steplist
    if chip.get('option', 'remote'):
        chip.set('option', 'steplist', [])

    chip.input(gds_path)
    chip.input(netlist_path)

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
    # parser.add_argument('--fpga',
    #                     action='store_true',
    #                     default=False,
    #                     help='Build FPGA bitstream.')
    parser.add_argument('--core-only',
                        action='store_true',
                        default=False,
                        help='Only build ASIC core GDS.')
    parser.add_argument('--top-only',
                        action='store_true',
                        default=False,
                        help='Only integrate ASIC core into padring. Assumes core already built.')
    parser.add_argument('--top-flat',
                        action='store_true',
                        default=False,
                        help='Build the entire ZeroSoC.')
    parser.add_argument('--floorplan',
                        action='store_true',
                        default=False,
                        help='Break after floorplanning.')
    parser.add_argument('--verify',
                        action='store_true',
                        default=False,
                        help="Run DRC and LVS.")
    parser.add_argument('--remote',
                        action='store_true',
                        default=False,
                        help='Run on remote server. Requires SC remote credentials.')
    parser.add_argument('--clean',
                        action='store_true',
                        default=False,
                        help='Clean previous run.')
    options = parser.parse_args()

    verify = options.verify

    if options.core_only:
        build_core(remote=options.remote,
                   verify=verify,
                   resume=not options.clean,
                   floorplan=options.floorplan)
    elif options.top_only:
        build_top(verify=verify,
                  remote=options.remote,
                  resume=not options.clean,
                  floorplan=options.floorplan)
    elif options.top_flat:
        build_top_flat(verify=verify,
                       remote=options.remote,
                       resume=not options.clean,
                       floorplan=options.floorplan)
    else:
        core_chip = build_core(remote=options.remote,
                               verify=False,
                               resume=not options.clean,
                               floorplan=options.floorplan)
        build_top(core_chip=core_chip,
                  remote=options.remote,
                  verify=verify,
                  resume=not options.clean,
                  floorplan=options.floorplan)


if __name__ == '__main__':
    main()
