import siliconcompiler as sc

# TODO: add switch to select fpga vs asic build

chip = sc.Chip()
chip.add('source', 'zerosoc.v')
chip.add('source', 'hw/top_icebreaker.v')
chip.add('design', 'top_icebreaker')
chip.set('target', 'ice40_nextpnr')
chip.set('constraint', 'data/icebreaker.pcf')
chip.set_jobid()

chip.target()

chip.run()
