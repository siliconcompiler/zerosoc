from siliconcompiler.floorplan import snap

def setup_floorplan(fp, chip):
    # Extract important tech-specific values
    std_cell_w = fp.std_cell_width
    std_cell_h = fp.std_cell_height
    io_cell_h = fp.available_cells['gpio'].height

    # Initialize die, based on die size for TinyRocket OpenROAD example
    # NOTE: cleaner spec could be as core w/h + coremargin
    core_w = 12000 * std_cell_w
    core_h = 1600 * std_cell_h

    fp.create_die_area(core_w + 2 * io_cell_h, core_h + 2 * io_cell_h,
        core_area=(io_cell_h, io_cell_h, core_w + io_cell_h, core_h + io_cell_h))

    # Define pads
    gpio_w = [(f'padring.we_pads\\[0\\].i0.padio\\[{i}\\].i0.iopad', 'gpio') for i in range(9)]
    gpio_n = [(f'padring.no_pads\\[0\\].i0.padio\\[{i}\\].i0.iopad', 'gpio') for i in range(9)]
    gpio_s = [(f'padring.so_pads\\[0\\].i0.padio\\[{i}\\].i0.iopad', 'gpio') for i in range(9)]
    gpio_e = [(f'padring.ea_pads\\[0\\].i0.padio\\[{i}\\].i0.iopad', 'gpio') for i in range(9)]
    power = [[(f'vss{i}', 'vss'), (f'vdd{i}', 'vdd'), (f'vddio{i}', 'vddio')] for i in range(4)]

    pads_w = gpio_w[:5] + power[0] + gpio_w[5:9]
    pads_n = gpio_n[:5] + power[1] + gpio_n[5:9]
    pads_e = gpio_e[:5] + power[2] + gpio_e[5:9]
    pads_s = gpio_s[:5] + power[3] + gpio_s[5:9]

    # Place pads w/ equal spacing
    die_w, die_h = fp.die_area

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_w)
    spacing = (die_h - io_cell_h * 2 - pads_width) / (len(pads_w) + 1)
    fp.place_macros(pads_w, (0, io_cell_h + spacing), spacing, 'v', 'E')

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_n)
    spacing = (die_w - io_cell_h * 2 - pads_width) / (len(pads_n) + 1)
    fp.place_macros(pads_n, (io_cell_h + spacing, die_h - io_cell_h), spacing, 'h', 'S')

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_e)
    spacing = (die_h - io_cell_h * 2 - pads_width) / (len(pads_e) + 1)
    fp.place_macros(pads_e, (die_w - io_cell_h, io_cell_h + spacing), spacing, 'v', 'W')

    pads_width = sum(fp.available_cells[cell].width for _, cell in pads_s)
    spacing = (die_w - io_cell_h * 2 - pads_width) / (len(pads_s) + 1)
    fp.place_macros(pads_s, (io_cell_h + spacing, 0), spacing, 'h', 'N')

    # Place corners
    # NOTE: scalar placement functions could be nice
    fp.place_macros([('corner_sw', 'corner')], (0, 0), 0, 'h', 'N')
    fp.place_macros([('corner_nw', 'corner')], (0, die_h - io_cell_h), 0, 'h', 'E')
    fp.place_macros([('corner_se', 'corner')], (die_w - io_cell_h, 0), 0, 'h', 'W')
    fp.place_macros([('corner_ne', 'corner')], (die_w - io_cell_h, die_h - io_cell_h), 0, 'h', 'S')

    # Place RAM macro
    ram_x = snap(0.6 * die_w, std_cell_w)
    ram_y = snap(0.6 * die_h, std_cell_h)
    # TODO: find a way to avoid the tech-specific info?
    instance = 'soc.ram.u_mem.gen_freepdk45.u_impl_freepdk45.mem'
    fp.place_macros([(instance, 'ram')], (ram_x, ram_y), 0, 'h', 'N')

    return fp
