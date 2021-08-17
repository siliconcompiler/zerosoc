import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from common import *
from siliconcompiler.floorplan import Floorplan

def setup_floorplan(fp, chip):
    # TODO: this should be automatically set to a valid value
    fp.db_units = 1000

    die_w, die_h, core_w, core_h, _, _, we_pads, no_pads, ea_pads, so_pads = floorplan_dims(fp)

    gpio_w = fp.available_cells['gpio'].width
    gpio_h = fp.available_cells['gpio'].height + 2.035
    corner_w = fp.available_cells['corner'].width
    corner_h = fp.available_cells['corner'].height
    fill_cell_h = fp.available_cells['fill1'].height

    # Initialize die
    fp.create_die_area(die_w, die_h, generate_rows=False, generate_tracks=False)

    # Place corners
    # NOTE: scalar placement functions could be nice
    fp.place_macros([('corner_sw.i0', 'corner')], 0, 0, 0, 0, 'S')
    fp.place_macros([('corner_nw.i0', 'corner')], 0, die_h - corner_w, 0, 0, 'W')
    fp.place_macros([('corner_se.i0', 'corner')], die_w - corner_h, 0, 0, 0, 'E')
    fp.place_macros([('corner_ne.i0', 'corner')], die_w - corner_w, die_h - corner_h, 0, 0, 'N')

    # Place I/O pads
    for pad_type, i, y in we_pads:
        if pad_type == 'gpio':
            name = f'padring.we_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio'
        else:
            name = f'{pad_type}{i}'
        fp.place_macros([(name, pad_type)], 0, y, 0, 0, 'W')
    for pad_type, i, x in no_pads:
        if pad_type == 'gpio':
            name = f'padring.no_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio'
        else:
            name = f'{pad_type}{i}'
        pad_h = fp.available_cells[pad_type].height
        fp.place_macros([(name, pad_type)], x, die_h - pad_h, 0, 0, 'N')
    for pad_type, i, y in ea_pads:
        if pad_type == 'gpio':
            name = f'padring.ea_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio'
        else:
            name = f'{pad_type}{i}'
        pad_h = fp.available_cells[pad_type].height
        fp.place_macros([(name, pad_type)], die_w - pad_h, y, 0, 0, 'E')
    for pad_type, i, x in so_pads:
        if pad_type == 'gpio':
            name = f'padring.so_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio'
        else:
            name = f'{pad_type}{i}'
        fp.place_macros([(name, pad_type)], x, 0, 0, 0, 'S')

    # Fill I/O region
    fp.fill_io_region([(0, 0), (fill_cell_h, die_h)], ['fill1', 'fill5', 'fill10', 'fill20'], 'W')
    fp.fill_io_region([(0, die_h - fill_cell_h), (die_w, die_h)], ['fill1', 'fill5', 'fill10', 'fill20'], 'N')
    fp.fill_io_region([(die_w - fill_cell_h, 0), (die_w, die_h)], ['fill1', 'fill5', 'fill10', 'fill20'], 'E')
    fp.fill_io_region([(0, 0), (die_w, fill_cell_h)], ['fill1', 'fill5', 'fill10', 'fill20'], 'S')

    fp.place_macros([('core', 'asic_core')], gpio_h, gpio_h, 0, 0, 'N')

    return fp

def generate_floorplan(chip):
    fp = Floorplan(chip)
    fp = setup_floorplan(fp, chip)
    fp.write_def('asic_top.def')
