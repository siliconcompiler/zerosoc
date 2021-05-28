import siliconcompiler as sc

# TODO: add switch to select fpga vs asic build

chip = sc.Chip()
chip.add('source', 'zerosoc.v')
chip.add('source', 'hw/top_icebreaker.v')
chip.add('design', 'top_icebreaker')
chip.set('target', 'ice40_nextpnr')
chip.set('constraint', 'data/icebreaker.pcf')

# Prevent us from erroring out on lint warnings during import
chip.set('relax', 'true')

chip.set_jobid()

chip.target()

chip.run()
