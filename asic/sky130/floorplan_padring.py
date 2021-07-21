from siliconcompiler.floorplan import snap

def setup_floorplan(fp, chip):
    # TODO: this should be automatically set to a valid value
    fp.db_units = 1000

    # Extract important tech-specific values
    std_cell_w = fp.std_cell_width
    std_cell_h = fp.std_cell_height

    # gpio cell is tallest in Sky130 io lib (should we validate this?)
    gpio_cell_w = fp.available_cells['gpio'].width
    gpio_cell_h = fp.available_cells['gpio'].height
    pow_cell_h = fp.available_cells['vdd'].height
    corner_w = fp.available_cells['corner'].width
    corner_h = fp.available_cells['corner'].height
    max_io_cell_h = max(gpio_cell_h, pow_cell_h)

    # Initialize die, based on die size for TinyRocket OpenROAD example
    # NOTE: cleaner spec could be as core w/h + coremargin
    core_w = 18000 * std_cell_w
    core_h = 2400 * std_cell_h

    # add one of each in case we round down
    margin_x = snap(max_io_cell_h, std_cell_w) + std_cell_w
    margin_y = snap(max_io_cell_h, std_cell_h) + std_cell_h

    fp.create_die_area(core_w + 2 * margin_x, core_h + 2 * margin_y,
        core_area=(margin_x, margin_y, core_w + margin_x, core_h + margin_y))

    # Define pads and associated pins
    gpio_w = [(f'padring.we_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio', 'gpio') for i in range(9)]
    gpio_pins_w = [f'we_pad[{i}]' for i in range(9)]
    gpio_n = [(f'padring.no_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio', 'gpio') for i in range(9)]
    gpio_pins_n = [f'no_pad[{i}]' for i in range(9)]
    gpio_s = [(f'padring.so_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio', 'gpio') for i in range(9)]
    gpio_pins_s = [f'so_pad[{i}]' for i in range(9)]
    gpio_e = [(f'padring.ea_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio', 'gpio') for i in range(9)]
    gpio_pins_e = [f'ea_pad[{i}]' for i in range(9)]
    power = [[(f'vdd{i}', 'vdd'), (f'vss{i}', 'vss'), (f'vddio{i}', 'vddio'), (f'vssio{i}', 'vssio')] for i in range(4)]
    power_pins = [['vdd', 'vss', f'{side}_vddio', f'{side}_vssio'] for side in ('we', 'no', 'so', 'ea')]

    pads_w = gpio_w[:5] + power[0] + gpio_w[5:9]
    pins_w = gpio_pins_w[:5] + power_pins[0] + gpio_pins_w[5:9]
    pads_n = gpio_n[:5] + power[1] + gpio_n[5:9]
    pins_n = gpio_pins_n[:5] + power_pins[1] + gpio_pins_n[5:9]
    pads_e = gpio_e[:5] + power[2] + gpio_e[5:9]
    pins_e = gpio_pins_e[:5] + power_pins[2] + gpio_pins_e[5:9]
    pads_s = gpio_s[:5] + power[3] + gpio_s[5:9]
    pins_s = gpio_pins_s[:5] + power_pins[3] + gpio_pins_s[5:9]

    # Place pads and pins w/ equal spacing
    # Pins need to be placed directly under pad metal area
    die_w, die_h = fp.die_area

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_w)

    # Assuming all pads have same width
    pad_w = pads_width // len(pads_w)

    spacing = (die_h - corner_w - corner_h - pads_width) / (len(pads_w) + 1)
    fp.place_macros(pads_w, (0, corner_h + spacing), spacing, 'v', 'W')
    # fp.place_pins(pins_w, corner_h + spacing + pad_w/2, spacing + pad_w, 'w', 10, 100, 'm3')

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_n)
    spacing = (die_w - corner_w - corner_h - pads_width) / (len(pads_n) + 1)
    fp.place_macros(pads_n[:5], (corner_h + spacing, die_h - gpio_cell_h), spacing, 'h', 'N')
    fp.place_macros(pads_n[5:9], (corner_h + 6 * spacing + 5 * gpio_cell_w, die_h - pow_cell_h), spacing, 'h', 'N')
    fp.place_macros(pads_n[9:], (corner_h + 6 * spacing + 5 * gpio_cell_w, die_h - gpio_cell_h), spacing, 'h', 'N')
    # fp.place_pins(pins_n, io_cell_h + spacing + pad_w/2, spacing + pad_w, 'n', 10, 100, 'm3')

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_e)
    spacing = (die_h - io_cell_h * 2 - pads_width) / (len(pads_e) + 1)
    fp.place_macros(pads_e, (die_w - io_cell_h, io_cell_h + spacing), spacing, 'v', 'E')
    # fp.place_pins(pins_e, io_cell_h + spacing + pad_w/2, spacing + pad_w, 'e', 10, 100, 'm3')

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_s)
    spacing = (die_w - io_cell_h * 2 - pads_width) / (len(pads_s) + 1)
    fp.place_macros(pads_s, (io_cell_h + spacing, 0), spacing, 'h', 'S')
    # fp.place_pins(pins_s, io_cell_h + spacing + pad_w/2, spacing + pad_w, 's', 10, 100, 'm3')

    # Place corners
    # NOTE: scalar placement functions could be nice
    fp.place_macros([('corner_sw', 'corner')], (0, 0), 0, 'h', 'S')
    fp.place_macros([('corner_nw', 'corner')], (0, die_h - io_cell_h), 0, 'h', 'W')
    fp.place_macros([('corner_se', 'corner')], (die_w - io_cell_h, 0), 0, 'h', 'E')
    fp.place_macros([('corner_ne', 'corner')], (die_w - io_cell_h, die_h - io_cell_h), 0, 'h', 'N')

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
