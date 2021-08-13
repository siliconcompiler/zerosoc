# Bit of a hack to be able to import 'common' when dynamically importing this
# module. TODO: cleaner way to handle this?
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from common import *
from siliconcompiler.floorplan import Floorplan

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
        ('tech_cfg', 4, 16, 16.665), # enable_vswitch_h
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

    for pad_type, i, y in we_pads:
        y -= gpio_h
        if pad_type == 'gpio':
            for pin, bit, width, offset in pins:
                name = f'we_{pin}[{i * width + bit}]'
                fp.place_pins([name], 0, y + offset, 0, 0, pin_depth, pin_width, 'm2')

    for pad_type, i, x in no_pads:
        x -= gpio_h
        if pad_type == 'gpio':
            for pin, bit, width, offset in pins:
                name = f'no_{pin}[{i * width + bit}]'
                fp.place_pins([name], x + offset, die_h - pin_depth, 0, 0, pin_width, pin_depth, 'm2')

    for pad_type, i, y in ea_pads:
        y -= gpio_h 
        if pad_type == 'gpio':
            for pin, bit, width, offset in pins:
                name = f'ea_{pin}[{i * width + bit}]'
                fp.place_pins([name], die_w - pin_depth, y + gpio_w - offset - pin_width, 0, 0, pin_depth, pin_width, 'm2')

    for pad_type, i, x in so_pads:
        x -= gpio_h
        if pad_type == 'gpio':
            for pin, bit, width, offset in pins:
                name = f'so_{pin}[{i * width + bit}]'
                fp.place_pins([name], x + gpio_w - offset - pin_width, 0, 0, 0, pin_width, pin_depth, 'm2')

    # PDN
    fp.add_viarule('via_1600x480', 'M1M2_PR', (0.15, 0.15), ('m1', 'via', 'm2'), (.17, .17), (.245,  .165, .055, .165), rowcol=(1,4))
    fp.add_viarule('via2_1600x480', 'M2M3_PR', (0.2, 0.2), ('m2', 'via2', 'm3'), (.2, .2), (.04,  .140, .1, .065), rowcol=(1,4))
    fp.add_viarule('via3_1600x480', 'M3M4_PR', (0.2, 0.2), ('m3', 'via3', 'm4'), (.2, .2), (.1,  .06, .1, .14), rowcol=(1,4))
    fp.add_viarule('via4_1600x1600', 'M4M5_PR', (0.8, 0.8), ('m4', 'via4', 'm5'), (.8, .8), (.04,  .04, .04, .04))

    hpitch = 50
    hwidth = 5
    hlayer = 'm5'
    vpitch = 50
    vwidth = 5
    vlayer = 'm4'

    fp.configure_net('vdd', 'vdd', 'power')
    fp.configure_net('vss', 'vss', 'ground')

    ## Horizontal straps
    n_hori =  int(core_h // (hpitch + hwidth))
    fp.place_wires(['vdd', 'vss'] * (n_hori // 2),
        margin_w, margin_h,
        0, hpitch + hwidth,
        core_w, hwidth, hlayer, 'STRIPE')

    ## Vertical straps
    n_vert = int(core_w // (vpitch + hwidth))
    fp.place_wires(['vdd', 'vss'] * (n_vert // 2),
        margin_w, margin_h,
        vpitch + vwidth, 0,
        vwidth, core_h, vlayer, 'STRIPE')

    # Vias connecting vdd straps
    x = margin_w + vwidth / 2
    y = margin_h + hwidth / 2
    for _ in range(n_hori//2):
        fp.place_vias(['vdd'] * (n_vert//2), x, y, 2 * (vpitch + vwidth), 0, 'm4', 'via4_1600x1600')
        y += 2 * (hpitch + hwidth)

    # Vias connecting vss straps
    x = margin_w + vwidth / 2 + (vpitch + vwidth)
    y = margin_h + hwidth / 2 + (hpitch + hwidth)
    for _ in range(n_hori//2):
        fp.place_vias(['vss'] * (n_vert//2), x, y, 2 * (vpitch + vwidth), 0, 'm4', 'via4_1600x1600')
        y += 2 * (hpitch + hwidth)

    npwr = 1 + math.floor(len(fp.rows) / 2)
    ngnd = math.ceil(len(fp.rows) / 2)

    # Vias connecting vdd straps to std cell stripes
    x = margin_w + vwidth / 2
    y = margin_h
    for _ in range(n_vert // 2):
        if x < ram_x - ram_core_space:
            fp.place_vias(['vdd'] * npwr, x, y, 0, 2 * fp.std_cell_height, 'm3', 'via3_1600x480')
            fp.place_vias(['vdd'] * npwr, x, y, 0, 2 * fp.std_cell_height, 'm2', 'via2_1600x480')
            fp.place_vias(['vdd'] * npwr, x, y, 0, 2 * fp.std_cell_height, 'm1', 'via1_1600x480')
        elif x > ram_x and x < ram_x + ram_w:
            fp.place_vias(['vdd'] * 2, x, ram_y + 5.63, 0, 405.28, 'm3', 'via3_1600x480')

        x += 2 * (vpitch + vwidth)

    # Vias connecting vss straps to std cell stripes
    x = margin_w + vwidth / 2 + (vpitch + vwidth)
    y = margin_h + fp.std_cell_height
    for _ in range(n_vert // 2):
        if x < ram_x - ram_core_space:
            fp.place_vias(['vss'] * ngnd, x, y, 0, 2 * fp.std_cell_height, 'm3', 'via3_1600x480')
            fp.place_vias(['vss'] * ngnd, x, y, 0, 2 * fp.std_cell_height, 'm2', 'via2_1600x480')
            fp.place_vias(['vss'] * ngnd, x, y, 0, 2 * fp.std_cell_height, 'm1', 'via1_1600x480')
        elif x > ram_x and x < ram_x + ram_w:
            fp.place_vias(['vss'] * 2, x, ram_y + 2.23, 0, 412.08, 'm3', 'via3_1600x480')

        x += 2 * (vpitch + vwidth)

    return fp

def generate_floorplan(chip):
    fp = Floorplan(chip)
    fp = setup_floorplan(fp, chip)
    fp.write_def('asic_core.def')
    fp.write_lef('asic_core.lef')
