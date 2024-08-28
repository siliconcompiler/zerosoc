from siliconcompiler import Library


def setup():
    lib = Library("opentitan", package='opentitan', auto_enable=True)
    lib.register_source(
        name='opentitan',
        path='git+https://github.com/lowRISC/opentitan.git',
        ref='8b9fe4bf2db8ccfac0b26600decf07cf41867e07')

    # Include dirs
    lib.add('option', 'idir', 'hw/ip/prim/rtl')
    lib.add('option', 'idir', 'hw/dv/sv/dv_utils')

    # Add RTL of all modules we use to search path
    lib.add('option', 'ydir', 'hw/ip/tlul/rtl')
    lib.add('option', 'ydir', 'hw/ip/rv_core_ibex/rtl')
    lib.add('option', 'ydir', 'hw/ip/uart/rtl')
    lib.add('option', 'ydir', 'hw/ip/gpio/rtl')
    lib.add('option', 'ydir', 'hw/ip/prim/rtl')
    lib.add('option', 'ydir', 'hw/ip/prim_generic/rtl')

    # SV packages (need to be added explicitly)
    lib.input('hw/top_earlgrey/rtl/top_pkg.sv')

    lib.input('hw/ip/gpio/rtl/gpio_reg_pkg.sv')
    lib.input('hw/ip/uart/rtl/uart_reg_pkg.sv')
    lib.input('hw/ip/prim/rtl/prim_alert_pkg.sv')
    lib.input('hw/ip/prim/rtl/prim_esc_pkg.sv')
    lib.input('hw/ip/prim/rtl/prim_otp_pkg.sv')
    lib.input('hw/ip/prim/rtl/prim_pad_wrapper_pkg.sv')
    lib.input('hw/ip/prim/rtl/prim_ram_1p_pkg.sv')
    lib.input('hw/ip/prim/rtl/prim_ram_2p_pkg.sv')
    lib.input('hw/ip/prim/rtl/prim_rom_pkg.sv')
    lib.input('hw/ip/tlul/rtl/tlul_pkg.sv')

    lib.input('hw/ip/prim/rtl/prim_util_pkg.sv')
    lib.input('hw/ip/prim/rtl/prim_secded_pkg.sv')

    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_pkg.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_top.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_core.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_cs_registers.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_register_file_latch.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_wb_stage.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_load_store_unit.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_ex_block.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_id_stage.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_if_stage.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_prefetch_buffer.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_fetch_fifo.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_csr.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_counter.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_controller.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_decoder.sv')
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_alu.sv')

    lib.input('hw/ip/lc_ctrl/rtl/lc_ctrl_state_pkg.sv')
    lib.input('hw/ip/lc_ctrl/rtl/lc_ctrl_pkg.sv')

    # Hack to work around Yosys + Surelog issue. Even though this is found in
    # one of our ydirs, we get different synthesis results if this isn't ordered
    # earlier.
    lib.input('hw/vendor/lowrisc_ibex/rtl/ibex_compressed_decoder.sv')

    return lib
