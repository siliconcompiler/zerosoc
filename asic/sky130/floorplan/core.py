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

    fp.configure_net('vdd', 'vdd', 'power')
    fp.configure_net('vss', 'vss', 'ground')

    gpio_w = fp.available_cells['gpio'].width
    gpio_h = fp.available_cells['gpio'].height + 2.035
    ram_w = fp.available_cells['ram'].width
    ram_h = fp.available_cells['ram'].height

    margin_w = (die_w - core_w) / 2
    margin_h = (die_h - core_h) / 2

    ram_core_space = 250 * fp.std_cell_width

    ram_x = fp.snap(die_w - margin_w - ram_w - ram_core_space, fp.std_cell_width)
    ram_y = fp.snap(die_h - margin_h - ram_h - 50 * fp.std_cell_height, fp.std_cell_height)

    fp.create_die_area(die_w, die_h, core_area = (margin_w, margin_h, ram_x - ram_core_space, core_h + margin_h))

    # PDN config (used throughout)
    n_vert = 8
    vwidth = 5
    vpitch = ((ram_x - ram_core_space - margin_w)  - n_vert * vwidth) / (n_vert + 1)
    vlayer = 'm4'

    n_hori = 10
    hwidth = 5
    hpitch = (core_h - n_hori * hwidth) / (n_hori + 1)
    hlayer = 'm5'

    vss_ring_left_x = margin_w - 4 * vwidth
    vss_ring_right_x = core_w + margin_w + 4 * vwidth
    vss_ring_bottom_y = margin_h - 4 * hwidth
    vss_ring_top_y = core_h + margin_h + 4 * hwidth
    vss_ring_width = core_w + 9 * vwidth
    vss_ring_height = core_h + 9 * hwidth

    vdd_ring_left_x = vss_ring_left_x + 2 * vwidth
    vdd_ring_right_x = vss_ring_right_x - 2 * vwidth
    vdd_ring_bottom_y = vss_ring_bottom_y + 2 * hwidth
    vdd_ring_top_y = vss_ring_top_y - 2 * hwidth
    vdd_ring_width = vss_ring_width - 4 * vwidth
    vdd_ring_height = vss_ring_height - 4 * hwidth

    # power ring
    ## vss bottom
    fp.place_wires(['vss'], vss_ring_left_x, vss_ring_bottom_y, 0, 0, vss_ring_width, hwidth, 'm5', 'stripe')
    ## vss top
    fp.place_wires(['vss'], vss_ring_left_x, vss_ring_top_y, 0, 0, vss_ring_width, hwidth, 'm5', 'stripe')
    ## vss left
    fp.place_wires(['vss'], vss_ring_left_x, vss_ring_bottom_y, 0, 0, vwidth, vss_ring_height, 'm4', 'stripe')
    ## vss right
    fp.place_wires(['vss'], vss_ring_right_x, vss_ring_bottom_y, 0, 0, hwidth, vss_ring_height, 'm4', 'stripe')

    # vss bottom+left
    fp.place_vias(['vss'], vss_ring_left_x + vwidth/2, vss_ring_bottom_y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')
    # vss top+left
    fp.place_vias(['vss'], vss_ring_left_x + vwidth/2, vss_ring_top_y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')
    # vss top+right
    fp.place_vias(['vss'], vss_ring_right_x + vwidth/2, vss_ring_top_y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')
    # vss bottom+right
    fp.place_vias(['vss'], vss_ring_right_x + vwidth/2, vss_ring_bottom_y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')

    ## vdd bottom
    fp.place_wires(['vdd'], vdd_ring_left_x, vdd_ring_bottom_y, 0, 0, vdd_ring_width, hwidth, 'm5', 'stripe')
    ## vdd top
    fp.place_wires(['vdd'], vdd_ring_left_x, vdd_ring_top_y, 0, 0, vdd_ring_width, hwidth, 'm5', 'stripe')
    ## vdd left
    fp.place_wires(['vdd'], vdd_ring_left_x, vdd_ring_bottom_y, 0, 0, vwidth, vdd_ring_height, 'm4', 'stripe')
    ## vss right
    fp.place_wires(['vdd'], vdd_ring_right_x, vdd_ring_bottom_y, 0, 0, hwidth, vdd_ring_height, 'm4', 'stripe')

    # vdd bottom+left
    fp.place_vias(['vdd'], vdd_ring_left_x + vwidth/2, vdd_ring_bottom_y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')
    # vdd top+left
    fp.place_vias(['vdd'], vdd_ring_left_x + vwidth/2, vdd_ring_top_y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')
    # vdd top+right
    fp.place_vias(['vdd'], vdd_ring_right_x + vwidth/2, vdd_ring_top_y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')
    # vdd bottom+right
    fp.place_vias(['vdd'], vdd_ring_right_x + vwidth/2, vdd_ring_bottom_y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')

    # Place RAM
    # Must be placed outside core area to ensure we don't run into routing
    # congestion issues (due to cells being placed too close to RAM pins)
    fp.place_macros([('soc.ram.u_mem.gen_sky130.u_impl_sky130.genblk1.mem', 'ram')], ram_x, ram_y, 0, 0, 'N')

    # Place pins
    pin_depth = 1

    pins = [
        ('din', 0, 1, 79.240, 79.570, 'm3'), # in
        ('dout', 0, 1, 22.355, 22.615, 'm2'), # out
        ('ie', 0, 1, 45.245, 45.505, 'm2'), # inp_dis
        ('oen', 0, 1, 3.375, 3.605, 'm2'), # oe_n
        ('tech_cfg', 0, 16, 31.815, 32.075, 'm2'), # hld_h_n
        ('tech_cfg', 1, 16, 35.460, 35.720, 'm2'), # enable_h
        ('tech_cfg', 2, 16, 38.390, 38.650, 'm2'), # enable_inp_h
        ('tech_cfg', 3, 16, 12.755, 13.015, 'm2'), # enable_vdda_h
        ('tech_cfg', 4, 16, 16.310, 16.570, 'm2'), # enable_vswitch_h
        ('tech_cfg', 5, 16, 78.580, 78.910, 'm3'), # enable_vddio
        ('tech_cfg', 6, 16, 5.420, 5.650, 'm2'), # ib_mode_sel
        ('tech_cfg', 7, 16, 6.130, 6.390, 'm2'), # vtrip_sel
        ('tech_cfg', 8, 16, 77.610, 77.870, 'm2'), # slow
        ('tech_cfg', 9, 16, 26.600, 26.860, 'm2'), # hld_ovr
        ('tech_cfg', 10, 16, 62.430, 62.690, 'm1'), # analog_en
        ('tech_cfg', 11, 16, 30.750, 31.010, 'm2'), # analog_sel
        ('tech_cfg', 12, 16, 45.865, 46.195, 'm3'), # analog_pol
        ('tech_cfg', 13, 16, 49.855, 50.115, 'm2'), # dm[0]
        ('tech_cfg', 14, 16, 66.835, 67.095, 'm2'), # dm[1]
        ('tech_cfg', 15, 16, 28.490, 28.750, 'm2'), # dm[2]
    ]

    for pad_type, i, y in we_pads:
        y -= gpio_h
        if pad_type == 'gpio':
            for pin, bit, width, offset_l, offset_h, layer in pins:
                name = f'we_{pin}[{i * width + bit}]'
                pin_width = offset_h - offset_l
                fp.place_pins([name], 0, y + offset_l, 0, 0, pin_depth, pin_width, layer)
        elif pad_type == 'vdd':
            fp.place_wires(['vdd'], 0, y + 0.495, 0, 0, vdd_ring_left_x + vwidth, 23.9, 'm3', 'followpin')
            fp.place_wires(['vdd'], 0, y + 50.39, 0, 0, vdd_ring_left_x + vwidth, 23.9, 'm3', 'followpin')
            fp.place_pins(['vdd'], 0, y + 0.495, 0, 0, vdd_ring_left_x + vwidth, 23.9, 'm3')
            fp.place_pins(['vdd'], 0, y + 50.39, 0, 0, vdd_ring_left_x + vwidth, 23.9, 'm3')
            fp.place_vias(['vdd'], vdd_ring_left_x + vwidth/2, y + 0.495 + 23.9/2, 0, 0, 'm3', 'via3_1600x480')
            fp.place_vias(['vdd'], vdd_ring_left_x + vwidth/2, y + 50.39 + 23.9/2, 0, 0, 'm3', 'via3_1600x480')
        elif pad_type == 'vss':
            fp.place_wires(['vss'], 0, y + 0.495, 0, 0, vss_ring_left_x + vwidth, 23.9, 'm3', 'followpin')
            fp.place_wires(['vss'], 0, y + 50.39, 0, 0, vss_ring_left_x + vwidth, 23.9, 'm3', 'followpin')
            fp.place_pins(['vss'], 0, y + 0.495, 0, 0, vss_ring_left_x + vwidth, 23.9, 'm3')
            fp.place_pins(['vss'], 0, y + 50.39, 0, 0, vss_ring_left_x + vwidth, 23.9, 'm3')
            fp.place_vias(['vss'], vss_ring_left_x + vwidth/2, y + 0.495 + 23.9/2, 0, 0, 'm3', 'via3_1600x480')
            fp.place_vias(['vss'], vss_ring_left_x + vwidth/2, y + 50.39 + 23.9/2, 0, 0, 'm3', 'via3_1600x480')

    pow_strap_depth = margin_h + hwidth
    for pad_type, i, x in no_pads:
        x -= gpio_h
        if pad_type == 'gpio':
            for pin, bit, width, offset_l, offset_h, layer in pins:
                name = f'no_{pin}[{i * width + bit}]'
                pin_width = offset_h - offset_l
                fp.place_pins([name], x + offset_l, die_h - pin_depth, 0, 0, pin_width, pin_depth, layer)
        elif pad_type == 'vdd':
            fp.place_wires(['vdd'], x + 0.495, vdd_ring_top_y, 0, 0, 23.9, die_h - vdd_ring_top_y, 'm3', 'followpin')
            fp.place_wires(['vdd'], x + 50.39, vdd_ring_top_y, 0, 0, 23.9, die_h - vdd_ring_top_y, 'm3', 'followpin')
            fp.place_pins(['vdd'], x + 0.495, vdd_ring_top_y, 0, 0, 23.9, die_h - vdd_ring_top_y, 'm3')
            fp.place_pins(['vdd'], x + 50.39, vdd_ring_top_y, 0, 0, 23.9, die_h - vdd_ring_top_y, 'm3')
            fp.place_vias(['vdd'], x + 0.495 + 23.9/2, vdd_ring_top_y + hwidth/2, 0, 0, 'm3', 'via3_1600x480')
            fp.place_vias(['vdd'], x + 50.39 + 23.9/2, vdd_ring_top_y + hwidth/2, 0, 0, 'm3', 'via3_1600x480')
        elif pad_type == 'vss':
            fp.place_wires(['vss'], x + 0.495, vss_ring_top_y, 0, 0, 23.9, die_h - vss_ring_top_y, 'm3', 'followpin')
            fp.place_wires(['vss'], x + 50.39, vss_ring_top_y, 0, 0, 23.9, die_h - vss_ring_top_y, 'm3', 'followpin')
            fp.place_pins(['vss'], x + 0.495, vss_ring_top_y, 0, 0, 23.9, die_h - vss_ring_top_y, 'm3')
            fp.place_pins(['vss'], x + 50.39, vss_ring_top_y, 0, 0, 23.9, die_h - vss_ring_top_y, 'm3')
            fp.place_vias(['vss'], x + 0.495 + 23.9/2, vss_ring_top_y + hwidth/2, 0, 0, 'm3', 'via3_1600x480')
            fp.place_vias(['vss'], x + 50.39 + 23.9/2, vss_ring_top_y + hwidth/2, 0, 0, 'm3', 'via3_1600x480')

    for pad_type, i, y in ea_pads:
        y -= gpio_h
        if pad_type == 'gpio':
            for pin, bit, width, offset_l, offset_h, layer in pins:
                name = f'ea_{pin}[{i * width + bit}]'
                pin_width = offset_h - offset_l
                fp.place_pins([name], die_w - pin_depth, y + gpio_w - offset_l - pin_width, 0, 0, pin_depth, pin_width, layer)
        elif pad_type == 'vdd':
            fp.place_wires(['vdd'], vdd_ring_right_x, y + 0.495, 0, 0, die_w - vdd_ring_right_x, 23.9, 'm3', 'followpin')
            fp.place_wires(['vdd'], vdd_ring_right_x, y + 50.39, 0, 0, die_w - vdd_ring_right_x, 23.9, 'm3', 'followpin')
            fp.place_pins(['vdd'], vdd_ring_right_x, y + 0.495, 0, 0, die_w - vdd_ring_right_x, 23.9, 'm3')
            fp.place_pins(['vdd'], vdd_ring_right_x, y + 50.39, 0, 0, die_w - vdd_ring_right_x, 23.9, 'm3')
            fp.place_vias(['vdd'], vdd_ring_right_x + vwidth/2, y + 0.495 + 23.9/2, 0, 0, 'm3', 'via3_1600x480')
            fp.place_vias(['vdd'], vdd_ring_right_x + vwidth/2, y + 50.39 + 23.9/2, 0, 0, 'm3', 'via3_1600x480')
        elif pad_type == 'vss':
            fp.place_wires(['vss'], vss_ring_right_x, y + 0.495, 0, 0, die_w - vss_ring_right_x, 23.9, 'm3', 'followpin')
            fp.place_wires(['vss'], vss_ring_right_x, y + 50.39, 0, 0, die_w - vss_ring_right_x, 23.9, 'm3', 'followpin')
            fp.place_pins(['vss'], vdd_ring_right_x, y + 0.495, 0, 0, die_w - vdd_ring_right_x, 23.9, 'm3')
            fp.place_pins(['vss'], vdd_ring_right_x, y + 50.39, 0, 0, die_w - vdd_ring_right_x, 23.9, 'm3')
            fp.place_vias(['vss'], vss_ring_right_x + vwidth/2, y + 0.495 + 23.9/2, 0, 0, 'm3', 'via3_1600x480')
            fp.place_vias(['vss'], vss_ring_right_x + vwidth/2, y + 50.39 + 23.9/2, 0, 0, 'm3', 'via3_1600x480')

    pow_strap_depth = margin_h + hwidth
    for pad_type, i, x in so_pads:
        x -= gpio_h
        if pad_type == 'gpio':
            for pin, bit, width, offset_l, offset_h, layer in pins:
                name = f'so_{pin}[{i * width + bit}]'
                pin_width = offset_h - offset_l
                fp.place_pins([name], x + gpio_w - offset_l - pin_width, 0, 0, 0, pin_width, pin_depth, layer)
        elif pad_type == 'vdd':
            fp.place_wires(['vdd'], x + 0.495, 0, 0, 0, 23.9, vdd_ring_bottom_y + hwidth, 'm3', 'followpin')
            fp.place_wires(['vdd'], x + 50.39, 0, 0, 0, 23.9, vdd_ring_bottom_y + hwidth, 'm3', 'followpin')
            fp.place_pins(['vdd'], x + 0.495, 0, 0, 0, 23.9, vdd_ring_bottom_y + hwidth, 'm3')
            fp.place_pins(['vdd'], x + 50.39, 0, 0, 0, 23.9, vdd_ring_bottom_y + hwidth, 'm3')
            fp.place_vias(['vdd'], x + 0.495 + 23.9/2, vdd_ring_bottom_y + hwidth/2, 0, 0, 'm3', 'via3_1600x480')
            fp.place_vias(['vdd'], x + 50.39 + 23.9/2, vdd_ring_bottom_y + hwidth/2, 0, 0, 'm3', 'via3_1600x480')
        elif pad_type == 'vss':
            fp.place_wires(['vss'], x + 0.495, 0, 0, 0, 23.9, vss_ring_bottom_y + hwidth, 'm3', 'followpin')
            fp.place_wires(['vss'], x + 50.39, 0, 0, 0, 23.9, vss_ring_bottom_y + hwidth, 'm3', 'followpin')
            fp.place_pins(['vss'], x + 0.495, 0, 0, 0, 23.9, vss_ring_bottom_y + hwidth, 'm3')
            fp.place_pins(['vss'], x + 50.39, 0, 0, 0, 23.9, vss_ring_bottom_y + hwidth, 'm3')
            fp.place_vias(['vss'], x + 0.495 + 23.9/2, vss_ring_bottom_y + hwidth/2, 0, 0, 'm3', 'via3_1600x480')
            fp.place_vias(['vss'], x + 50.39 + 23.9/2, vss_ring_bottom_y + hwidth/2, 0, 0, 'm3', 'via3_1600x480')

    # # PDN
    fp.add_viarule('via_1600x480', 'M1M2_PR', (0.15, 0.15), ('m1', 'via', 'm2'), (.17, .17), (.245,  .165, .055, .165), rowcol=(1,4))
    fp.add_viarule('via2_1600x480', 'M2M3_PR', (0.2, 0.2), ('m2', 'via2', 'm3'), (.2, .2), (.04,  .140, .1, .065), rowcol=(1,4))
    fp.add_viarule('via3_1600x480', 'M3M4_PR', (0.2, 0.2), ('m3', 'via3', 'm4'), (.2, .2), (.1,  .06, .1, .14), rowcol=(1,4))
    fp.add_viarule('via4_1600x1600', 'M4M5_PR', (0.8, 0.8), ('m4', 'via4', 'm5'), (.8, .8), (.04,  .04, .04, .04))

    ## Horizontal straps
    y = margin_h + hpitch
    for _ in range(n_hori//2):
        fp.place_wires(['vdd'],
            vdd_ring_left_x, y,
            0, 0,
            vdd_ring_width, hwidth, hlayer, 'STRIPE')
        # RAM power vias
        if y > ram_y and y < ram_y + ram_h:
            fp.place_vias(['vdd'], ram_x + 4.76 + 1.74/2, y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')
            fp.place_vias(['vdd'], ram_x + 678.34 - 1.74/2, y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')

        y += 2 * (hpitch + hwidth)

    fp.place_vias(['vdd'] * (n_hori // 2),
        vdd_ring_left_x + vwidth/2, margin_h + hpitch + hwidth/2,
        0, 2 * (hpitch + hwidth), 'm4', 'via4_1600x1600')

    fp.place_vias(['vdd'] * (n_hori // 2),
        vdd_ring_right_x + vwidth/2, margin_h + hpitch + hwidth/2,
        0, 2 * (hpitch + hwidth), 'm4', 'via4_1600x1600')

    y = margin_h + hpitch + (hpitch + hwidth)
    for _ in range(n_hori//2):
        fp.place_wires(['vss'],
            vss_ring_left_x, y,
            0, 0,
            vss_ring_width, hwidth, hlayer, 'STRIPE')
        y += 2 * (hpitch + hwidth)
        # RAM power vias
        if y > ram_y and y < ram_y + ram_h:
            fp.place_vias(['vss'], ram_x + 1.36 + 1.74/2, y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')
            fp.place_vias(['vss'], ram_x + 681.74 - 1.74/2, y + hwidth/2, 0, 0, 'm4', 'via4_1600x1600')

    fp.place_vias(['vss'] * (n_vert // 2),
        vss_ring_left_x + vwidth/2, margin_h + hpitch + (hpitch + hwidth) + hwidth/2,
        0, 2 * (hpitch + hwidth), 'm4', 'via4_1600x1600')

    fp.place_vias(['vss'] * (n_vert // 2),
        vss_ring_right_x + vwidth/2, margin_h + hpitch + (hpitch + hwidth) + hwidth/2,
        0, 2 * (hpitch + hwidth), 'm4', 'via4_1600x1600')

    ## Vertical straps
    fp.place_wires(['vdd'] * (n_vert // 2),
        margin_w + vpitch, vdd_ring_bottom_y,
        2 * (vpitch + vwidth), 0,
        vwidth, vdd_ring_height, vlayer, 'STRIPE')

    fp.place_vias(['vdd'] * (n_vert // 2),
        margin_w + vpitch + vwidth/2, vdd_ring_bottom_y + hwidth/2,
        2 * (vpitch + vwidth), 0, 'm4', 'via4_1600x1600')

    fp.place_vias(['vdd'] * (n_vert // 2),
        margin_w + vpitch + vwidth/2, vdd_ring_top_y + hwidth/2,
        2 * (vpitch + vwidth), 0, 'm4', 'via4_1600x1600')

    fp.place_wires(['vss'] * (n_vert // 2),
        margin_w + vpitch + (vpitch + vwidth), vss_ring_bottom_y,
        2 * (vpitch + vwidth), 0,
        vwidth, core_h + 9 * hwidth, vlayer, 'STRIPE')

    fp.place_vias(['vss'] * (n_vert // 2),
        margin_w + vpitch + (vpitch + vwidth) + vwidth/2, vss_ring_bottom_y + hwidth/2,
        2 * (vpitch + vwidth), 0, 'm4', 'via4_1600x1600')

    fp.place_vias(['vss'] * (n_vert // 2),
        margin_w + vpitch + (vpitch + vwidth) + vwidth/2, vss_ring_top_y + hwidth/2,
        2 * (vpitch + vwidth), 0, 'm4', 'via4_1600x1600')

    # Vias connecting vdd straps
    x = margin_w + vpitch + vwidth/2
    y = margin_h + hpitch + hwidth/2
    for _ in range(n_hori//2):
        fp.place_vias(['vdd'] * (n_vert//2), x, y, 2 * (vpitch + vwidth), 0, 'm4', 'via4_1600x1600')
        y += 2 * (hpitch + hwidth)

    # Vias connecting vss straps
    x = margin_w + vpitch + vwidth / 2 + (vpitch + vwidth)
    y = margin_h + hpitch + hwidth / 2 + (hpitch + hwidth)
    for _ in range(n_hori//2):
        fp.place_vias(['vss'] * (n_vert//2), x, y, 2 * (vpitch + vwidth), 0, 'm4', 'via4_1600x1600')
        y += 2 * (hpitch + hwidth)

    npwr = 1 + math.floor(len(fp.rows) / 2)
    ngnd = math.ceil(len(fp.rows) / 2)

    # Vias connecting vdd straps to std cell stripes
    x = margin_w + vpitch + vwidth / 2
    y = margin_h
    for _ in range(n_vert // 2):
        if x < ram_x - ram_core_space:
            fp.place_vias(['vdd'] * npwr, x, y, 0, 2 * fp.std_cell_height, 'm3', 'via3_1600x480')
            fp.place_vias(['vdd'] * npwr, x, y, 0, 2 * fp.std_cell_height, 'm2', 'via2_1600x480')
            fp.place_vias(['vdd'] * npwr, x, y, 0, 2 * fp.std_cell_height, 'm1', 'via_1600x480')
        elif x > ram_x and x < ram_x + ram_w:
            fp.place_vias(['vdd'] * 2, x, ram_y + 5.63, 0, 405.28, 'm3', 'via3_1600x480')

        x += 2 * (vpitch + vwidth)

    # Vias connecting vss straps to std cell stripes
    x = margin_w + vpitch + vwidth / 2 + (vpitch + vwidth)
    y = margin_h + fp.std_cell_height
    for _ in range(n_vert // 2):
        if x < ram_x - ram_core_space:
            fp.place_vias(['vss'] * ngnd, x, y, 0, 2 * fp.std_cell_height, 'm3', 'via3_1600x480')
            fp.place_vias(['vss'] * ngnd, x, y, 0, 2 * fp.std_cell_height, 'm2', 'via2_1600x480')
            fp.place_vias(['vss'] * ngnd, x, y, 0, 2 * fp.std_cell_height, 'm1', 'via_1600x480')
        elif x > ram_x and x < ram_x + ram_w:
            fp.place_vias(['vss'] * 2, x, ram_y + 2.23, 0, 412.08, 'm3', 'via3_1600x480')

        x += 2 * (vpitch + vwidth)

    return fp

def generate_floorplan(chip):
    fp = Floorplan(chip)
    fp = setup_floorplan(fp, chip)
    fp.write_def('asic_core.def')
    fp.write_lef('asic_core.lef')
