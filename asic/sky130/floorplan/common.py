import math

def floorplan_dims(fp):
    gpio_w = fp.available_cells['gpio'].width
    gpio_h = fp.available_cells['gpio'].height
    corner_w = fp.available_cells['corner'].width
    corner_h = fp.available_cells['corner'].height

    place_w = 6750 * fp.std_cell_width
    place_h = 900 * fp.std_cell_height
    margin_min = 100

    core_w = place_w + 2 * margin_min
    core_h = place_h + 2 * margin_min
    
    die_w = math.ceil(core_w + 2 * gpio_h) 
    die_h = math.ceil(core_h + 2 * gpio_h)

    # We recalculate core_w based on ceil'd die dimensions, essentially
    # "stretching" the core margin to ensure the die dimensions are integers
    core_w = die_w - 2 * gpio_h
    core_h = die_h - 2 * gpio_h

    we_pad_types = [('gpio', i) for i in range(5)] + [('vdd', 0), ('vss', 0), ('vddio', 0), ('vssio', 0)] + [('gpio', i) for i in range(5, 9)]
    n = len(we_pad_types)
    pads_width = sum(fp.available_cells[pad_type].width for pad_type, _ in we_pad_types)
    spacing = (die_h - corner_h - corner_w - pads_width) // (n + 1)

    y = corner_h + spacing
    we_pads = []
    for pad_type, i in we_pad_types:
        we_pads.append((pad_type, i, y))
        y += gpio_w + spacing

    no_pad_types = [('gpio', i) for i in range(9, 14)] + [('vdd', 1), ('vss', 1), ('vddio', 1), ('vssio', 1)] + [('gpio', i) for i in range(14, 18)]
    n = len(no_pad_types)
    pads_width = sum(fp.available_cells[pad_type].width for pad_type, _ in no_pad_types)
    spacing = (die_w - corner_h - corner_w - pads_width) // (n + 1)

    x = corner_h + spacing
    no_pads = []
    for pad_type, i in no_pad_types:
        no_pads.append((pad_type, i, x))
        x += gpio_w + spacing

    ea_pad_types = [('gpio', i) for i in range(18, 23)] + [('vdd', 2), ('vss', 2), ('vddio', 2), ('vssio', 2)] + [('gpio', i) for i in range(23, 27)]
    n = len(ea_pad_types)
    pads_width = sum(fp.available_cells[pad_type].width for pad_type, _ in ea_pad_types)
    spacing = (die_h - corner_h - corner_w - pads_width) // (n + 1)

    y = corner_w + spacing
    ea_pads = []
    for pad_type, i in ea_pad_types:
        ea_pads.append((pad_type, i, y))
        y += gpio_w + spacing

    so_pad_types = [('gpio', i) for i in range(27, 32)] + [('vdd', 3), ('vss', 3), ('vddio', 3), ('vssio', 3)] + [('gpio', i) for i in range(32, 36)]
    n = len(so_pad_types)
    pads_width = sum(fp.available_cells[pad_type].width for pad_type, _ in so_pad_types)
    spacing = (die_w - corner_h - corner_w - pads_width) // (n + 1)

    x = corner_w + spacing
    so_pads = []
    for pad_type, i in so_pad_types:
        so_pads.append((pad_type, i, x))
        x += gpio_w + spacing

    return die_w, die_h, core_w, core_h, place_w, place_h, we_pads, no_pads, ea_pads, so_pads