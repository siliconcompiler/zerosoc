#!/usr/bin/env python3
'''
ZeroSOC build system
'''

from siliconcompiler import DesignSchema, Project, ASICProject
from siliconcompiler.flows import lintflow
from lambdalib.ramlib import Spram
from lambdalib.padring import Padring

import argparse
import os
import sys

# # Libraries
# from lambdapdk.sky130.libs import sky130sram, sky130io
from siliconcompiler.targets import skywater130_demo

# from siliconcompiler.tools.openroad import openroad
# from siliconcompiler.tools._common import get_tool_tasks as _get_tool_tasks

# import floorplan as zerosoc_floorplan
# import zerosoc_core
# import zerosoc_top

ASIC_CORE_CFG = 'zerosoc_core.pkg.json'


from siliconcompiler.flows.asicflow import SV2VASICFlow
from siliconcompiler.tools.openroad.init_floorplan import InitFloorplanTask
from siliconcompiler.tools.openroad._apr import OpenROADPSMParameter
from siliconcompiler.tools.openroad._apr import APRTask
from siliconcompiler.tools.openroad.power_grid import PowerGridTask



class OpenTITAN(DesignSchema):
    def __init__(self):
        super().__init__("opentitan")

        self.set_dataroot("opentitan",
                          'git+https://github.com/lowRISC/opentitan.git',
                          tag='8b9fe4bf2db8ccfac0b26600decf07cf41867e07')

        with self.active_dataroot("opentitan"), self.active_fileset("rtl"):
            self.add_idir("hw/ip/prim/rtl")
            self.add_idir("hw/dv/sv/dv_utils")

            # SV packages (need to be added explicitly)
            self.add_file('hw/top_earlgrey/rtl/top_pkg.sv')

            self.add_file('hw/ip/gpio/rtl/gpio_reg_pkg.sv')
            self.add_file('hw/ip/gpio/rtl/gpio_reg_top.sv')
            self.add_file('hw/ip/gpio/rtl/gpio.sv')

            self.add_file('hw/ip/uart/rtl/uart_reg_pkg.sv')
            self.add_file('hw/ip/uart/rtl/uart_reg_top.sv')
            self.add_file('hw/ip/uart/rtl/uart_rx.sv')
            self.add_file('hw/ip/uart/rtl/uart_tx.sv')
            self.add_file('hw/ip/uart/rtl/uart.sv')

            self.add_file('hw/ip/prim/rtl/prim_alert_pkg.sv')
            self.add_file('hw/ip/prim/rtl/prim_secded_pkg.sv')
            self.add_file('hw/ip/prim/rtl/prim_esc_pkg.sv')
            self.add_file('hw/ip/prim/rtl/prim_otp_pkg.sv')
            self.add_file('hw/ip/prim/rtl/prim_pad_wrapper_pkg.sv')
            self.add_file('hw/ip/prim/rtl/prim_ram_1p_pkg.sv')
            self.add_file('hw/ip/prim/rtl/prim_ram_2p_pkg.sv')
            self.add_file('hw/ip/prim/rtl/prim_rom_pkg.sv')
            self.add_file('hw/ip/prim/rtl/prim_subreg_arb.sv')
            self.add_file('hw/ip/prim/rtl/prim_subreg.sv')
            self.add_file('hw/ip/prim/rtl/prim_subreg_ext.sv')
            self.add_file('hw/ip/prim/rtl/prim_subreg_shadow.sv')
            self.add_file('hw/ip/prim/rtl/prim_intr_hw.sv')
            self.add_file('hw/ip/prim/rtl/prim_fifo_sync.sv')
            self.add_file('hw/ip/prim/rtl/prim_filter_ctr.sv')
            self.add_file('hw/ip/prim/rtl/prim_ram_1p_adv.sv')
            self.add_file('hw/ip/prim/rtl/prim_secded_64_57_dec.sv')
            self.add_file('hw/ip/prim/rtl/prim_secded_64_57_enc.sv')
            self.add_file('hw/ip/prim/rtl/prim_arbiter_ppc.sv')
            self.add_file('hw/ip/prim/rtl/prim_lc_sync.sv')
            self.add_file('hw/ip/prim/rtl/prim_esc_receiver.sv')
            self.add_file('hw/ip/prim/rtl/prim_diff_decode.sv')

            self.add_file('hw/ip/prim_generic/rtl/prim_generic_flop_2sync.sv')
            self.add_file('hw/ip/prim_generic/rtl/prim_generic_flop.sv')
            self.add_file('hw/ip/prim_generic/rtl/prim_generic_buf.sv')

            self.add_file('hw/ip/tlul/rtl/tlul_pkg.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_adapter_sram.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_socket_1n.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_socket_m1.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_cmd_intg_chk.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_rsp_intg_gen.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_adapter_reg.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_fifo_sync.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_err.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_err_resp.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_adapter_host.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_cmd_intg_gen.sv')
            self.add_file('hw/ip/tlul/rtl/tlul_rsp_intg_chk.sv')

            self.add_file('hw/ip/prim/rtl/prim_util_pkg.sv')
            self.add_file('hw/ip/prim/rtl/prim_secded_pkg.sv')

            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_pkg.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_top.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_core.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_cs_registers.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_register_file_latch.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_wb_stage.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_load_store_unit.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_ex_block.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_id_stage.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_if_stage.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_prefetch_buffer.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_fetch_fifo.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_csr.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_counter.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_controller.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_decoder.sv')
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_alu.sv')

            self.add_file('hw/ip/lc_ctrl/rtl/lc_ctrl_state_pkg.sv')
            self.add_file('hw/ip/lc_ctrl/rtl/lc_ctrl_pkg.sv')

            self.add_file("hw/ip/rv_core_ibex/rtl/rv_core_ibex.sv")

            # Hack to work around Yosys + Surelog issue. Even though this is found in
            # one of our ydirs, we get different synthesis results if this isn't ordered
            # earlier.
            self.add_file('hw/vendor/lowrisc_ibex/rtl/ibex_compressed_decoder.sv')


