# ZeroSoC

ZeroSoC is a basic RISC-V SoC meant to demonstrate the capabilities of
SiliconCompiler. ZeroSoC currently consists of an Ibex core, the OpenTitan's
UART and GPIO peripherals, and 8 KB of RAM.

## Build flow

There are currently two targets supported by this repository: either the
Icebreaker FPGA dev board via SC, or simulation with Icarus Verilog.

### Firmware

Both targets require building the demo firmware `sw/hello.c`. To do so, cd into
`sw/` and run `make gen/gpio_regs.h`, followed by `make`. Building the
firmware requires installing the [RISC-V
toolchain](https://github.com/riscv/riscv-gnu-toolchain). I configured my
toolchain using `--with-arch=rv32i --with-abi=ilp32`, and ran the build for
Newlib.

In addition, generating the `*.mem` file requires the Python utility
[bin2coe](https://github.com/anishathalye/bin2coe). I plan to change the
Makefile to just use riscv-gcc's objcopy instead, since I believe newer versions
can output to this format.

### Simulation

To build the simulation, run `make sim/soc_tb.out`. Running it with
`./sim/soc_tb.out` generates a waveform `zerosoc.vcd`. Building the
simulation executable requires installing [sv2v](https://github.com/zachjs/sv2v) and [Icarus Verilog](http://iverilog.icarus.com/).

### FPGA

To build ZeroSoC for the Icebreaker FPGA dev board, run `make`. This target will
generate a flattened Verilog translation of the SoC SystemVerilog, and then run
that through SiliconCompiler. See the Makefile for how I'm doing the translation
with sv2v, and see build.py for how this gets run through SC using its Python API.

The default target will also copy the final result, `zerosoc.bit`, out of the SC
build directory and into the top level. Building the FPGA bitstream requires the
most prerequisites: you'll need [sv2v](https://github.com/zachjs/sv2v),
[SiliconCompiler](https://github.com/siliconcompiler/siliconcompiler/), as well
as Yosys, NextPNR-ice40, and the Icestorm tools (instructions for
building/installing these can be found
[here](http://www.clifford.at/icestorm/)).

## Memory map

Putting this here as a single source of truth between `hw/xbar_pkg.sv` and
`sw/devices.h`. Having a generator for these files could be useful!

(These addresses are based on the addresses used in OpenTitan, but can be
changed/finalized once full set of peripherals is complete)

Peripheral | Base Address
-----------|-------------
RAM        | 0x00000000
UART       | 0x40000000
GPIO       | 0x40010000
