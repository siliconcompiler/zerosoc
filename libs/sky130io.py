import siliconcompiler

def setup():
    libname = 'sky130io'
    lib = siliconcompiler.Chip(libname)

    stackup = '5M1LI' # TODO: this should this be extracted from something

    lib.set('asic', 'pdk', 'skywater130')
    lib.set('asic', 'stackup', stackup)

    lib.set('model', 'timing', 'nldm', 'typical', 'asic/sky130/io/sky130_dummy_io.lib')
    lib.set('model', 'layout', 'lef', stackup, 'asic/sky130/io/sky130_ef_io.lef')

    # Need both GDS files: ef relies on fd one
    lib.add('model', 'layout', 'gds', stackup, 'asic/sky130/io/sky130_ef_io.gds')
    lib.add('model', 'layout', 'gds', stackup, 'asic/sky130/io/sky130_fd_io.gds')
    lib.add('model', 'layout', 'gds', stackup, 'asic/sky130/io/sky130_ef_io__gpiov2_pad_wrapped.gds')