class ZeroSOC(DesignSchema):
    def __init__(self):
        super().__init__("zerosoc")

        self.set_dataroot("zerosoc", __file__)

        with self.active_dataroot("zerosoc"), self.active_fileset("rtl.core"):
            self.set_topmodule("asic_core")
            self.add_idir("hw")
            self.add_file("hw/xbar_pkg.sv")
            self.add_file("hw/prim/prim_pkg.sv")
            self.add_file("hw/uart_core.sv")
            self.add_file("hw/zerosoc.sv")
            self.add_file("hw/xbar.sv")
            self.add_file("hw/tl_dbg.sv")
            self.add_file("hw/asic_core.v")
            self.add_file("hw/xbar.sv")
            self.add_file("hw/xbar.sv")
            self.add_file('hw/prim/lambdalib/prim_lambdalib_ram_1p.v')
            self.add_file('hw/prim/lambdalib/prim_lambdalib_clock_gating.v')
            self.add_file('hw/prim/prim_flop_2sync.sv')
            self.add_file('hw/prim/prim_ram_1p.sv')
            self.add_file('hw/prim/prim_flop.sv')
            self.add_file('hw/prim/prim_clock_gating.sv')
            self.add_file('hw/prim/prim_buf.sv')

            self.add_define('PRIM_DEFAULT_IMPL=prim_pkg::ImplLambdalib')
            self.add_define('RAM_DEPTH=512')
            self.add_define(f'MEM_ROOT={self.get_dataroot("zerosoc")}')
            self.add_define('SYNTHESIS')

            self.add_depfileset(Spram(), "rtl")
            self.add_depfileset(OpenTITAN(), "rtl")

        with self.active_dataroot("zerosoc"), self.active_fileset("rtl.top"):
            self.set_topmodule("asic_top")
            self.add_file("hw/asic_top.v")
            self.add_depfileset(self, "rtl.core")
            self.add_depfileset(Padring(), "rtl")

        with self.active_dataroot("zerosoc"), self.active_fileset("padring.sky130"):
            self.add_file("openroad/padring.tcl")

        with self.active_dataroot("zerosoc"), self.active_fileset("globalconns.flattop"):
            self.add_file("openroad/global_connect_core_top_flat.tcl")
            self.add_file("openroad/global_connect_io.tcl")

        with self.active_dataroot("zerosoc"), self.active_fileset("pdn.flattop"):
            self.add_file("openroad/pdngen_top.tcl")
            self.add_file("openroad/pdngen_sram.tcl")

        with self.active_dataroot("zerosoc"), self.active_fileset("sdc.top.sky130"):
            self.add_file("hw/asic_top.sdc")


