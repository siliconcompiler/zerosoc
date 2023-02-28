from siliconcompiler import Chip

import math

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

def configure_chip(design):
    chip = Chip(design)
    chip.load_target('skywater130_demo')

    chip.load_lib('sky130sram')
    chip.load_lib('sky130io')
    chip.add('asic', 'macrolib', 'sky130sram')
    chip.add('asic', 'macrolib', 'sky130io')

    chip.set('option', 'showtool', 'def', 'klayout')
    chip.set('option', 'showtool', 'gds', 'klayout')

    return chip

def define_dimensions():
    place_w = 4860 * 0.46
    place_h = 648 * 2.72
    margin_left = 60 * 0.46
    margin_bottom = 10 * 2.72

    core_w = place_w + 2 * margin_left
    core_h = place_h + 2 * margin_bottom

    # Use math.ceil to ensure that top-level's dimensions are a whole number of
    # microns. This implicitly stretches out the top/right margins around the
    # placement area a bit.
    gpio_h = 0
    top_w = math.ceil(core_w + 2 * gpio_h)
    top_h = math.ceil(core_h + 2 * gpio_h)

    core_w = top_w - 2 * gpio_h
    core_h = top_h - 2 * gpio_h

    return (top_w, top_h), (core_w, core_h), (place_w, place_h), (margin_left, margin_bottom)

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

def define_io_placement(chip):
    we_io = [GPIO] * 5 + [VDD, VSS, VDDIO, VSSIO] + [GPIO] * 4
    no_io = [GPIO] * 9 + [VDDIO, VSSIO, VDD, VSS]
    ea_io = [GPIO] * 9 + [VDDIO, VSS, VDD, VSSIO]
    so_io = [GPIO] * 5 + [VDD, VSS, VDDIO, VSSIO] + [GPIO] * 4

    return we_io, no_io, ea_io, so_io

