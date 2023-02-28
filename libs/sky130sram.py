import siliconcompiler

def setup(chip):
    libname = 'sky130sram'
    lib = siliconcompiler.Library(chip, libname)

    stackup = '5M1LI' # TODO: this should this be extracted from something
    version = 'v0_0_2'

    lib.set('package', 'version', version)

    lib.set('option', 'pdk', 'skywater130')
    lib.set('option', 'stackup', stackup)

    # Only one corner available, so use that for all corners
    lib.add('output', 'slow',    'nldm', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    lib.add('output', 'typical', 'nldm', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    lib.add('output', 'fast',    'nldm', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')

    lib.add('output', stackup, 'lef', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    lib.add('output', stackup, 'gds', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds')

    return lib

if __name__ == "__main__":
    lib = setup(siliconcompiler.Chip('<lib>'))
    lib.write_manifest(f'{lib.top()}.json')
