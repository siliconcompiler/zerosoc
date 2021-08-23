import math

def define_dimensions(fp):
    # Add 2.035 since GPIO cell's bottom pins stick out by that much
    gpio_h = fp.available_cells['gpio'].height + 2.035

    place_w = 6750 * fp.std_cell_width
    place_h = 900 * fp.std_cell_height
    margin_x = 60 * fp.std_cell_width
    margin_y = 10 * fp.std_cell_height

    core_w = math.ceil(place_w + 2 * margin_x)
    core_h = math.ceil(place_h + 2 * margin_y)

    die_w = core_w + 2 * gpio_h
    die_h = core_h + 2 * gpio_h

    # die_w = math.ceil(core_w + 2 * gpio_h)
    # die_h = math.ceil(core_h + 2 * gpio_h)

    # core_w = die_w - 2 * gpio_h
    # core_h = die_h - 2 * gpio_h

    assert die_w % 1 == 0
    assert die_h % 1 == 0

    return die_w, die_h, core_w, core_h, place_w, place_h

def calculate_even_spacing(fp, pads, distance):
    n = len(pads)
    pads_width = sum(fp.available_cells[pad].width for pad in pads)
    spacing = (distance - pads_width) // (n + 1)

    return spacing

def define_io_placement(fp):
    die_w, die_h, _, _, _, _ = define_dimensions(fp)

    corner_w = fp.available_cells['corner'].width
    corner_h = fp.available_cells['corner'].height

    # Define I/O arrangement on each side
    we_io = ['gpio'] * 5 + ['vdd', 'vss', 'vddio', 'vssio'] + ['gpio'] * 4
    no_io = ['gpio'] * 9 + ['vdd', 'vss', 'vddio', 'vssio']
    ea_io = ['gpio'] * 9 + ['vdd', 'vss', 'vddio', 'vssio']
    so_io = ['gpio'] * 5 + ['vdd', 'vss', 'vddio', 'vssio'] + ['gpio'] * 4

    # Calculate location of each I/O pad
    spacing = calculate_even_spacing(fp, we_io, die_h - corner_h - corner_w)
    y = corner_h + spacing
    we_io_pos = []
    for pad_type in we_io:
        we_io_pos.append((pad_type, y))
        y += fp.available_cells[pad_type].width + spacing

    spacing = calculate_even_spacing(fp, no_io, die_w - corner_h - corner_w)
    x = corner_h + spacing
    no_io_pos = []
    for pad_type in no_io:
        no_io_pos.append((pad_type, x))
        x += fp.available_cells[pad_type].width + spacing

    spacing = calculate_even_spacing(fp, ea_io, die_h - corner_h - corner_w)
    y = corner_w + spacing
    ea_io_pos = []
    for pad_type in ea_io:
        ea_io_pos.append((pad_type, y))
        y += fp.available_cells[pad_type].width + spacing

    spacing = calculate_even_spacing(fp, so_io, die_w - corner_h - corner_w)
    x = corner_w + spacing
    so_io_pos = []
    for pad_type in so_io:
        so_io_pos.append((pad_type, x))
        x += fp.available_cells[pad_type].width + spacing

    return  we_io_pos, no_io_pos, ea_io_pos, so_io_pos
