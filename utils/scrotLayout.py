'''
KLayout screenshot script originally based on:
https://github.com/The-OpenROAD-Project/OpenLane/blob/master/scripts/klayout/scrotLayout.py

Assumes you have a technology named "sky130A" configured.
'''

import pya
import re
import os

WIDTH = 2048
HEIGHT = 1700

app = pya.Application.instance()
win = app.main_window()

win.initial_technology = 'sky130A'
cell_view = win.load_layout(input_layout, 0)
layout_view = cell_view.view()

layout_view.max_hier()

print("[INFO] Writing out PNG screenshot '{0}'".format(input_layout+".png"))
basename = os.path.splitext(input_layout)[0]
layout_view.save_image(basename+".png", WIDTH, HEIGHT)
print("Done")
app.exit(0)
