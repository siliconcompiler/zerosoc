from siliconcompiler.core import Chip
from siliconcompiler.floorplan import Floorplan

from floorplan import setup_floorplan

chip = Chip()

chip.set('design', 'zerosoc')
chip.target('freepdk45')

macro = 'io'
chip.add('asic', 'macrolib', macro)
chip.set('macro', macro, 'lef', 'iocells.lef')
chip.set('macro', macro, 'cells', 'gpio', 'IOPAD')
chip.set('macro', macro, 'cells', 'vdd', 'PWRPAD')
chip.set('macro', macro, 'cells', 'vddio', 'PWRPAD')
chip.set('macro', macro, 'cells', 'vss', 'PWRPAD')
chip.set('macro', macro, 'cells', 'corner', 'CORNER')
chip.set('macro', macro, 'cells', 'fill1',  'FILLER01')
chip.set('macro', macro, 'cells', 'fill2',  'FILLER02')
chip.set('macro', macro, 'cells', 'fill5',  'FILLER05')
chip.set('macro', macro, 'cells', 'fill10', 'FILLER10')
chip.set('macro', macro, 'cells', 'fill25', 'FILLER25')
chip.set('macro', macro, 'cells', 'fill50', 'FILLER50')

macro = 'sram_32x2048_1rw'
chip.add('asic', 'macrolib', macro)
chip.set('macro', macro, 'lef', f'../hw/prim/freepdk45/{macro}.lef')
chip.set('macro', macro, 'cells', 'ram', 'sram_32x2048_1rw')

fp = Floorplan(chip)

setup_floorplan(fp, chip)

fp.write_def('zerosoc.def')
