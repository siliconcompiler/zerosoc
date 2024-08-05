import os
from siliconcompiler import Library
from lambdalib import padring
import core


def setup(chip):
    lib = Library(chip, 'zerosoc_top', package='zerosoc', auto_enable=True)

    lib.input('hw/asic_top.v')
    lib.add('option', 'idir', 'hw')

    lib.use(padring)
    lib.use(core)

    return lib
