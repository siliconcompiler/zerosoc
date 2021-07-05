from siliconcompiler.floorplan import snap

def setup_floorplan(fp, chip):
    # Extract important tech-specific values
    std_cell_w = fp.std_cell_width
    std_cell_h = fp.std_cell_height
    io_cell_h = fp.available_cells['gpio'].height

    # Initialize die, based on die size for TinyRocket OpenROAD example
    # NOTE: cleaner spec could be as core w/h + coremargin
    core_w = 6000 * std_cell_w
    core_h = 800 * std_cell_h

    fp.create_die_area(core_w + 2 * io_cell_h, core_h + 2 * io_cell_h,
        core_area=(io_cell_h, io_cell_h, core_w + io_cell_h, core_h + io_cell_h))

    # Define pads
    gpio = [('gpio[{i}]', 'gpio') for i in range(32)]
    power = [[(f'vss{i}', 'vss'), (f'vdd{i}', 'vdd'), (f'vddio{i}', 'vddio')] for i in range(4)]
    special = [('clk', 'gpio'), ('rst', 'gpio'), ('uart_rx', 'gpio'), ('uart_tx', 'gpio')]

    pads_w = gpio[:5] + power[0] + special
    pads_n = gpio[5:10] + power[1] + gpio[10:14]
    pads_e = gpio[14:19] + power[2] + gpio[19:23]
    pads_s = gpio[23:28] + power[3] + gpio[28:]

    # Place pads w/ equal spacing
    die_w, die_h = fp.die_area

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_w)
    spacing = (die_h - io_cell_h * 2 - pads_width) / (len(pads_w) + 1)
    fp.place_macros(pads_w, (0, io_cell_h + spacing), spacing, 'v', 'W')

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_n)
    spacing = (die_w - io_cell_h * 2 - pads_width) / (len(pads_n) + 1)
    fp.place_macros(pads_n, (io_cell_h + spacing, die_h - io_cell_h), spacing, 'h', 'N')

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_e)
    spacing = (die_h - io_cell_h * 2 - pads_width) / (len(pads_e) + 1)
    fp.place_macros(pads_e, (die_w - io_cell_h, io_cell_h + spacing), spacing, 'v', 'E')

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_s)
    spacing = (die_w - io_cell_h * 2 - pads_width) / (len(pads_s) + 1)
    fp.place_macros(pads_e, (io_cell_h + spacing, 0), spacing, 'h', 'S')

    # Place corners
    # NOTE: scalar placement functions could be nice
    fp.place_macros([('corner_sw', 'corner')], (0, 0), 0, 'h', 'N')
    fp.place_macros([('corner_nw', 'corner')], (0, die_h - io_cell_h), 0, 'h', 'E')
    fp.place_macros([('corner_se', 'corner')], (die_w - io_cell_h, 0), 0, 'h', 'W')
    fp.place_macros([('corner_ne', 'corner')], (die_w - io_cell_h, die_h - io_cell_h), 0, 'h', 'S')

    # Place RAM macro
    ram_x = snap(0.6 * die_w, std_cell_w)
    ram_y = snap(0.6 * die_h, std_cell_h)
    fp.place_macros([('ram', 'ram')], (ram_x, ram_y), 0, 'h', 'N')

    return fp