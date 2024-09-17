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


def define_io_placement():
    io = [GPIO] * 9 + [VSSIO, VDDIO, VDD, VSS]

    return io, io, io, io


def generate_core_pins(chip):
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
    ea_pins = len(pins) * ea_pads.count(GPIO)
    for i in range(ea_pads.count(GPIO)):
        order_offset = len(pins) * i
        for pin_order, pin_spec in enumerate(pins):
            pin, bit, width = pin_spec
            # Construct name based on side, pin name, and bit # in vector
            name = f'we_{pin}[{i * width + bit}]'
            chip.set('constraint', 'pin', name, 'side', 1)
            chip.set('constraint', 'pin', name, 'order', ea_pins - (order_offset + pin_order))

    # Repeat the same logic for each of the other 3 sides, with positions/axes
    # adjusted accordingly...
    no_pins = len(pins) * no_pads.count(GPIO)
    for i in range(no_pads.count(GPIO)):
        order_offset = len(pins) * i
        for pin_order, pin_spec in enumerate(pins):
            pin, bit, width = pin_spec
            # Construct name based on side, pin name, and bit # in vector
            name = f'no_{pin}[{i * width + bit}]'
            chip.set('constraint', 'pin', name, 'side', 2)
            chip.set('constraint', 'pin', name, 'order', no_pins - (order_offset + pin_order))

    we_pins = len(pins) * we_pads.count(GPIO)
    for i in range(we_pads.count(GPIO)):
        order_offset = len(pins) * i
        for pin_order, pin_spec in enumerate(pins):
            pin, bit, width = pin_spec
            # Construct name based on side, pin name, and bit # in vector
            name = f'ea_{pin}[{i * width + bit}]'
            chip.set('constraint', 'pin', name, 'side', 3)
            chip.set('constraint', 'pin', name, 'order', we_pins - (order_offset + pin_order))

    so_pins = len(pins) * so_pads.count(GPIO)
    for i in range(so_pads.count(GPIO)):
        order_offset = len(pins) * i
        for pin_order, pin_spec in enumerate(pins):
            pin, bit, width = pin_spec
            # Construct name based on side, pin name, and bit # in vector
            name = f'so_{pin}[{i * width + bit}]'
            chip.set('constraint', 'pin', name, 'side', 4)
            chip.set('constraint', 'pin', name, 'order', so_pins - (order_offset + pin_order))


def __configure_padring_side(chip, side_pads, side_name):
    pad_name_prefix = f'padring.i{side_name}.ipad'
    pad_name_suffix = '.i0.'

    pad_name_map = {
        GPIO: ('gbidir', 'gpio'),
        VDD: ('gvdd', 'iovdd'),
        VDDIO: ('gvddio', 'iovddio'),
        VSS: ('gvss', 'iovss'),
        VSSIO: ('gvssio', 'iovssio')
    }

    for i, pad_type in enumerate(side_pads):
        pad_type_name, pad_type_inst = pad_name_map[pad_type]
        pad_name = fr'{pad_name_prefix}\[{i}\]*.{pad_type_name}{pad_name_suffix}{pad_type_inst}'
        chip.add('tool', 'openroad', 'task', 'floorplan', 'var', f'padring_{side_name}_name',
                 pad_name)


def configure_padring(chip):
    # Place pads
    padring_file = os.path.join(os.path.dirname(__file__), 'openroad', 'padring.tcl')
    chip.set('tool', 'openroad', 'task', 'floorplan', 'file', 'padring', padring_file)

    we_pads, no_pads, ea_pads, so_pads = define_io_placement()

    __configure_padring_side(chip, we_pads, 'west')
    __configure_padring_side(chip, no_pads, 'north')
    __configure_padring_side(chip, ea_pads, 'east')
    __configure_padring_side(chip, so_pads, 'south')


def generate_core_outline(chip):
    # Set up die area
    core_w = 1700
    core_h = 1200
    core_margin = 10
    diearea = [(0, 0), (core_w, core_h)]
    corearea = [(core_margin, core_margin), (core_w - core_margin, core_h - core_margin)]

    chip.set('constraint', 'outline', diearea)
    chip.set('constraint', 'corearea', corearea)


def generate_core_floorplan(chip):
    generate_core_outline(chip)
    generate_core_pins(chip)

    # Global connections
    for gc in ('global_connect_core.tcl',):
        gc_path = os.path.join(os.path.dirname(__file__),
                               'openroad',
                               gc)
        chip.add('tool', 'openroad', 'task', 'floorplan', 'file', 'global_connect', gc_path)

    # Define power grid
    for grid in ('pdngen_core_only.tcl', 'pdngen_sram.tcl'):
        pdngen_path = os.path.join(os.path.dirname(__file__),
                                   'openroad',
                                   grid)
        chip.add('tool', 'openroad', 'task', 'floorplan', 'file', 'pdn_config', pdngen_path)


def generate_top_outline(chip):
    # Create die area
    top_w = 2300
    top_h = 1800

    io_offset = 10
    core_offset = 220
    margin = core_offset + io_offset
    chip.set('constraint', 'outline', [(0, 0), (top_w, top_h)])
    chip.set('constraint', 'corearea', [(margin, margin), (top_w - margin, top_h - margin)])


def generate_top_placement(chip):
    # Place core
    chip.set('constraint', 'component', 'core', 'placement', (300, 300))


def generate_top_floorplan(chip):
    generate_top_outline(chip)
    generate_top_placement(chip)
    configure_padring(chip)

    # Global connections
    for gc in ('global_connect_core_top.tcl', 'global_connect_io.tcl'):
        gc_file = os.path.join(os.path.dirname(__file__), 'openroad', gc)
        chip.add('tool', 'openroad', 'task', 'floorplan', 'file', 'global_connect', gc_file)

    # Define power grid
    for grid in ('pdngen_top.tcl', 'pdngen_core.tcl'):
        pdngen_file = os.path.join(os.path.dirname(__file__), 'openroad', grid)
        chip.add('tool', 'openroad', 'task', 'floorplan', 'file', 'pdn_config', pdngen_file)


def generate_top_flat_floorplan(chip):
    generate_top_outline(chip)
    configure_padring(chip)

    # Global connections
    for gc in ('global_connect_core_top_flat.tcl', 'global_connect_io.tcl'):
        gc_file = os.path.join(os.path.dirname(__file__), 'openroad', gc)
        chip.add('tool', 'openroad', 'task', 'floorplan', 'file', 'global_connect', gc_file)

    # Define power grid
    for grid in ('pdngen_top.tcl', 'pdngen_sram.tcl'):
        pdngen_file = os.path.join(os.path.dirname(__file__), 'openroad', grid)
        chip.add('tool', 'openroad', 'task', 'floorplan', 'file', 'pdn_config', pdngen_file)
