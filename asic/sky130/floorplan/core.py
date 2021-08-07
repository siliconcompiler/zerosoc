# Bit of a hack to be able to import 'common' when dynamically importing this
# module. TODO: cleaner way to handle this?
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from common import *

def setup_floorplan(fp, chip):
    # TODO: this should be automatically set to a valid value
    fp.db_units = 1000

    _, _, die_w, die_h, core_w, core_h, we_pads, no_pads, ea_pads, so_pads = floorplan_dims(fp)
    
    gpio_w = fp.available_cells['gpio'].width
    gpio_h = fp.available_cells['gpio'].height
    ram_w = fp.available_cells['ram'].width
    ram_h = fp.available_cells['ram'].height

    margin_w = (die_w - core_w) / 2
    margin_h = (die_h - core_h) / 2

    ram_core_space = 250 * fp.std_cell_width

    ram_x = fp.snap(die_w - margin_w - ram_w - ram_core_space, fp.std_cell_width)
    ram_y = fp.snap(die_h - margin_h - ram_h - 50 * fp.std_cell_height, fp.std_cell_height)
    
    fp.create_die_area(die_w, die_h, core_area = (margin_w, margin_h, ram_x - ram_core_space, core_h + margin_h))
    
    # Place RAM
    # Must be placed outside core area to ensure we don't run into routing
    # congestion issues (due to cells being placed too close to RAM pins)
    fp.place_macros([('soc.ram.u_mem.gen_sky130.u_impl_sky130.genblk1.mem', 'ram')], ram_x, ram_y, 0, 0, 'N')

    # Place pins
    oe_offset = 4.245
    out_offset = 19.885
    in_offset = 75.08
    pin_width = 0.28
    pin_depth = 1

    pins = [
        ('din', 0, 1, 75.085), # in
        ('dout', 0, 1, 19.885), # out
        ('ie', 0, 1, 41.505), # inp_dis
        ('oen', 0, 1, 4.245), # oe_n
        ('tech_cfg', 0, 16, 31.845), # hld_h_n
        ('tech_cfg', 1, 16, 35.065), # enable_h
        ('tech_cfg', 2, 16, 38.285), # enable_inp_h
        ('tech_cfg', 3, 16, 13.445), # enable_vdda_h
        ('tech_cfg', 4, 16, 16.310), # enable_vswitch_h
        ('tech_cfg', 5, 16, 69.105), # enable_vddio
        ('tech_cfg', 6, 16, 7.465), # ib_mode_sel
        ('tech_cfg', 7, 16, 10.685), # vtrip_sel
        ('tech_cfg', 8, 16, 65.885), # slow
        ('tech_cfg', 9, 16, 22.645), # hld_ovr
        ('tech_cfg', 10, 16, 50.705), # analog_en
        ('tech_cfg', 11, 16, 29.085), # analog_sel
        ('tech_cfg', 12, 16, 44.265), # analog_pol
        ('tech_cfg', 13, 16, 47.485), # dm[0]
        ('tech_cfg', 14, 16, 56.685), # dm[1]
        ('tech_cfg', 15, 16, 25.865), # dm[2]
    ]

    for i, y in enumerate(we_pads):
        y -= gpio_h
        for pin, bit, width, offset in pins:
            name = f'we_{pin}[{i * width + bit}]'
            fp.place_pins([name], 0, y + offset, 0, 0, pin_depth, pin_width, 'm2')

    for i, x in enumerate(no_pads):
        x -= gpio_h
        for pin, bit, width, offset in pins:
            name = f'no_{pin}[{i * width + bit}]'
            fp.place_pins([name], x + offset, die_h - pin_depth, 0, 0, pin_width, pin_depth, 'm2')

    for i, y in enumerate(ea_pads):
        y -= gpio_h 
        for pin, bit, width, offset in pins:
            name = f'ea_{pin}[{i * width + bit}]'
            fp.place_pins([name], die_w - pin_depth, y + gpio_w - offset - pin_width, 0, 0, pin_depth, pin_width, 'm2')

    for i, x in enumerate(so_pads):
        x -= gpio_h
        for pin, bit, width, offset in pins:
            name = f'so_{pin}[{i * width + bit}]'
            fp.place_pins([name], x + gpio_w - offset - pin_width, 0, 0, 0, pin_width, pin_depth, 'm2')
   
    return fp
