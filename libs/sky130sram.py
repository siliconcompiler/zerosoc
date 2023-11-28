import siliconcompiler


def setup(chip):
    libname = 'sky130sram'
    lib = siliconcompiler.Library(chip, libname)

    stackup = '5M1LI'
    version = 'v0_0_2'

    lib.set('option', 'pdk', 'skywater130')
    lib.set('option', 'stackup', stackup)

    # Only one corner available, so use that for all corners
    libpath = 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib'
    lib.add('output', 'slow',    'nldm', libpath, package='zerosoc')
    lib.add('output', 'typical', 'nldm', libpath, package='zerosoc')
    lib.add('output', 'fast',    'nldm', libpath, package='zerosoc')

    lib.add('output', stackup, 'lef', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef',
            package='zerosoc')
    lib.add('output', stackup, 'gds', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds',
            package='zerosoc')

    return lib


if __name__ == "__main__":
    lib = setup(siliconcompiler.Chip('<lib>'))
    lib.write_manifest(f'{lib.top()}.json')
