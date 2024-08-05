import os
from siliconcompiler import Library
from lambdalib import padring
import zerosoc_core


def setup(chip):
    lib = Library(chip, 'zerosoc_top', package='zerosoc', auto_enable=True)
    lib.register_source(
        name='zerosoc',
        path=os.path.abspath(os.path.dirname(__file__)))

    lib.input('hw/asic_top.v')
    lib.add('option', 'idir', 'hw')

    lib.use(padring)
    lib.use(zerosoc_core)

    return lib