def build_fpga():
    chip = siliconcompiler.Chip('top_icebreaker')

    chip.set('fpga', 'partname', 'ice40up5k-sg48')
    chip.use(fpgaflow_demo, partname='ice40up5k-sg48')

    chip.use(zerosoc_core)

    chip.input('hw/top_icebreaker.v', package='zerosoc')
    chip.input('hw/prim/ice40/prim_ice40_clock_gating.v', package='zerosoc')
    chip.input('fpga/icebreaker.pcf', package='zerosoc')

    chip.add('option', 'define', 'PRIM_DEFAULT_IMPL="prim_pkg::ImplIce40"')

    _run_build(chip)


def _setup_core():
    chip = siliconcompiler.Chip('zerosoc_core')
    chip.set('option', 'entrypoint', 'asic_core')

    chip.use(skywater130_demo)

    chip.add('option', 'define', 'SYNTHESIS')
    chip.use(zerosoc_core)

    chip.use(sky130sram)
    chip.swap_library('lambdalib_ramlib', 'lambdalib_sky130sram')

    # Ignore cells in these libraries during DRC, they violate the rules but are
    # foundry-validated
    for task in ('extspice', 'drc'):
        chip.add('tool', 'magic', 'task', task, 'var', 'exclude', 'sky130_sram_1rw1r_64x256_8')
    chip.add('tool', 'netgen', 'task', 'lvs', 'var', 'exclude', 'sky130_sram_1rw1r_64x256_8')

    chip.set('tool', 'openroad', 'task', 'write_data', 'var',
             'ord_abstract_lef_bloat_layers', False)

    chip.clock(r'we_din\[5\]', period=66)

    chip.set('tool', 'openroad', 'task', 'macro_placement', 'var', 'rtlmp_enable', 'true')
    chip.set('tool', 'openroad', 'task', 'write_data', 'var', 'write_cdl', 'false')
    chip.set('option', 'var', 'openroad_place_density', '0.40')
    chip.set('option', 'var', 'openroad_grt_macro_extension', '0')

    zerosoc_floorplan.generate_core_floorplan(chip)

    return chip


def _setup_core_module(chip):
    # set up pointers to final outputs for integration
    # Set physical outputs
    stackup = chip.get('option', 'stackup')
    chip.set('output', stackup, 'gds', chip.find_result('gds', step='write.gds'))
    chip.set('output', stackup, 'lef', chip.find_result('lef', step='write.views'))

    # Set output netlist
    chip.set('output', 'netlist', 'verilog', chip.find_result('vg', step='write.views'))

    # Set timing libraries
    for scenario in chip.getkeys('constraint', 'timing'):
        corner = chip.get('constraint', 'timing', scenario, 'libcorner')[0]
        lib = chip.find_result(f'{corner}.lib', step='write.views')
        chip.set('output', corner, 'nldm', lib)

    # Set pex outputs
    for scenario in chip.getkeys('constraint', 'timing'):
        corner = chip.get('constraint', 'timing', scenario, 'pexcorner')
        spef = chip.find_result(f'{corner}.spef', step='write.views')
        chip.set('output', corner, 'spef', spef)

    # Hash output files
    for fileset in chip.getkeys('output'):
        for filetype in chip.getkeys('output', fileset):
            chip.hash_files('output', fileset, filetype)

    chip.write_manifest(ASIC_CORE_CFG)


def build_core(verify=True, remote=False, resume=False, floorplan=False):
    chip = _setup_core()
    chip.set('option', 'clean', not resume)
    chip.set('option', 'breakpoint', floorplan and not remote, step='floorplan')

    _run_build(chip, remote)

    if verify:
        _run_signoff(chip, 'write.views', 'write.gds', remote)

    _setup_core_module(chip)

    return chip


