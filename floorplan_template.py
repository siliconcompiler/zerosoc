from siliconcompiler.core import Chip
from siliconcompiler.floorplan import Floorplan

import math

#@ begin macro_names
GPIO = 'sky130_ef_io__gpiov2_pad_wrapped'
VDD = 'sky130_ef_io__vccd_hvc_pad'
VDDIO = 'sky130_ef_io__vddio_hvc_pad'
VSS = 'sky130_ef_io__vssd_hvc_pad'
VSSIO = 'sky130_ef_io__vssio_hvc_pad'
CORNER = 'sky130_ef_io__corner_pad'
FILL_CELLS = ['sky130_ef_io__com_bus_slice_1um',
              'sky130_ef_io__com_bus_slice_5um',
              'sky130_ef_io__com_bus_slice_10um',
              'sky130_ef_io__com_bus_slice_20um']

RAM = 'sky130_sram_2kbyte_1rw1r_32x512_8'
#@ end macro_names

#@ begin configure_chip
def configure_chip(design):
    #@ begin configure_chip_target
    chip = Chip()
    chip.target('skywater130')
    #@ end configure_chip_target

    #@ begin configure_chip_design
    chip.set('design', design)
    #@ end configure_chip_design

    #@ begin configure_chip_macro
    libname = 'ram'
    chip.add('library', libname, 'nldm', 'typical', 'lib', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    chip.add('library', libname, 'lef', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    chip.add('library', libname, 'gds', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds')
    #@ end configure_chip_macro
    #@ begin configure_chip_macrolib
    chip.add('asic', 'macrolib', libname)
    #@ end configure_chip_macrolib
    #@ begin configure_chip_type
    chip.set('library', libname, 'type', 'component')
    #@ end configure_chip_type

    libname = 'io'
    chip.add('library', libname, 'nldm', 'typical', 'lib', 'asic/sky130/io/sky130_dummy_io.lib')
    chip.set('library', libname, 'lef', 'asic/sky130/io/sky130_ef_io.lef')
    # Need both GDS files: "ef" relies on "fd"
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_ef_io.gds')
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_fd_io.gds')
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'type', 'component')

    chip.set('showtool', 'def', 'klayout')
    chip.set('showtool', 'gds', 'klayout')

    return chip
#@ end configure_chip

#@ begin define_dimensions
#@ begin define_dimensions_prototype
def define_dimensions(fp):
#@ end define_dimensions_prototype
    #@ begin place_dims
    place_w = 4860 * fp.stdcell_width
    place_h = 648 * fp.stdcell_height
    margin_left = 60 * fp.stdcell_width
    margin_bottom = 10 * fp.stdcell_height
    #@ end place_dims

    #@ begin core
    core_w = place_w + 2 * margin_left
    core_h = place_h + 2 * margin_bottom
    #@ end core

    # Use math.ceil to ensure that top-level's dimensions are a whole number of
    # microns. This implicitly stretches out the top/right margins around the
    # placement area a bit.
    #@ begin top
    gpio_h = fp.available_cells[GPIO].height
    top_w = math.ceil(core_w + 2 * gpio_h)
    top_h = math.ceil(core_h + 2 * gpio_h)
    #@ end top

    #@ begin core_stretch
    core_w = top_w - 2 * gpio_h
    core_h = top_h - 2 * gpio_h
    #@ end core_stretch

    return (top_w, top_h), (core_w, core_h), (place_w, place_h), (margin_left, margin_bottom)
#@ end define_dimensions

#@ begin calculate_even_spacing
def calculate_even_spacing(fp, pads, distance, start):
    n = len(pads)
    pads_width = sum(fp.available_cells[pad].width for pad in pads)
    spacing = (distance - pads_width) // (n + 1)

    pos = start + spacing
    io_pos = []
    for pad in pads:
        io_pos.append((pad, pos))
        pos += fp.available_cells[pad].width + spacing

    return io_pos
#@ end calculate_even_spacing

#@ begin define_io_placement
#@ begin iolist
def define_io_placement(fp):
    we_io = [GPIO] * 5 + [VDD, VSS, VDDIO, VSSIO] + [GPIO] * 4
    no_io = [GPIO] * 9 + [VDDIO, VSSIO, VDD, VSS]
    ea_io = [GPIO] * 9 + [VDDIO, VSS, VDD, VSSIO]
    so_io = [GPIO] * 5 + [VDD, VSS, VDDIO, VSSIO] + [GPIO] * 4
    #@ end iolist

    (top_w, top_h), _, _, _ = define_dimensions(fp)
    corner_w = fp.available_cells[CORNER].width
    corner_h = fp.available_cells[CORNER].height

    we_io_pos = calculate_even_spacing(fp, we_io, top_h - corner_h - corner_w, corner_h)
    so_io_pos = calculate_even_spacing(fp, so_io, top_w - corner_h - corner_w, corner_w)

    # For east and north, we crowd GPIO on the first half of the side to make
    # sure we don't run into routing congestion issues due to the RAM in the
    # top-right corner.
    mid_w = (top_w - corner_h - corner_w) // 2
    no_io_pos = (calculate_even_spacing(fp, no_io[:9], mid_w, corner_h) +
                 calculate_even_spacing(fp, no_io[9:], mid_w, mid_w + corner_h))
    mid_h = (top_h - corner_h - corner_w) // 2
    ea_io_pos = (calculate_even_spacing(fp, ea_io[:9], mid_h, corner_w) +
                 calculate_even_spacing(fp, ea_io[9:], mid_h, mid_h + corner_w))

    return we_io_pos, no_io_pos, ea_io_pos, so_io_pos
#@ end define_io_placement


def core_floorplan(fp):
    ## Set up die area ##
    #@ begin die_area
    dims = define_dimensions(fp)
    _, (core_w, core_h), (place_w, place_h), (margin_left, margin_bottom) = dims
    diearea = [(0, 0), (core_w, core_h)]
    corearea = [(margin_left, margin_bottom), (place_w + margin_left, place_h + margin_bottom)]
    fp.create_diearea(diearea, corearea=corearea)
    #@ end die_area
    #@ screenshot die_area.png

    ## Place RAM macro ##
    #@ begin ram_placement
    ram_w = fp.available_cells[RAM].width
    ram_h = fp.available_cells[RAM].height
    ram_x = place_w + margin_left - ram_w
    ram_y = place_h + margin_bottom - ram_h
    instance_name = 'soc.ram.u_mem.gen_sky130.u_impl_sky130.gen32x512.mem'
    fp.place_macros([(instance_name, RAM)], ram_x, ram_y, 0, 0, 'N', snap=True)
    #@ end ram_placement

    #@ begin blockage_placement
    ram_margin_x = 120 * fp.stdcell_width
    ram_margin_y = 20 * fp.stdcell_height
    blockage_x = ram_x - ram_margin_x
    blockage_y = ram_y - ram_margin_y
    blockage_w = ram_w + ram_margin_x
    blockage_h = ram_h + ram_margin_y
    fp.place_blockage(blockage_x, blockage_y, blockage_w, blockage_h)
    #@ end blockage_placement
    #@ screenshot ram.png

    ## Place pins ##
    #@ begin pin_data
    pins = [
        # (name, offset from cell edge, # bit in vector, width of vector)
        ('din', 75.085, 0, 1), # in
        ('dout', 19.885, 0, 1), # out
        ('ie', 41.505, 0, 1), # inp_dis
        ('oen', 4.245, 0, 1), # oe_n
        ('tech_cfg', 31.845, 0, 18), # hld_h_n
        ('tech_cfg', 35.065, 1, 18), # enable_h
        ('tech_cfg', 38.285, 2, 18), # enable_inp_h
        ('tech_cfg', 13.445, 3, 18), # enable_vdda_h
        ('tech_cfg', 16.665, 4, 18), # enable_vswitch_h
        ('tech_cfg', 69.105, 5, 18), # enable_vddio
        ('tech_cfg',  7.465, 6, 18), # ib_mode_sel
        ('tech_cfg', 10.685, 7, 18), # vtrip_sel
        ('tech_cfg', 65.885, 8, 18), # slow
        ('tech_cfg', 22.645, 9, 18), # hld_ovr
        ('tech_cfg', 50.705, 10, 18), # analog_en
        ('tech_cfg', 29.085, 11, 18), # analog_sel
        ('tech_cfg', 44.265, 12, 18), # analog_pol
        ('tech_cfg', 47.485, 13, 18), # dm[0]
        ('tech_cfg', 56.685, 14, 18), # dm[1]
        ('tech_cfg', 25.865, 15, 18), # dm[2]
        ('tech_cfg', 78.305, 16, 18), # tie_lo_esd
        ('tech_cfg', 71.865, 17, 18), # tie_hi_esd
    ]
    pin_width = 0.28
    pin_depth = 1
    pin_layer = 'm2'
    #@ end pin_data

    #@ begin pin_loops
    we_pads, no_pads, ea_pads, so_pads = define_io_placement(fp)

    gpio_w = fp.available_cells[GPIO].width
    gpio_h = fp.available_cells[GPIO].height

    # Filter out GPIO pins
    we_gpio_pos = [pos for pad, pos in we_pads if pad == GPIO]
    # Constant x position for west side
    pin_x = 0
    for i, pad_y in enumerate(we_gpio_pos):
        pad_y -= gpio_h # account for padring height
        for pin, offset, bit, width in pins:
            # Construct name based on side, pin name, and bit # in vector
            name = f'we_{pin}[{i * width + bit}]'
            # Calculate pin position based on cell and offset
            pin_y = pad_y + offset
            # Place pin!
            fp.place_pins([name], pin_x, pin_y, 0, 0, pin_depth, pin_width, pin_layer)

    # Repeat the same logic for each of the other 3 sides, with positions/axes
    # adjusted accordingly...
    no_gpio_pos = [pos for pad, pos in no_pads if pad == GPIO]
    pin_y = core_h - pin_depth
    for i, pad_x in enumerate(no_gpio_pos):
        pad_x -= gpio_h
        for pin, offset, bit, width in pins:
            name = f'no_{pin}[{i * width + bit}]'
            pin_x = pad_x + offset
            fp.place_pins([name], pin_x, pin_y, 0, 0, pin_width, pin_depth, pin_layer)

    ea_gpio_pos = [pos for pad, pos in ea_pads if pad == GPIO]
    pin_x = core_w - pin_depth
    for i, pad_y in enumerate(ea_gpio_pos):
        pad_y -= gpio_h
        for pin, offset, bit, width in pins:
            name = f'ea_{pin}[{i * width + bit}]'
            pin_y = pad_y + gpio_w - offset - pin_width
            fp.place_pins([name], pin_x, pin_y, 0, 0, pin_depth, pin_width, pin_layer)

    so_gpio_pos = [pos for pad, pos in so_pads if pad == GPIO]
    pin_y = 0
    for i, pad_x in enumerate(so_gpio_pos):
        pad_x -= gpio_h
        for pin, offset, bit, width in pins:
            name = f'so_{pin}[{i * width + bit}]'
            pin_x = pad_x + gpio_w - offset - pin_width
            fp.place_pins([name], pin_x, pin_y, 0, 0, pin_width, pin_depth, pin_layer)
    #@ end pin_loops
    #@ def pins.def

    ## Place PDN ##
    #@ begin place_pdn_call
    place_pdn(fp, ram_x, ram_y, ram_margin_x)
    #@ end place_pdn_call

#@ begin place_pdn_def
def place_pdn(fp, ram_x, ram_y, ram_margin):
    dims = define_dimensions(fp)
    _, (core_w, core_h), (place_w, place_h), (margin_left, margin_bottom) = dims
    we_pads, no_pads, ea_pads, so_pads = define_io_placement(fp)
    #@ end place_pdn_def

    #@ begin pdn_config
    n_vert = 8 # how many vertical straps to place
    vwidth = 5 # width of vertical straps in microns
    n_hori = 10 # how many horizontal straps to place
    hwidth = 5 # width of horizontal straps
    vlayer = 'm4' # metal layer for vertical straps
    hlayer = 'm5' # metal layer for horizontal straps

    # Calculate even spacing for straps
    vpitch = ((ram_x - ram_margin - margin_left) - n_vert * vwidth) / (n_vert + 1)
    hpitch = (core_h - n_hori * hwidth) / (n_hori + 1)
    #@ end pdn_config

    #@ begin pdn_add_nets
    fp.add_net('_vdd', ['VPWR', 'vccd1'], 'power')
    fp.add_net('_vss', ['VGND', 'vssd1'], 'ground')
    #@ end pdn_add_nets

    #@ begin pdn_place_ring
    vss_ring_left = margin_left - 4 * vwidth
    vss_ring_bottom = margin_bottom - 4 * hwidth
    vss_ring_width = place_w + 9 * vwidth
    vss_ring_height = place_h + 9 * hwidth
    vss_ring_right = vss_ring_left + vss_ring_width
    vss_ring_top = vss_ring_bottom + vss_ring_height

    vdd_ring_left = vss_ring_left + 2 * vwidth
    vdd_ring_bottom = vss_ring_bottom + 2 * hwidth
    vdd_ring_width = vss_ring_width - 4 * vwidth
    vdd_ring_height = vss_ring_height - 4 * hwidth
    vdd_ring_right = vdd_ring_left + vdd_ring_width
    vdd_ring_top = vdd_ring_bottom + vdd_ring_height

    fp.place_ring('_vdd', vdd_ring_left, vdd_ring_bottom, vdd_ring_width,
                  vdd_ring_height, hwidth, vwidth, hlayer, vlayer)
    fp.place_ring('_vss', vss_ring_left, vss_ring_bottom, vss_ring_width,
                  vss_ring_height, hwidth, vwidth, hlayer, vlayer)
    #@ end pdn_place_ring
    #@ screenshot pdn_ring.png

    #@ begin pdn_power_straps
    # Horizontal stripes
    spacing = 2 * (hpitch + hwidth)

    bottom = margin_bottom + hpitch
    fp.place_wires(['_vdd'] * (n_hori // 2), vdd_ring_left, bottom, 0, spacing,
                   vdd_ring_width, hwidth, hlayer, shape='stripe')

    bottom = margin_bottom + hpitch + (hpitch + hwidth)
    fp.place_wires(['_vss'] * (n_hori // 2), vss_ring_left, bottom, 0, spacing,
                   vss_ring_width, hwidth, hlayer, shape='stripe')

    # Vertical stripes
    spacing = 2 * (vpitch + vwidth)

    left = margin_left + vpitch
    fp.place_wires(['_vdd'] * (n_vert // 2), left, vdd_ring_bottom, spacing, 0,
                   vwidth, vdd_ring_height, vlayer, shape='stripe')

    left = margin_left + vpitch + (vpitch + vwidth)
    fp.place_wires(['_vss'] * (n_vert // 2), left, vss_ring_bottom, spacing, 0,
                   vwidth, vss_ring_height, vlayer, shape='stripe')
    #@ end pdn_power_straps
    #@ screenshot power_straps.png

    #@ begin power_pad_connections
    gpio_h = fp.available_cells[GPIO].height
    pow_h = fp.available_cells[VDD].height
    # account for GPIO padcells being larger than power padcells
    pow_gap = gpio_h - pow_h

    pin_width = 23.9
    pin_offsets = (0.495, 50.39)

    # Place wires/pins connecting power pads to the power ring
    for pad_type, y in we_pads:
        y -= gpio_h
        for offset in pin_offsets:
            if pad_type == VDD:
                fp.place_wires(['_vdd'], -pow_gap, y + offset, 0, 0,
                               vdd_ring_left + vwidth + pow_gap, pin_width, 'm3')
                fp.place_pins (['_vdd'], 0, y + offset, 0, 0,
                               vdd_ring_left + vwidth, pin_width, 'm3', use='power')
            elif pad_type == VDDIO:
                fp.place_pins (['_vddio'], 0, y + offset, 0, 0,
                               margin_left, pin_width, 'm3')
            elif pad_type == VSS:
                fp.place_wires(['_vss'], -pow_gap, y + offset, 0, 0,
                               vss_ring_left + vwidth + pow_gap, pin_width, 'm3')
                fp.place_pins(['_vss'], 0, y + offset, 0, 0,
                              vss_ring_left + vwidth, pin_width, 'm3', use='power')

    for pad_type, x in no_pads:
        x -= gpio_h
        for offset in pin_offsets:
            if pad_type == VDD:
                fp.place_wires(['_vdd'], x + offset, vdd_ring_top - hwidth, 0, 0,
                               pin_width, core_h - vdd_ring_top + hwidth + pow_gap, 'm3')
                fp.place_pins(['_vdd'], x + offset, vdd_ring_top - hwidth, 0, 0,
                              pin_width, core_h - vdd_ring_top + hwidth, 'm3', use='power')
            elif pad_type == VDDIO:
                fp.place_pins(['_vddio'], x + offset, margin_bottom + place_h, 0, 0,
                              pin_width, core_h - (margin_bottom + place_h), 'm3')
            elif pad_type == VSS:
                fp.place_wires(['_vss'], x + offset, vss_ring_top - hwidth, 0, 0,
                               pin_width, core_h - vss_ring_top + hwidth + pow_gap, 'm3')
                fp.place_pins(['_vss'], x + offset, vss_ring_top - hwidth, 0, 0,
                              pin_width, core_h - vss_ring_top + hwidth, 'm3', use='power')

    for pad_type, y in ea_pads:
        y -= gpio_h
        pad_w = fp.available_cells[pad_type].width
        for offset in pin_offsets:
            if pad_type == VDD:
                fp.place_wires(['_vdd'], vdd_ring_right - vwidth, y + pad_w - offset - pin_width, 0, 0,
                               core_w - vdd_ring_right + vwidth + pow_gap, pin_width, 'm3')
                fp.place_pins(['_vdd'], vdd_ring_right - vwidth, y + pad_w - offset - pin_width, 0, 0,
                              core_w - vdd_ring_right + vwidth, pin_width, 'm3', use='power')
            elif pad_type == VDDIO:
                fp.place_pins(['_vddio'], margin_left + place_w, y + pad_w - offset - pin_width, 0, 0,
                              core_w - (margin_left + place_w), pin_width, 'm3')
            elif pad_type == VSS:
                fp.place_wires(['_vss'], vss_ring_right - vwidth, y + pad_w - offset - pin_width, 0, 0,
                               core_w - vss_ring_right + vwidth + pow_gap, pin_width, 'm3')
                fp.place_pins(['_vss'], vss_ring_right - vwidth, y + pad_w - offset - pin_width, 0, 0,
                              core_w - vss_ring_right + vwidth, pin_width, 'm3', use='power')

    for pad_type, x in so_pads:
        x -= gpio_h
        pad_w = fp.available_cells[pad_type].width
        for offset in pin_offsets:
            if pad_type == VDD:
                fp.place_wires(['_vdd'], x + pad_w - offset - pin_width, -pow_gap, 0, 0,
                               pin_width, vdd_ring_bottom + hwidth + pow_gap, 'm3')
                fp.place_pins(['_vdd'], x + pad_w - offset - pin_width, 0, 0, 0,
                              pin_width, vdd_ring_bottom + hwidth, 'm3', use='power')
            elif pad_type == VDDIO:
                fp.place_pins(['_vddio'], x + pad_w - offset - pin_width, 0, 0, 0,
                              pin_width, margin_bottom, 'm3')
            elif pad_type == VSS:
                fp.place_wires(['_vss'], x + pad_w - offset - pin_width, -pow_gap, 0, 0,
                               pin_width, vss_ring_bottom + hwidth + pow_gap, 'm3')
                fp.place_pins(['_vss'], x + pad_w - offset - pin_width, 0, 0, 0,
                              pin_width, vss_ring_bottom + hwidth, 'm3', use='power')
    #@ end power_pad_connections
    #@ def power_pins.def


    #@ begin stdcell_straps
    rows_below_ram = (ram_y - margin_bottom) // fp.stdcell_height
    rows_above_ram = len(fp.rows) - rows_below_ram

    npwr_below = 1 + math.floor(rows_below_ram / 2)
    ngnd_below = math.ceil(rows_below_ram / 2)

    npwr_above = 1 + math.floor(rows_above_ram / 2)
    ngnd_above = math.ceil(rows_above_ram / 2)

    stripe_w = 0.48
    spacing = 2 * fp.stdcell_height

    bottom = margin_bottom - stripe_w/2
    fp.place_wires(['_vdd'] * npwr_below, margin_left, bottom, 0, spacing,
                   place_w, stripe_w, 'm1', 'followpin')

    bottom = margin_bottom - stripe_w/2 + fp.stdcell_height
    fp.place_wires(['_vss'] * ngnd_below, margin_left, bottom, 0, spacing,
                   place_w, stripe_w, 'm1', 'followpin')

    bottom = margin_bottom - stripe_w/2 + npwr_below * 2 * fp.stdcell_height
    fp.place_wires(['_vdd'] * npwr_above, margin_left, bottom, 0, spacing,
                   ram_x - 2 * margin_left, stripe_w, 'm1', 'followpin')

    bottom = margin_bottom - stripe_w/2 + fp.stdcell_height + ngnd_below * 2 * fp.stdcell_height
    fp.place_wires(['_vss'] * ngnd_above, margin_left, bottom, 0, spacing,
                   ram_x - 2 * margin_left, stripe_w, 'm1', 'followpin')
    #@ end stdcell_straps

    #@ begin ram_power_pins
    ram_x = fp.snap(ram_x, fp.stdcell_width)
    ram_y = fp.snap(ram_y, fp.stdcell_height)

    ram_vdd_pin_bottom = 4.76
    ram_vdd_pins_left = (4.76, 676.6)
    ram_vdd_pins_width = 6.5 - 4.76
    ram_vdd_pins_height = 411.78 - 4.76
    for x_offset in ram_vdd_pins_left:
        fp.place_wires(['_vdd'], ram_x + x_offset, ram_y + ram_vdd_pin_bottom,
                       0, 0, ram_vdd_pins_width, ram_vdd_pins_height, 'm4')

    ram_vss_pin_bottom = 1.36
    ram_vss_pins_left = (1.36, 680)
    ram_vss_pins_width = 3.1 - 1.36
    ram_vss_pins_height = 415.18 - 1.36
    for x_offset in ram_vss_pins_left:
        fp.place_wires(['_vss'], ram_x + x_offset, ram_y + ram_vss_pin_bottom,
                       0, 0, ram_vss_pins_width, ram_vss_pins_height, 'm4')
    #@ end ram_power_pins

    #@ begin insert_vias
    fp.insert_vias(layers=[('m1', 'm4'), ('m3', 'm4'), ('m3', 'm5'), ('m4', 'm5')])
    #@ end insert_vias

    #@ screenshot complete_pdn.png
    #@ def complete_pdn_zoom.def

#@ begin top_floorplan
def top_floorplan(fp):
    ## Create die area ##
    (top_w, top_h), (core_w, core_h), (place_w, place_h), (margin_left, margin_bottom) = define_dimensions(fp)
    fp.create_diearea([(0, 0), (top_w, top_h)])

    ## Place pads ##
    we_pads, no_pads, ea_pads, so_pads = define_io_placement(fp)
    indices = {}
    indices[GPIO] = 0
    indices[VDD] = 0
    indices[VSS] = 0
    indices[VDDIO] = 0
    indices[VSSIO] = 0

    gpio_h = fp.available_cells[GPIO].height
    pow_h = fp.available_cells[VDD].height
    corner_w = fp.available_cells[CORNER].width
    corner_h = fp.available_cells[CORNER].height
    fill_cell_h = fp.available_cells[FILL_CELLS[0]].height

    pin_dim = 10
    # Calculate where to place pin based on hardcoded GPIO pad pin location
    pin_offset_width = (11.2 + 73.8) / 2 - pin_dim / 2
    pin_offset_depth = gpio_h - ((102.525 + 184.975) / 2 - pin_dim / 2)

    #@ begin place_pads_loop
    for pad_type, y in we_pads:
        i = indices[pad_type]
        indices[pad_type] += 1
        if pad_type == GPIO:
            pad_name = f'padring.we_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio'
            pin_name = f'we_pad[{i}]'
        else:
            if pad_type == VDD:
                pin_name = 'vdd'
            elif pad_type == VSS:
                pin_name = 'vss'
            elif pad_type == VDDIO:
                pin_name = 'vddio'
            elif pad_type == VSSIO:
                pin_name = 'vssio'
            pad_name = f'{pin_name}{i}'

        fp.place_macros([(pad_name, pad_type)], 0, y, 0, 0, 'W')
        fp.place_pins([pin_name], pin_offset_depth, y + pin_offset_width,
                      0, 0, pin_dim, pin_dim, 'm5')
    #@ end place_pads_loop

    indices[GPIO] = 0
    for pad_type, x in no_pads:
        i = indices[pad_type]
        indices[pad_type] += 1
        if pad_type == GPIO:
            pad_name = f'padring.no_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio'
            pin_name = f'no_pad[{i}]'
        else:
            if pad_type == VDD:
                pin_name = 'vdd'
            elif pad_type == VSS:
                pin_name = 'vss'
            elif pad_type == VDDIO:
                pin_name = 'vddio'
            elif pad_type == VSSIO:
                pin_name = 'vssio'
            pad_name = f'{pin_name}{i}'

        pad_h = fp.available_cells[pad_type].height
        fp.place_macros([(pad_name, pad_type)], x, top_h - pad_h, 0, 0, 'N')
        fp.place_pins([pin_name], x + pin_offset_width, top_h - pin_offset_depth,
                      0, 0, pin_dim, pin_dim, 'm5')

    indices[GPIO] = 0
    for pad_type, y in ea_pads:
        i = indices[pad_type]
        indices[pad_type] += 1
        if pad_type == GPIO:
            pad_name = f'padring.ea_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio'
            pin_name = f'ea_pad[{i}]'
        else:
            if pad_type == VDD:
                pin_name = 'vdd'
            elif pad_type == VSS:
                pin_name = 'vss'
            elif pad_type == VDDIO:
                pin_name = 'vddio'
            elif pad_type == VSSIO:
                pin_name = 'vssio'
            pad_name = f'{pin_name}{i}'

        pad_h = fp.available_cells[pad_type].height
        fp.place_macros([(pad_name, pad_type)], top_w - pad_h, y, 0, 0, 'E')
        fp.place_pins([pin_name], top_w - pin_offset_depth, y + pin_offset_width,
                      0, 0, pin_dim, pin_dim, 'm5')


    indices[GPIO] = 0
    for pad_type, x in so_pads:
        i = indices[pad_type]
        indices[pad_type] += 1
        if pad_type == GPIO:
            pad_name = f'padring.so_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio'
            pin_name = f'so_pad[{i}]'
        else:
            if pad_type == VDD:
                pin_name = 'vdd'
            elif pad_type == VSS:
                pin_name = 'vss'
            elif pad_type == VDDIO:
                pin_name = 'vddio'
            elif pad_type == VSSIO:
                pin_name = 'vssio'
            pad_name = f'{pin_name}{i}'

        fp.place_macros([(pad_name, pad_type)], x, 0, 0, 0, 'S')
        fp.place_pins([pin_name], x + pin_offset_width, pin_offset_depth,
                       0, 0, pin_dim, pin_dim, 'm5')

    #@ screenshottop unfilled_padring.png

    # Connections to vddio pins
    pin_width = 23.9
    pin_offsets = (0.495, 50.39)

    pad_h = fp.available_cells[VDDIO].height
    pow_gap = fp.available_cells[GPIO].height - pad_h

    # Place wires/pins connecting power pads to the power ring
    fp.add_net('_vddio', [], 'power')
    for pad_type, y in we_pads:
        if pad_type == VDDIO:
            for offset in pin_offsets:
                fp.place_wires (['_vddio'], pad_h, y + offset, 0, 0,
                                margin_left + pow_gap, pin_width, 'm3')

    margin_top = core_h - (margin_bottom + place_h)
    for pad_type, x in no_pads:
        if pad_type == VDDIO:
            for offset in pin_offsets:
                fp.place_wires (['_vddio'], x + offset, top_h - pad_h - (margin_top + pow_gap), 0, 0,
                                pin_width, margin_top + pow_gap, 'm3')

    margin_right = core_w - (margin_left + place_w)
    for pad_type, y in ea_pads:
        if pad_type == VDDIO:
            for offset in pin_offsets:
                fp.place_wires (['_vddio'], top_w - pad_h - (margin_right + pow_gap), y + offset, 0, 0,
                                margin_right + pow_gap, pin_width, 'm3')

    for pad_type, x in so_pads:
        if pad_type == VDDIO:
            for offset in pin_offsets:
                fp.place_wires (['_vddio'], x + offset, pad_h, 0, 0,
                                pin_width, margin_bottom + pow_gap, 'm3')

    ## Place corner cells ##
    #@ begin place_macros
    fp.place_macros([('corner_sw', CORNER)], 0, 0, 0, 0, 'S')
    fp.place_macros([('corner_nw', CORNER)], 0, top_h - corner_w, 0, 0, 'W')
    fp.place_macros([('corner_se', CORNER)], top_w - corner_h, 0, 0, 0, 'E')
    fp.place_macros([('corner_ne', CORNER)], top_w - corner_w, top_h - corner_h, 0, 0, 'N')
    #@ end place_macros

    ## Fill I/O ring ##
    #@ begin fill_io
    fp.fill_io_region([(0, 0), (fill_cell_h, top_h)], FILL_CELLS, 'W', 'v')
    fp.fill_io_region([(0, top_h - fill_cell_h), (top_w, top_h)], FILL_CELLS, 'N', 'h')
    fp.fill_io_region([(top_w - fill_cell_h, 0), (top_w, top_h)], FILL_CELLS, 'E', 'v')
    fp.fill_io_region([(0, 0), (top_w, fill_cell_h)], FILL_CELLS, 'S', 'h')
    #@ end fill_io

    #@ screenshottop padring.png
    #@ deftop filled.def

    ## Place core ##
    #@ begin place_core
    fp.place_macros([('core', 'asic_core')], gpio_h, gpio_h, 0, 0, 'N')
    #@ end place_core
#@ end top_floorplan

def generate_core_floorplan(chip):
    fp = Floorplan(chip)
    core_floorplan(fp)
    fp.write_def('asic_core.def')
    fp.write_lef('asic_core.lef')

def generate_top_floorplan(chip):
    fp = Floorplan(chip)
    top_floorplan(fp)
    fp.write_def('asic_top.def')

def main():
    core_chip = configure_chip('asic_core')
    core_chip.write_manifest('sc_manifest.json')
    core_fp = Floorplan(core_chip)
    core_floorplan(core_fp)
    core_fp.write_def('asic_core.def')
    core_fp.write_lef('asic_core.lef')

    chip = configure_chip('asic_top')

    # Add asic_core as library
    libname = 'asic_core'
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'type', 'component')
    chip.set('library', libname, 'lef', 'asic_core.lef')

    fp = Floorplan(chip)
    top_floorplan(fp)
    fp.write_def('asic_top.def')

if __name__ == '__main__':
  main()
