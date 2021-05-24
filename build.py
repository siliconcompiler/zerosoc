import siliconcompiler as sc

source = 'soc.v'

chip = sc.Chip()
chip.add('source', source)
chip.add('design', 'soc')
chip.set('target', 'freepdk45')
chip.set('asic', 'diesize', "0 0 100.13 100.8")
chip.set('asic', 'coresize', "10.07 11.2 90.25 91")
chip.set_jobid()

chip.target()

chip.run()
