import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from common import *

def setup_floorplan(fp, chip):
    # TODO: this should be automatically set to a valid value
    fp.db_units = 1000

    die_w, die_h, core_w, core_h, _, _, we_pads, no_pads, ea_pads, so_pads = floorplan_dims(fp)

    gpio_w = fp.available_cells['gpio'].width
    gpio_h = fp.available_cells['gpio'].height
    corner_w = fp.available_cells['corner'].width
    corner_h = fp.available_cells['corner'].height
    fill_cell_h = fp.available_cells['fill1'].height

    # Initialize die
    fp.create_die_area(die_w, die_h, generate_rows=False, generate_tracks=False)
    
    # Place corners
    # NOTE: scalar placement functions could be nice
    fp.place_macros([('corner_sw', 'corner')], 0, 0, 0, 0, 'S')
    fp.place_macros([('corner_nw', 'corner')], 0, die_h - corner_w, 0, 0, 'W')
    fp.place_macros([('corner_se', 'corner')], die_w - corner_h, 0, 0, 0, 'E')
    fp.place_macros([('corner_ne', 'corner')], die_w - corner_w, die_h - corner_h, 0, 0, 'N')

    # Place I/O pads
    for i, y in enumerate(we_pads):
        name = f'we_pad{i}'
        fp.place_macros([(name, 'gpio')], 0, y, 0, 0, 'W')
    for i, x in enumerate(no_pads):
        name = f'no_pad{i}'
        fp.place_macros([(name, 'gpio')], x, die_h - gpio_h, 0, 0, 'N')
    for i, y in enumerate(ea_pads):
        name = f'ea_pad{i}'
        fp.place_macros([(name, 'gpio')], die_w - gpio_h, y, 0, 0, 'E')
    for i, x in enumerate(so_pads):
        name = f'so_pad{i}'
        fp.place_macros([(name, 'gpio')], x, 0, 0, 0, 'S')
    
    # Fill I/O region
    fp.fill_io_region([(0, 0), (fill_cell_h, die_h)], ['fill1', 'fill5', 'fill10', 'fill20'], 'W')
    fp.fill_io_region([(0, die_h - fill_cell_h), (die_w, die_h)], ['fill1', 'fill5', 'fill10', 'fill20'], 'N')
    fp.fill_io_region([(die_w - fill_cell_h, 0), (die_w, die_h)], ['fill1', 'fill5', 'fill10', 'fill20'], 'E')
    fp.fill_io_region([(0, 0), (die_w, fill_cell_h)], ['fill1', 'fill5', 'fill10', 'fill20'], 'S')
    
    fp.place_macros([('core', 'zerosoc')], gpio_h, gpio_h, 0, 0, 'N')

    return fp