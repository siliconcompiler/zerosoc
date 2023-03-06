import os

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


def define_io_placement():
    we_io = [GPIO] * 5 + [VDD, VSS, VDDIO, VSSIO] + [GPIO] * 4
    no_io = [GPIO] * 9 + [VDDIO, VSSIO, VDD, VSS]
    ea_io = [GPIO] * 9 + [VDDIO, VSS, VDD, VSSIO]
    so_io = [GPIO] * 5 + [VDD, VSS, VDDIO, VSSIO] + [GPIO] * 4

    return we_io, no_io, ea_io, so_io


def generate_core_floorplan(chip):
    # Set up die area
    core_w = 1700
    core_h = 1200
    core_margin = 10
    diearea = [(0, 0), (core_w, core_h)]
    corearea = [(core_margin, core_margin), (core_w - core_margin, core_h - core_margin)]

    chip.set('constraint', 'outline', diearea)
    chip.set('constraint', 'corearea', corearea)

    # Place RAM macro
    instance_name = 'soc.ram.u_mem.gen_sky130.u_impl_sky130.gen32x512.mem'
    chip.set('constraint', 'component', instance_name, 'placement', [core_w / 2, core_h / 2, 0])

    # Place pins
    pins = [
        # (name, offset from cell edge, # bit in vector, width of vector)
        ('din', 0, 1),  # in
        ('dout', 0, 1),  # out
        ('ie', 0, 1),  # inp_dis
        ('oen', 0, 1),  # oe_n
        ('tech_cfg', 0, 18),  # hld_h_n
        ('tech_cfg', 1, 18),  # enable_h
        ('tech_cfg', 2, 18),  # enable_inp_h
        ('tech_cfg', 3, 18),  # enable_vdda_h
        ('tech_cfg', 4, 18),  # enable_vswitch_h
        ('tech_cfg', 5, 18),  # enable_vddio
        ('tech_cfg', 6, 18),  # ib_mode_sel
        ('tech_cfg', 7, 18),  # vtrip_sel
        ('tech_cfg', 8, 18),  # slow
        ('tech_cfg', 9, 18),  # hld_ovr
        ('tech_cfg', 10, 18),  # analog_en
        ('tech_cfg', 11, 18),  # analog_sel
        ('tech_cfg', 12, 18),  # analog_pol
        ('tech_cfg', 13, 18),  # dm[0]
        ('tech_cfg', 14, 18),  # dm[1]
        ('tech_cfg', 15, 18),  # dm[2]
        ('tech_cfg', 16, 18),  # tie_lo_esd
        ('tech_cfg', 17, 18),  # tie_hi_esd
    ]

    we_pads, no_pads, ea_pads, so_pads = define_io_placement()

    # Filter out GPIO pins
    for i, _ in enumerate([pad for pad in we_pads if pad == GPIO]):
        order_offset = len(pins) * i
        for pin_order, pin_spec in enumerate(pins):
            pin, bit, width = pin_spec
            # Construct name based on side, pin name, and bit # in vector
            name = f'we_{pin}[{i * width + bit}]'
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
            chip.set('constraint', 'pin', name, 'side', 2)
            chip.set('constraint', 'pin', name, 'order', order_offset + pin_order)

    for i, _ in enumerate([pad for pad in ea_pads if pad == GPIO]):
        order_offset = len(pins) * i
        for pin_order, pin_spec in enumerate(pins):
            pin, bit, width = pin_spec
            # Construct name based on side, pin name, and bit # in vector
            name = f'ea_{pin}[{i * width + bit}]'
            chip.set('constraint', 'pin', name, 'side', 3)
            chip.set('constraint', 'pin', name, 'order', order_offset + pin_order)

    for i, _ in enumerate([pad for pad in so_pads if pad == GPIO]):
        order_offset = len(pins) * i
        for pin_order, pin_spec in enumerate(pins):
            pin, bit, width = pin_spec
            # Construct name based on side, pin name, and bit # in vector
            name = f'so_{pin}[{i * width + bit}]'
            chip.set('constraint', 'pin', name, 'side', 4)
            chip.set('constraint', 'pin', name, 'order', order_offset + pin_order)

    # Global connections
    gc_path = os.path.join(os.path.dirname(__file__),
                           'openroad',
                           'global_connect.tcl')
    chip.set('tool', 'openroad', 'task', 'floorplan', 'file', 'global_connect', gc_path)

    # Define power grid
    pdngen_path = os.path.join(os.path.dirname(__file__),
                               'openroad',
                               'pdngen.tcl')
    chip.set('tool', 'openroad', 'task', 'floorplan', 'file', 'pdn_config', pdngen_path)


