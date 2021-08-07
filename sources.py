def add_sources(chip):
    chip.add('idir', 'opentitan/hw/ip/prim/rtl/')
    chip.add('idir', 'opentitan/hw/dv/sv/dv_utils')

    chip.add('define', 'SYNTHESIS')

    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_assert.sv')

    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_secded_pkg.sv')
    chip.add('source', 'opentitan/hw/top_earlgrey/rtl/top_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_pkg.sv')
    chip.add('source', 'hw/xbar_pkg.sv')

    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_adapter_sram.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_err.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_rsp_intg_gen.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_fifo_sync.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_adapter_host.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_rsp_intg_chk.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_cmd_intg_gen.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_cmd_intg_chk.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_adapter_reg.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_socket_m1.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_socket_1n.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_err_resp.sv')

    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/rv_core_ibex/rtl/rv_core_ibex.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_top.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_alu.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_compressed_decoder.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_csr.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_controller.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_counter.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_cs_registers.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_decoder.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_ex_block.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_fetch_fifo.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_id_stage.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_if_stage.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_load_store_unit.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_multdiv_fast.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_prefetch_buffer.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_pmp.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_register_file_ff.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_register_file_fpga.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_core.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_wb_stage.sv')

    chip.add('source', 'opentitan/hw/ip/uart/rtl/uart_reg_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/uart/rtl/uart_reg_top.sv')
    chip.add('source', 'opentitan/hw/ip/uart/rtl/uart_rx.sv')
    chip.add('source', 'opentitan/hw/ip/uart/rtl/uart_tx.sv')
    # TODO: upstream changes and switch back to OpenTitan UART
    chip.add('source', 'hw/uart_core.sv')
    chip.add('source', 'opentitan/hw/ip/uart/rtl/uart.sv')

    chip.add('source', 'opentitan/hw/ip/gpio/rtl/gpio_reg_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/gpio/rtl/gpio_reg_top.sv')
    chip.add('source', 'opentitan/hw/ip/gpio/rtl/gpio.sv')

    chip.add('source', 'opentitan/hw/ip/lc_ctrl/rtl/lc_ctrl_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/lc_ctrl/rtl/lc_ctrl_state_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_util_pkg.sv')
    chip.add('source', 'hw/prim/prim_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_esc_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_ram_1p_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_subreg_arb.sv')

    chip.add('source', 'hw/prim/prim_ram_1p.sv')
    chip.add('source', 'hw/prim/prim_flop_2sync.sv')
    chip.add('source', 'hw/prim/prim_buf.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_fifo_sync.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_secded_64_57_enc.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_secded_64_57_dec.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_lc_sync.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_esc_receiver.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_diff_decode.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_intr_hw.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_subreg.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_subreg_ext.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_filter_ctr.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_arbiter_ppc.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_ram_1p_adv.sv')
    chip.add('source', 'hw/prim/prim_flop.sv')
    chip.add('source', 'hw/prim/prim_clock_gating.sv')
    chip.add('source', 'opentitan/hw/ip/prim_generic/rtl/prim_generic_flop_2sync.sv')
    chip.add('source', 'opentitan/hw/ip/prim_generic/rtl/prim_generic_clock_gating.sv')
    chip.add('source', 'opentitan/hw/ip/prim_generic/rtl/prim_generic_ram_1p.sv')
    chip.add('source', 'opentitan/hw/ip/prim_generic/rtl/prim_generic_buf.sv')
    chip.add('source', 'opentitan/hw/ip/prim_generic/rtl/prim_generic_flop.sv')
    chip.add('source', 'hw/SB_HFOSC.v')

    chip.add('source', 'hw/tl_dbg.sv')
    chip.add('source', 'hw/xbar.sv')
    chip.add('source', 'hw/zerosoc.sv')
