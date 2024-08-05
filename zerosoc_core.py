import os
from siliconcompiler import Library
from siliconcompiler.package import path as sc_path
import opentitan
from lambdalib import ramlib


def setup(chip):
    lib = Library(chip, "zerosoc_core", package='zerosoc', auto_enable=True)
    lib.register_source(
        name='zerosoc',
        path=os.path.abspath(os.path.dirname(__file__)))

    lib.add('option', 'idir', 'hw')
    lib.add('option', 'ydir', 'hw/prim')
    # lib.input('hw/asic_top.v')
    lib.input('hw/xbar_pkg.sv')
    lib.input('hw/prim/prim_pkg.sv')

    lib.input('hw/uart_core.sv')

    lib.input('hw/zerosoc.sv')
    lib.input('hw/xbar.sv')
    lib.input('hw/tl_dbg.sv')

    lib.input('hw/asic_core.v')

    # TODO: break into separate lib
    lib.input('hw/prim/lambdalib/prim_lambdalib_ram_1p.v')
    lib.input('hw/prim/lambdalib/prim_lambdalib_clock_gating.v')

    # hack to work around fact that $readmemh now runs in context of build
    # directory and can't load .mem files using relative paths
    lib.add('option', 'define', f'MEM_ROOT={sc_path(lib, "zerosoc")}')
    lib.add('option', 'define', 'PRIM_DEFAULT_IMPL="prim_pkg::ImplLambdalib"')
    lib.add('option', 'define', 'RAM_DEPTH=512')

    lib.use(opentitan)
    lib.use(ramlib)

    return lib
