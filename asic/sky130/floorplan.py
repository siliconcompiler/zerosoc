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
    max_io_cell_h = max(gpio_cell_h, pow_cell_h, corner_w, corner_h)

    # Initialize die
    margin = 4 * max_io_cell_h

    die_w = 6750 * std_cell_w + 2 * margin
    die_h = 900 * std_cell_h + 2 * margin
    ram_core_space = 250 * std_cell_w

    ram_w = fp.available_cells['ram'].width
    ram_h = fp.available_cells['ram'].height
    ram_x = fp.snap(die_w - margin - ram_w - ram_core_space, std_cell_w)
    ram_y = fp.snap(die_h - margin - ram_h - 50 * std_cell_h, std_cell_h)

    fp.create_die_area(die_w, die_h,
        core_area=(margin, margin, die_w - margin, die_h - margin))

    # Place RAM
    # Must be placed outside core area to ensure we don't run into routing
    # congestion issues (due to cells being placed too close to RAM pins)
    fp.place_macros([('soc.ram.u_mem.gen_sky130.u_impl_sky130.mem', 'ram')], ram_x, ram_y, 0, 0, 'N')

    # Define pads and associated pins
    gpio_w = [(f'padring.we_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio', f'we_pad[{i}]', 'gpio') for i in range(9)]
    gpio_n = [(f'padring.no_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio', f'no_pad[{i}]', 'gpio') for i in range(9)]
    gpio_s = [(f'padring.so_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio', f'so_pad[{i}]', 'gpio') for i in range(9)]
    gpio_e = [(f'padring.ea_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio', f'ea_pad[{i}]', 'gpio') for i in range(9)]
    power = [[(f'padring.{side}_pads\\[0\\].i0.pad{port}\\[0\\].i0.io{port}',
               f'{port}' if port in ('vdd', 'vss') else f'{side}_{port}',
               f'{port}')
                for port in ('vdd', 'vss', 'vddio', 'vssio')]
                for side in ('we', 'no', 'ea', 'so')]

    pads_w = gpio_w[:5] + power[0] + gpio_w[5:9]
    pads_n = gpio_n[:5] + power[1] + gpio_n[5:9]
    pads_e = gpio_e[:5] + power[2] + gpio_e[5:9]
    pads_s = gpio_s[:5] + power[3] + gpio_s[5:9]

    # Place pads and pins w/ equal spacing
    # TODO: place pins directly under pad metal area
    die_w, die_h = fp.die_area

    # # west
    # pads_width = sum(fp.available_cells[cell].width for _, cell in pads_w)
    # spacing = (die_h - corner_w - corner_h - pads_width) / (len(pads_w) + 1)

    # y = corner_h + spacing
    # for pad_name, pad_type in pads_w:
    #     width = fp.available_cells[pad_type].width
    #     height = fp.available_cells[pad_type].height

    #     fp.place_macros([(pad_name, pad_type)], 0, y, 0, 0, 'W')
    #     # fp.place_pin([pin_name], 0, y, 0, 0, 10, 10, 'm5', 'N')

    #     y += width + spacing

    pin_depth_offset = 60
    pin_size = 10

    # north
    pads_n = pads_w + pads_n

    pads_width = sum(fp.available_cells[cell].width for _, _, cell in pads_n)
    spacing = fp.snap((die_w - corner_w - corner_h - pads_width) / (len(pads_n) + 1), 1)

    x = corner_h + spacing
    for pad_name, pin_name, pad_type in pads_n:
        width = fp.available_cells[pad_type].width
        height = fp.available_cells[pad_type].height

        fp.place_macros([(pad_name, pad_type)], x, die_h - height, 0, 0, 'N')
        # fp.place_pin([pin_name], x + width/2, die_h - pin_depth_offset, 0, 0, pin_size, pin_size, 'm5', 'N')

        x += width + spacing

    # # east
    # pads_width = sum(fp.available_cells[cell].width for _, cell in pads_e)
    # spacing = (die_h - corner_w - corner_h - pads_width) / (len(pads_e) + 1)
    # y = corner_w + spacing
    # for pad_name, pad_type in pads_e:
    #     width = fp.available_cells[pad_type].width
    #     height = fp.available_cells[pad_type].height

    #     fp.place_macros([(pad_name, pad_type)], die_w - height, y, 0, 0, 'E')

    #     y += width + spacing

    # south
    pads_s = pads_e + pads_s
    pads_width = sum(fp.available_cells[cell].width for _, _, cell in pads_s)
    spacing = fp.snap((die_w - corner_w - corner_h - pads_width) / (len(pads_s) + 1), 1)

    x = corner_w + spacing
    for pad_name, pin_name, pad_type in pads_s:
        width = fp.available_cells[pad_type].width
        height = fp.available_cells[pad_type].height

        fp.place_macros([(pad_name, pad_type)], x, 0, 0, 0, 'S')
        # fp.place_pin([pin_name], x + width/2, pin_depth_offset, 0, 0, pin_size, pin_size, 'm5', 'N')

        x += width + spacing

    # Place corners
    # NOTE: scalar placement functions could be nice
    fp.place_macros([('corner_sw.corner', 'corner')], 0, 0, 0, 0, 'S')
    fp.place_macros([('corner_nw.corner', 'corner')], 0, die_h - corner_w, 0, 0, 'W')
    fp.place_macros([('corner_se.corner', 'corner')], die_w - corner_h, 0, 0, 0, 'E')
    fp.place_macros([('corner_ne.corner', 'corner')], die_w - corner_w, die_h - corner_h, 0, 0, 'N')

    return fp
