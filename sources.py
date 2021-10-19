def add_sources(chip):
    chip.add('define', 'SYNTHESIS')

    # Include dirs
    chip.add('idir', 'opentitan/hw/ip/prim/rtl/')
    chip.add('idir', 'opentitan/hw/dv/sv/dv_utils')

    # SV packages (need to be added explicitly)
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_util_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_secded_pkg.sv')
    chip.add('source', 'opentitan/hw/top_earlgrey/rtl/top_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/tlul/rtl/tlul_pkg.sv')
    chip.add('source', 'hw/xbar_pkg.sv')
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/uart/rtl/uart_reg_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/gpio/rtl/gpio_reg_pkg.sv')
    chip.add('source', 'hw/prim/prim_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/lc_ctrl/rtl/lc_ctrl_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/lc_ctrl/rtl/lc_ctrl_state_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_esc_pkg.sv')
    chip.add('source', 'opentitan/hw/ip/prim/rtl/prim_ram_1p_pkg.sv')

    # Hack to work around Yosys + Surelog issue. Even though this is found in
    # one of our ydirs, we get different synthesis results if this isn't ordered
    # earlier.
    chip.add('source', 'opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_compressed_decoder.sv')

    # TODO: we're overwriting the OpenTitan uart_core, so need to include this
    # module explicitly
    chip.add('source', 'hw/uart_core.sv')

    # Add RTL of all modules we use to search path
    chip.add('ydir', 'hw')
    chip.add('ydir', 'hw/prim')
    chip.add('ydir', 'opentitan/hw/ip/tlul/rtl')
    chip.add('ydir', 'opentitan/hw/ip/rv_core_ibex/rtl')
    chip.add('ydir', 'opentitan/hw/vendor/lowrisc_ibex/rtl')
    chip.add('ydir', 'opentitan/hw/ip/uart/rtl')
    chip.add('ydir', 'opentitan/hw/ip/gpio/rtl')
    chip.add('ydir', 'opentitan/hw/ip/prim/rtl')
    chip.add('ydir', 'opentitan/hw/ip/prim_generic/rtl')