def _setup_top_flat():
    chip = siliconcompiler.Chip('zerosoc')
    chip.set('option', 'entrypoint', 'asic_top')

    chip.use(skywater130_demo)
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
    chip.set('tool', 'openroad', 'task', 'macro_placement', 'var', 'rtlmp_enable', 'true')
    chip.set('option', 'var', 'openroad_grt_macro_extension', '0')
    for task in _get_tool_tasks(chip, openroad):
        chip.add('tool', 'openroad', 'task', task, 'var', 'psm_skip_nets', 'ioring*')
        chip.add('tool', 'openroad', 'task', task, 'var', 'psm_skip_nets', 'v*io')

    chip.set('tool', 'yosys', 'task', 'syn_asic', 'var', 'hierarchy_separator', '.')
    chip.clock(r'padring.iwest.ipad\[3\].gbidir.i0.gpio/IN', period=60)

    zerosoc_floorplan.generate_top_flat_floorplan(chip)

    return chip


def _setup_top_hier(core_chip):
    chip = siliconcompiler.Chip('zerosoc_top')

    if not core_chip:
        if not os.path.exists(ASIC_CORE_CFG):
            print(f"'{ASIC_CORE_CFG}' has not been generated.", file=sys.stderr)
            return
        core_chip = siliconcompiler.Library('zerosoc_core')
        core_chip.read_manifest(ASIC_CORE_CFG)
    core_chip.set('design', 'asic_zerosoc_core')

    chip = siliconcompiler.Chip('zerosoc_top')
    chip.set('option', 'entrypoint', 'asic_top')

    chip.use(skywater130_demo)
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
    chip.set('option', 'var', 'openroad_grt_macro_extension', 0)

    for met, adj in (('met2', 0.2),
                     ('met3', 0.1),
                     ('met4', 0.1),
                     ('met5', 0.1)):
        chip.set('pdk', 'skywater130', 'var', 'openroad', f'{met}_adjustment', '5M1LI', str(adj))

    for task in _get_tool_tasks(chip, openroad):
        chip.add('tool', 'openroad', 'task', task, 'var', 'psm_skip_nets', 'ioring*')
        chip.add('tool', 'openroad', 'task', task, 'var', 'psm_skip_nets', 'v*io')
    chip.set('tool', 'yosys', 'task', 'syn_asic', 'var', 'hierarchy_separator', '.')

    zerosoc_floorplan.generate_top_floorplan(chip)

    return chip


def build_top_flat(resume=True, remote=False, floorplan=False):
    project = ASICProject(ZeroSOC())
    project.add_fileset("rtl.top")
    project.add_fileset("sdc.top.sky130")

    project.load_target(skywater130_demo.setup)
    project.set_flow(SV2VASICFlow())

    init_fp: InitFloorplanTask = project.get_task(filter=InitFloorplanTask)
    init_fp.add_openroad_padringfileset("padring.sky130")

    for task in project.get_task(filter=APRTask):
        task.add_openroad_globalconnectfileset("zerosoc", "globalconns.flattop")

    project.get_task(filter=PowerGridTask).add_openroad_powergridfileset("zerosoc", "pdn.flattop")

    for task in project.get_task(filter=OpenROADPSMParameter):
        task.add("var", "psm_skip_nets", 'ioring*')
        task.add("var", "psm_skip_nets", 'v*io')

    project.get_areaconstraints().set_diearea_rectangle(1700, 2300, coremargin=230)
    # chip = _setup_top_flat()

    project.set('option', 'clean', not resume)

    project.set('option', 'breakpoint', floorplan and not remote, step='floorplan')

    project.run()
    project.summary()

    return project


def build_top(core_chip=None, verify=True, resume=False, remote=False, floorplan=False):
    chip = _setup_top_hier(core_chip)

    chip.set('option', 'clean', not resume)
    chip.set('option', 'breakpoint', floorplan and not remote, step='floorplan')

    _run_build(chip, remote)
    if verify:
        _run_signoff(chip, 'write.views', 'write.gds', remote)

    return chip


def _run_build(chip, remote):
    if remote:
        _configure_remote(chip)

    chip.run()
    chip.summary()


def _run_signoff(chip, netlist_step, layout_step, remote):
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

    _run_build(chip, remote)


def _main():
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
        build_top_flat(remote=options.remote,
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
    project = Project(ZeroSOC())
    project.add_fileset("rtl.top")
    project.set_flow(lintflow.LintFlow())

    assert project.check_filepaths()
    project.run()


    # _main()
