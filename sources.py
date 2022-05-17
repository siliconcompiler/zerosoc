def add_sources(chip):
    chip.add('option', 'define', 'SYNTHESIS')

    # Include dirs
    chip.add('option', 'idir', 'opentitan/hw/ip/prim/rtl/')
    chip.add('option', 'idir', 'opentitan/hw/dv/sv/dv_utils')

    # Workaround for new import collection scheme. Since we now rename collected
    # source files, Surelog errors out due to a conflict between collected pkg
    # files and the same pkgs found in the ydirs. I think before it would ignore
    # files in the ydir with the same names as ones passed in directly as
    # sources. To avoid this issue for now, we disable collecting the source
    # files by unsetting the 'copy' flag. This doesn't cause any problems since
    # we run import locally anyways.
    chip.set('input', 'verilog', False, field='copy')

    # SV packages (need to be added explicitly)
    chip.add('input', 'verilog', 'opentitan/hw/ip/prim/rtl/prim_util_pkg.sv')
    chip.add('input', 'verilog', 'opentitan/hw/ip/prim/rtl/prim_secded_pkg.sv')
    chip.add('input', 'verilog', 'opentitan/hw/top_earlgrey/rtl/top_pkg.sv')
    chip.add('input', 'verilog', 'opentitan/hw/ip/tlul/rtl/tlul_pkg.sv')
    chip.add('input', 'verilog', 'hw/xbar_pkg.sv')
    chip.add('input', 'verilog', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_pkg.sv')
    chip.add('input', 'verilog', 'opentitan/hw/ip/uart/rtl/uart_reg_pkg.sv')
    chip.add('input', 'verilog', 'opentitan/hw/ip/gpio/rtl/gpio_reg_pkg.sv')
    chip.add('input', 'verilog', 'hw/prim/prim_pkg.sv')
    chip.add('input', 'verilog', 'opentitan/hw/ip/lc_ctrl/rtl/lc_ctrl_pkg.sv')
    chip.add('input', 'verilog', 'opentitan/hw/ip/lc_ctrl/rtl/lc_ctrl_state_pkg.sv')
    chip.add('input', 'verilog', 'opentitan/hw/ip/prim/rtl/prim_esc_pkg.sv')
    chip.add('input', 'verilog', 'opentitan/hw/ip/prim/rtl/prim_ram_1p_pkg.sv')

    # Hack to work around Yosys + Surelog issue. Even though this is found in
    # one of our ydirs, we get different synthesis results if this isn't ordered
    # earlier.
    chip.add('input', 'verilog', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_compressed_decoder.sv')

    # TODO: we're overwriting the OpenTitan uart_core, so need to include this
    # module explicitly
    chip.add('input', 'verilog', 'hw/uart_core.sv')

    chip.add('input', 'verilog', 'hw/zerosoc.sv')
    chip.add('input', 'verilog', 'hw/xbar.sv')
    chip.add('input', 'verilog', 'hw/tl_dbg.sv')

    # Add RTL of all modules we use to search path
    chip.add('option', 'ydir', 'hw/prim')
    chip.add('option', 'ydir', 'opentitan/hw/ip/tlul/rtl')
    chip.add('option', 'ydir', 'opentitan/hw/ip/rv_core_ibex/rtl')
    chip.add('option', 'ydir', 'opentitan/hw/vendor/lowrisc_ibex/rtl')
    chip.add('option', 'ydir', 'opentitan/hw/ip/uart/rtl')
    chip.add('option', 'ydir', 'opentitan/hw/ip/gpio/rtl')
    chip.add('option', 'ydir', 'opentitan/hw/ip/prim/rtl')
    chip.add('option', 'ydir', 'opentitan/hw/ip/prim_generic/rtl')
