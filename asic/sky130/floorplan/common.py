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

    n = 9
    spacing = (die_h - corner_h - corner_w - n * gpio_w) // (n + 1)

    y = corner_h + spacing
    we_pads = []
    for _ in range(n):
        we_pads.append(y)
        y += gpio_w + spacing

    n = 9
    spacing = (die_w - corner_h - corner_w - n * gpio_w) // (n + 1)

    x = corner_h + spacing
    no_pads = []
    for _ in range(n):
        no_pads.append(x)
        x += gpio_w + spacing

    n = 9
    spacing = (die_h - corner_h - corner_w - n * gpio_w) // (n + 1)

    y = corner_w + spacing
    ea_pads = []
    for _ in range(n):
        ea_pads.append(y)
        y += gpio_w + spacing

    n = 9
    spacing = (die_w - corner_h - corner_w - n * gpio_w) // (n + 1)

    x = corner_w + spacing
    so_pads = []
    for _ in range(n):
        so_pads.append(x)
        x += gpio_w + spacing

    return die_w, die_h, core_w, core_h, place_w, place_h, we_pads, no_pads, ea_pads, so_pads