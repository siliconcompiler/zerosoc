from siliconcompiler.floorplan import snap

def setup_floorplan(fp, chip):
    # TODO: this should be automatically set to a valid value
    fp.db_units = 1000

    # Extract important tech-specific values
    std_cell_w = fp.std_cell_width
    std_cell_h = fp.std_cell_height

    # Initialize die, based on die size for TinyRocket OpenROAD example
    # NOTE: cleaner spec could be as core w/h + coremargin
    die_w = 6750 * std_cell_w
    die_h = 900 * std_cell_h
    margin_x = 5 * std_cell_w
    margin_y = 5 * std_cell_h

    ram_x = snap(0.7 * die_w, std_cell_w)
    ram_y = snap(0.7 * die_h, std_cell_h)

    fp.create_die_area(die_w, die_h,
        core_area=(margin_x, margin_y, ram_x - 50 * margin_x, die_h - margin_y))

    # Define pads and associated pins
    pins_w = ['clk_i', 'rst_ni', 'uart_rx_i'] + [f'gpio_i[{i}]' for i in range(32)]
    pins_e = ['uart_tx_o', 'uart_tx_en_o'] + [f'{bus}[{i}]' for i in range(32) for bus in ('gpio_o', 'gpio_en_o')]

    # Place pads and pins w/ equal spacing
    # Pins need to be placed directly under pad metal area
    die_w, die_h = fp.die_area

    metal = chip.get('asic', 'hpinlayer')[-1]
    width = fp.layers[metal]['width']
    spacing = fp.snap_to_y_track(die_h / (len(pins_w) + 1), metal)
    fp.place_pins(pins_w, spacing, spacing, 'w', width, 5 * width, metal)

    spacing = fp.snap_to_y_track(die_h / (len(pins_e) + 1), metal)
    fp.place_pins(pins_e, spacing, spacing, 'e', width, 5 * width, metal)

    fp.place_macros([('ram.u_mem.gen_sky130.u_impl_sky130.mem', 'ram')], (ram_x, ram_y), 0, 'h', 'N')

    return fp
