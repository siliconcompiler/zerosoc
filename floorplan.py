from siliconcompiler.core import Chip
from siliconcompiler.floorplan import Floorplan

import math

GPIO = 'sky130_ef_io__gpiov2_pad'
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
    chip = Chip()
    chip.target('skywater130')

    chip.set('design', design)

    libname = 'ram'
    chip.add('library', libname, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    chip.add('library', libname, 'lef', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    chip.add('library', libname, 'gds', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds')
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'type', 'component')

    libname = 'io'
    chip.add('library', libname, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/io/sky130_dummy_io.lib')
    chip.set('library', libname, 'lef', 'asic/sky130/io/sky130_ef_io.lef')
    # Need both GDS files: ef relies on fd one
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_ef_io.gds')
    chip.add('library', libname, 'gds', 'asic/sky130/io/sky130_fd_io.gds')
    chip.add('asic', 'macrolib', libname)
    chip.set('library', libname, 'type', 'component')

    return chip

def define_dimensions(fp):
    place_w = 3375 * fp.std_cell_width
    place_h = 450 * fp.std_cell_height
    margin_left = 60 * fp.std_cell_width
    margin_bottom = 10 * fp.std_cell_height

    core_w = place_w + 2 * margin_left
    core_h = place_h + 2 * margin_bottom

    # GPIO is largest I/O cell, so its height is the height of each side of the
    # padring
    gpio_h = fp.available_cells[GPIO].height

    # Use math.ceil to ensure that chip's dimensions are whole microns, so we can
    # fill with I/O fill cells (this implicitly stretches our top/right margins a
    # bit to make this work out -- i.e. the place area is not entirely centered
    # within the core, but you can't tell)
    top_w = math.ceil(core_w + 2 * gpio_h)
    top_h = math.ceil(core_h + 2 * gpio_h)

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

def define_io_placement(fp):
    (top_w, top_h), _, _, _ = define_dimensions(fp)
    corner_w = fp.available_cells[CORNER].width
    corner_h = fp.available_cells[CORNER].height

    we_io = [GPIO] * 5 + [VDD, VSS, VDDIO, VSSIO] + [GPIO] * 4
    no_io = [GPIO] * 9 + [VDD, VSS, VDDIO, VSSIO]
    ea_io = [GPIO] * 9 + [VDD, VSS, VDDIO, VSSIO]
    so_io = [GPIO] * 5 + [VDD, VSS, VDDIO, VSSIO] + [GPIO] * 4

    we_io_pos = calculate_even_spacing(fp, we_io, top_h - corner_h - corner_w, corner_h)
    no_io_pos = calculate_even_spacing(fp, no_io, top_w - corner_h - corner_w, corner_h)
    ea_io_pos = calculate_even_spacing(fp, ea_io, top_h - corner_h - corner_w, corner_w)
    so_io_pos = calculate_even_spacing(fp, so_io, top_w - corner_h - corner_w, corner_w)

    return we_io_pos, no_io_pos, ea_io_pos, so_io_pos

def place_pdn(fp):
    pass

def core_floorplan(fp):
    ## Set up die area ##
    _, (core_w, core_h), (place_w, place_h), (margin_left, margin_bottom) = define_dimensions(fp)
    fp.create_die_area([(0, 0), (core_w, core_h)], core_area=[(margin_left, margin_bottom), (place_w + margin_left, place_h + margin_bottom)])

    ## Place RAM macro ##
    ram_w = fp.available_cells[RAM].width
    ram_h = fp.available_cells[RAM].height
    ram_x = place_w + margin_left - ram_w
    ram_y = place_h + margin_bottom - ram_h
    fp.place_macros([('soc.ram.u_mem.gen_sky130.u_impl_sky130.mem', RAM)], ram_x, ram_y, 0, 0, 'N', snap=True)

    ram_core_space_x = 120 * fp.std_cell_width
    ram_core_space_y = 20 * fp.std_cell_height
    fp.place_blockage(ram_x - ram_core_space_x, ram_y - ram_core_space_y, ram_w + 2 * ram_core_space_x, ram_h + 2 * ram_core_space_y)

    ## Place pins ##
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
    layer = 'm2'

    we_pads, no_pads, ea_pads, so_pads = define_io_placement(fp)

    gpio_w = fp.available_cells[GPIO].width
    gpio_h = fp.available_cells[GPIO].height

    we_gpio_pos = [pos for pad, pos in we_pads if pad == GPIO]
    for i, y in enumerate(we_gpio_pos):
        y -= gpio_h
        for pin, bit, width, offset in pins:
            name = f'we_{pin}[{i * width + bit}]'
            fp.place_pins([name], 0, y + offset, 0, 0, pin_depth, pin_width, layer)

    no_gpio_pos = [pos for pad, pos in no_pads if pad == GPIO]
    for i, x in enumerate(no_gpio_pos):
        x -= gpio_h
        for pin, bit, width, offset in pins:
            name = f'no_{pin}[{i * width + bit}]'
            fp.place_pins([name], x + offset, core_h - pin_depth, 0, 0, pin_width, pin_depth, layer)

    ea_gpio_pos = [pos for pad, pos in ea_pads if pad == GPIO]
    for i, y in enumerate(ea_gpio_pos):
        y -= gpio_h
        for pin, bit, width, offset in pins:
            name = f'ea_{pin}[{i * width + bit}]'
            fp.place_pins([name], core_w - pin_depth, y + gpio_w - offset - pin_width, 0, 0, pin_depth, pin_width, layer)

    so_gpio_pos = [pos for pad, pos in so_pads if pad == GPIO]
    for i, x in enumerate(so_gpio_pos):
        x -= gpio_h
        for pin, bit, width, offset in pins:
            name = f'so_{pin}[{i * width + bit}]'
            fp.place_pins([name], x + gpio_w - offset - pin_width, 0, 0, 0, pin_width, pin_depth, layer)

    ## Place PDN ##
    place_pdn(fp)

def main():
  core_chip = configure_chip('asic_core')
  core_fp = Floorplan(core_chip)
  core_floorplan(core_fp)
  core_fp.write_def('asic_core.def')

if __name__ == '__main__':
  main()