#!/usr/bin/env python3
'''
ZeroSOC build system
'''

import argparse

# Libraries
from siliconcompiler.targets import skywater130_demo

from siliconcompiler import Design, ASIC
from lambdalib.ramlib import Spram
from lambdalib.padring import Padring


from siliconcompiler.tools.yosys.syn_asic import ASICSynthesis
from siliconcompiler.tools.openroad.init_floorplan import InitFloorplanTask
from siliconcompiler.tools.openroad._apr import OpenROADPSMParameter
from siliconcompiler.tools.openroad._apr import APRTask
from siliconcompiler.tools.openroad.power_grid import PowerGridTask


ASIC_CORE_CFG = 'zerosoc_core.pkg.json'


class OpenTITAN(Design):
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


class ZeroSOC(Design):
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


def build_top_flat(resume=True, remote=False, floorplan=False):
    project = ASIC(ZeroSOC())
    project.add_fileset("rtl.top")
    project.add_fileset("sdc.top.sky130")

    skywater130_demo(project)

    ASICSynthesis.find_task(project).set_yosys_useslang(True)

    InitFloorplanTask.find_task(project).add_openroad_padringfileset("padring.sky130")

    for task in APRTask.find_task(project):
        task.add_openroad_globalconnectfileset("zerosoc", "globalconns.flattop")

    PowerGridTask.find_task(project).add_openroad_powergridfileset("zerosoc", "pdn.flattop")

    for task in OpenROADPSMParameter.find_task(project):
        task.add_openroad_psmskipnets('ioring*')
        task.add_openroad_psmskipnets('v*io')

    project.constraint.area.set_diearea_rectangle(1700, 2300, coremargin=230)

    project.option.set_clean(not resume)
    project.option.set_breakpoint(floorplan and not remote, step='floorplan.init')

    project.run()
    project.summary()

    return project


def _main():
    parser = argparse.ArgumentParser(description='Build ZeroSoC')
    parser.add_argument('--floorplan',
                        action='store_true',
                        default=False,
                        help='Break after floorplanning.')
    parser.add_argument('--remote',
                        action='store_true',
                        default=False,
                        help='Run on remote server. Requires SC remote credentials.')
    parser.add_argument('--clean',
                        action='store_true',
                        default=False,
                        help='Clean previous run.')
    options = parser.parse_args()

    build_top_flat(remote=options.remote,
                   resume=not options.clean,
                   floorplan=options.floorplan)


if __name__ == '__main__':
    _main()
