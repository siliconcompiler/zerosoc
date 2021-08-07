from siliconcompiler.core import Chip
from siliconcompiler.floorplan import Floorplan

import padring
import core

def configure(name): 
    chip = Chip()

    chip.set('design', name)

    chip.target('skywater130')

    macro = 'ram'
    chip.add('asic', 'macrolib', macro)
    chip.add('macro', macro, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib')
    chip.add('macro', macro, 'lef', 'asic/sky130/sky130_sram_2kbyte_1rw1r_32x512_8.lef')
    chip.add('macro', macro, 'gds', 'asic/sky130/sky130_sram_2kbyte_1rw1r_32x512_8.gds')
    chip.set('macro', macro, 'cells', 'ram', 'sky130_sram_2kbyte_1rw1r_32x512_8')
    chip.add('source', 'hw/prim/sky130/prim_sky130_ram_1p.v')
    chip.add('source', 'asic/sky130/sky130_sram_2kbyte_1rw1r_32x512_8.bb.v')

    macro = 'io'
    chip.add('asic', 'macrolib', macro)
    chip.add('macro', macro, 'model', 'typical', 'nldm', 'lib', 'asic/sky130/io/sky130_dummy_io.lib')
    chip.set('macro', macro, 'lef', f'asic/sky130/io/sky130_ef_io.lef')
    chip.set('macro', macro, 'cells', 'gpio', 'sky130_ef_io__gpiov2_pad_wrapped')
    chip.set('macro', macro, 'cells', 'vdd', 'sky130_ef_io__vccd_hvc_pad')
    chip.set('macro', macro, 'cells', 'vddio', 'sky130_ef_io__vddio_hvc_pad')
    chip.set('macro', macro, 'cells', 'vss', 'sky130_ef_io__vssd_hvc_pad')
    chip.set('macro', macro, 'cells', 'vssio', 'sky130_ef_io__vssio_hvc_pad')
    chip.set('macro', macro, 'cells', 'corner', 'sky130_ef_io__corner_pad')
    chip.set('macro', macro, 'cells', 'fill1',  'sky130_ef_io__com_bus_slice_1um')
    chip.set('macro', macro, 'cells', 'fill5',  'sky130_ef_io__com_bus_slice_5um')
    chip.set('macro', macro, 'cells', 'fill10', 'sky130_ef_io__com_bus_slice_10um')
    chip.set('macro', macro, 'cells', 'fill20', 'sky130_ef_io__com_bus_slice_20um')
    
    return chip

if __name__ == '__main__':
    chip = configure('core')
    fp = Floorplan(chip)
    core.setup_floorplan(fp, chip)
    fp.write_lef('core.lef')
    fp.write_def('core.def')

    chip = configure('padring')

    macro = 'zerosoc'
    chip.add('asic', 'macrolib', macro)
    chip.set('macro', macro, 'lef', 'core.lef')
    chip.set('macro', macro, 'cells', 'zerosoc', 'core')

    fp = Floorplan(chip)
    padring.setup_floorplan(fp, chip)
    fp.write_def('padring.def')