def core_floorplan(chip):
    ## Set up die area ##
    dims = define_dimensions()
    _, (core_w, core_h), (place_w, place_h), (margin_left, margin_bottom) = dims
    diearea = [(0, 0), (core_w, core_h)]
    corearea = [(margin_left, margin_bottom), (place_w + margin_left, place_h + margin_bottom)]

    chip.set('constraint', 'outline', diearea)
    chip.set('constraint', 'corearea', corearea)

    ## Place RAM macro ##
    # ram_w = fp.available_cells[RAM].width
    # ram_h = fp.available_cells[RAM].height
    # ram_x = fp.snap(place_w + margin_left - ram_w, 0.46)
    # # Add hand-calculated fudge factor to align left-side pins with routing tracks.
    # ram_y = place_h + margin_bottom - ram_h - 15 * 2.72 + 0.53

    instance_name = 'soc.ram.u_mem.gen_sky130.u_impl_sky130.gen32x512.mem'
    chip.set('constraint', 'component', instance_name, 'placement', [core_w / 2, core_h / 2, 0])
    chip.set('constraint', 'component', instance_name, 'rotation', '0')
    chip.set('constraint', 'component', instance_name, 'flip', 'false')

    ## Place pins ##
    pins = [
        # (name, offset from cell edge, # bit in vector, width of vector)
        ('din', 0, 1), # in
        ('dout', 0, 1), # out
        ('ie', 0, 1), # inp_dis
        ('oen', 0, 1), # oe_n
        ('tech_cfg', 0, 18), # hld_h_n
        ('tech_cfg', 1, 18), # enable_h
        ('tech_cfg', 2, 18), # enable_inp_h
        ('tech_cfg', 3, 18), # enable_vdda_h
        ('tech_cfg', 4, 18), # enable_vswitch_h
        ('tech_cfg', 5, 18), # enable_vddio
        ('tech_cfg', 6, 18), # ib_mode_sel
        ('tech_cfg', 7, 18), # vtrip_sel
        ('tech_cfg', 8, 18), # slow
        ('tech_cfg', 9, 18), # hld_ovr
        ('tech_cfg', 10, 18), # analog_en
        ('tech_cfg', 11, 18), # analog_sel
        ('tech_cfg', 12, 18), # analog_pol
        ('tech_cfg', 13, 18), # dm[0]
        ('tech_cfg', 14, 18), # dm[1]
        ('tech_cfg', 15, 18), # dm[2]
        ('tech_cfg', 16, 18), # tie_lo_esd
        ('tech_cfg', 17, 18), # tie_hi_esd
    ]

    we_pads, no_pads, ea_pads, so_pads = define_io_placement(chip)

    # gpio_w = fp.available_cells[GPIO].width
    # gpio_h = fp.available_cells[GPIO].height

    # Filter out GPIO pins
    for i, _ in enumerate([pad for pad in we_pads if pad == GPIO]):
        order_offset = len(pins) * i
        for pin_order, pin_spec in enumerate(pins):
            pin, bit, width = pin_spec
            # Construct name based on side, pin name, and bit # in vector
            name = f'we_{pin}[{i * width + bit}]'
            # Place pin!
            chip.set('constraint', 'pin', name, 'side', 1)
            chip.set('constraint', 'pin', name, 'order', order_offset + pin_order)

    # Repeat the same logic for each of the other 3 sides, with positions/axes
    # adjusted accordingly...
    for i, _ in enumerate([pad for pad in no_pads if pad == GPIO]):
        order_offset = len(pins) * i
        for pin_order, pin_spec in enumerate(pins):
            pin, bit, width = pin_spec
            # Construct name based on side, pin name, and bit # in vector
            name = f'no_{pin}[{i * width + bit}]'
            # Place pin!
            chip.set('constraint', 'pin', name, 'side', 2)
            chip.set('constraint', 'pin', name, 'order', order_offset + pin_order)

    for i, _ in enumerate([pad for pad in ea_pads if pad == GPIO]):
        order_offset = len(pins) * i
        for pin_order, pin_spec in enumerate(pins):
            pin, bit, width = pin_spec
            # Construct name based on side, pin name, and bit # in vector
            name = f'ea_{pin}[{i * width + bit}]'
            # Place pin!
            chip.set('constraint', 'pin', name, 'side', 3)
            chip.set('constraint', 'pin', name, 'order', order_offset + pin_order)

    for i, _ in enumerate([pad for pad in so_pads if pad == GPIO]):
        order_offset = len(pins) * i
        for pin_order, pin_spec in enumerate(pins):
            pin, bit, width = pin_spec
            # Construct name based on side, pin name, and bit # in vector
            name = f'so_{pin}[{i * width + bit}]'
            # Place pin!
            chip.set('constraint', 'pin', name, 'side', 4)
            chip.set('constraint', 'pin', name, 'order', order_offset + pin_order)

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


    ## Connections to vddio pins ##
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
    fp.place_macros([('corner_sw', CORNER)], 0, 0, 0, 0, 'S')
    fp.place_macros([('corner_nw', CORNER)], 0, top_h - corner_w, 0, 0, 'W')
    fp.place_macros([('corner_se', CORNER)], top_w - corner_h, 0, 0, 0, 'E')
    fp.place_macros([('corner_ne', CORNER)], top_w - corner_w, top_h - corner_h, 0, 0, 'N')

    ## Fill I/O ring ##
    fp.fill_io_region([(0, 0), (fill_cell_h, top_h)], FILL_CELLS, 'W', 'v')
    fp.fill_io_region([(0, top_h - fill_cell_h), (top_w, top_h)], FILL_CELLS, 'N', 'h')
    fp.fill_io_region([(top_w - fill_cell_h, 0), (top_w, top_h)], FILL_CELLS, 'E', 'v')
    fp.fill_io_region([(0, 0), (top_w, fill_cell_h)], FILL_CELLS, 'S', 'h')


    ## Place core ##
    fp.place_macros([('core', 'asic_core')], gpio_h, gpio_h, 0, 0, 'N')

def generate_core_floorplan(chip):
    core_floorplan(chip)


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
    stackup = chip.get('asic', 'stackup')
    core_chip.set('model', 'layout', 'lef', stackup, 'asic_core.lef')
    chip.import_library(core_chip)
    chip.add('asic', 'macrolib', 'asic_core')

    fp = Floorplan(chip)
    top_floorplan(fp)
    fp.write_def('asic_top.def')

if __name__ == '__main__':
  main()