def configure_padring(chip):
    # Place pads
    padring_file = os.path.join(os.path.dirname(__file__), 'openroad', 'padring.tcl')
    chip.set('tool', 'openroad', 'task', 'floorplan', 'file', 'padring', padring_file)

    we_pads, no_pads, ea_pads, so_pads = define_io_placement()
    indices = {}
    indices[GPIO] = 0
    indices[VDD] = 0
    indices[VSS] = 0
    indices[VDDIO] = 0
    indices[VSSIO] = 0

    for pad_type in we_pads:
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
            pad_name = f'padring.we_pads\\[0\\].i0.pad{pin_name}\\[0\\].i0.io{pin_name}'

        chip.add('tool', 'openroad', 'task', 'floorplan', 'var', 'padring_west_name', pad_name)

    indices[GPIO] = 0
    for pad_type in no_pads:
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
            pad_name = f'padring.no_pads\\[0\\].i0.pad{pin_name}\\[0\\].i0.io{pin_name}'

        chip.add('tool', 'openroad', 'task', 'floorplan', 'var', 'padring_north_name', pad_name)

    indices[GPIO] = 0
    for pad_type in ea_pads:
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
            pad_name = f'padring.ea_pads\\[0\\].i0.pad{pin_name}\\[0\\].i0.io{pin_name}'

        chip.add('tool', 'openroad', 'task', 'floorplan', 'var', 'padring_east_name', pad_name)

    indices[GPIO] = 0
    for pad_type in so_pads:
        i = indices[pad_type]
        indices[pad_type] += 1
        if pad_type == GPIO:
            pad_name = f'padring.so_pads\\[0\\].i0.padio\\[{i}\\].i0.gpio'
        else:
            if pad_type == VDD:
                pin_name = 'vdd'
            elif pad_type == VSS:
                pin_name = 'vss'
            elif pad_type == VDDIO:
                pin_name = 'vddio'
            elif pad_type == VSSIO:
                pin_name = 'vssio'
            pad_name = f'padring.so_pads\\[0\\].i0.pad{pin_name}\\[0\\].i0.io{pin_name}'

        chip.add('tool', 'openroad', 'task', 'floorplan', 'var', 'padring_south_name', pad_name)


def generate_top_floorplan(chip):
    # Create die area
    top_w = 2300
    top_h = 1800

    io_offset = 10
    core_offset = 220
    margin = core_offset + io_offset
    chip.set('constraint', 'outline', [(0, 0), (top_w, top_h)])
    chip.set('constraint', 'corearea', [(margin, margin), (top_w - margin, top_h - margin)])

    # Place pads
    configure_padring(chip)

    # Global connections
    gc_file = os.path.join(os.path.dirname(__file__), 'openroad', 'global_connect_top.tcl')
    chip.set('tool', 'openroad', 'task', 'floorplan', 'file', 'global_connect', gc_file)

    # Define power grid
    pdngen_file = os.path.join(os.path.dirname(__file__), 'openroad', 'pdngen_top.tcl')
    chip.set('tool', 'openroad', 'task', 'floorplan', 'file', 'pdn_config', pdngen_file)

    # Place core
    chip.set('constraint', 'component', 'core', 'placement', [top_w / 2, top_h / 2, 0])
