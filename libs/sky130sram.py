import siliconcompiler

def setup(chip):
    libname = 'sky130sram'
    lib = siliconcompiler.Chip(libname)

    stackup = '5M1LI' # TODO: this should this be extracted from something

    lib.set('asic', 'pdk', 'skywater130')
    lib.set('asic', 'stackup', stackup)

    lib.add('model', 'timing', 'nldm', 'typical', 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    lib.add('model', 'layout', 'lef', stackup, 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    lib.add('model', 'layout', 'gds', stackup, 'asic/sky130/ram/sky130_sram_2kbyte_1rw1r_32x512_8.gds')

    return lib
