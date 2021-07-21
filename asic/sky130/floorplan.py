from siliconcompiler.floorplan import snap

def setup_floorplan(fp, chip):
    # TODO: this should be automatically set to a valid value
    fp.db_units = 1000

    # Extract important tech-specific values
    std_cell_w = fp.std_cell_width
    std_cell_h = fp.std_cell_height

    # Initialize die, based on die size for TinyRocket OpenROAD example
    # NOTE: cleaner spec could be as core w/h + coremargin
    core_w = 27000 * std_cell_w
    core_h = 3600 * std_cell_h

    margin_x = 5 * std_cell_w
    margin_y = 5 * std_cell_h

    fp.create_die_area(core_w + 2 * margin_x, core_h + 2 * margin_y,
        core_area=(margin_x, margin_y, core_w + margin_x, core_h + margin_y))

    # Define pads and associated pins
    pins_w = ['clk_i', 'rst_ni', 'uart_rx_i'] + [f'gpio_i[{i}]' for i in range(32)]
    pins_e = ['uart_tx_o', 'uart_tx_en_o'] + [f'{bus}[{i}]' for i in range(32) for bus in ('gpio_o', 'gpio_en_o')]

    # Place pads and pins w/ equal spacing
    # Pins need to be placed directly under pad metal area
    die_w, die_h = fp.die_area

    metal = 'm3'
    width = fp.layers[metal]['width']
    spacing = fp.snap_to_y_track(die_h / (len(pins_w) + 1), metal)
    fp.place_pins(pins_w, spacing, spacing, 'w', width, 5 * width, metal)

    spacing = fp.snap_to_y_track(die_h / (len(pins_e) + 1), metal)
    fp.place_pins(pins_e, spacing, spacing, 'e', width, 5 * width, metal)

#     # Place RAM macros
#     ram_x = snap(0.2 * die_w, std_cell_w)
#     ram_y = snap(0.5 * die_h, std_cell_h)
#     # TODO: find a way to avoid the tech-specific info?
#     row1 = [('ram.u_mem.gen_sky130.u_impl_sky130.mem0', 'ram'),
#             ('ram.u_mem.gen_sky130.u_impl_sky130.mem1', 'ram')]
#     row2 = [('ram.u_mem.gen_sky130.u_impl_sky130.mem2', 'ram'),
#             ('ram.u_mem.gen_sky130.u_impl_sky130.mem3', 'ram')]

#     spacing = snap(200, std_cell_w) + std_cell_w
#     fp.place_macros(row1, (ram_x, ram_y), spacing, 'h', 'N')
#     new_y = ram_y + snap(600, std_cell_h) + std_cell_h
#     fp.place_macros(row2, (ram_x, new_y), spacing, 'h', 'N')

    return fp
