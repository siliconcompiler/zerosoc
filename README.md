# ZeroSoC

[![Nightly ZeroSoC Build](https://github.com/siliconcompiler/zerosoc/actions/workflows/build.yml/badge.svg)](https://github.com/siliconcompiler/zerosoc/actions/workflows/build.yml)

ZeroSoC is a basic RISC-V SoC meant to demonstrate the capabilities of
SiliconCompiler. ZeroSoC currently consists of an Ibex core, the OpenTitan's
UART and GPIO peripherals, and 8 KB of RAM.

## Getting Started

Clone the repository and all its submodules.

```
$ git clone --recursive git@github.com:siliconcompiler/zerosoc.git
$ pip install -r python-requirements.txt
```

## Build flow

There are currently three targets supported by this repository: the Icebreaker
FPGA dev board via SC, simulation with Icarus Verilog, or an ASIC flow via SC.

### Firmware

Both the sim and FPGA targets require building the demo firmware `sw/hello.c`.
To do so, cd into `sw/` and run `make gen/gpio_regs.h`, followed by `make`.
Building the firmware requires installing the [RISC-V
toolchain](https://github.com/riscv/riscv-gnu-toolchain). I configured my
toolchain using `--with-arch=rv32i --with-abi=ilp32`, and ran the build for
Newlib. A prebuilt multilib toolchain can be downloaded from Embecosm:

```
$ wget https://buildbot.embecosm.com/job/riscv32-gcc-centos7/67/artifact/riscv32-embecosm-gcc-centos7-20210530.tar.gz
$ tar xvf riscv32-embecosm-gcc-centos7-20210530.tar.gz --strip-components=1 -C ~/.local/
```

In addition, generating the `*.mem` file requires the Python utility
[bin2coe](https://github.com/anishathalye/bin2coe). I plan to change the
Makefile to just use riscv-gcc's objcopy instead, since I believe newer versions
can output to this format.

### Simulation

To build the simulation, run `make sim/soc_tb.out`. Running it with
`./sim/soc_tb.out` generates a waveform `zerosoc.vcd`. Building the
simulation executable requires installing [sv2v](https://github.com/zachjs/sv2v) and [Icarus Verilog](http://iverilog.icarus.com/).

### FPGA

- To build the bitstream, run: `python build.py --fpga -a validate`
     - Note if the build directory already exists, the validate step can be
     skipped by removing the `-a` flag
- To build the firmware and embed it in the FPGA bitstream: `make
zerosoc_hello.bit`
- To program the FPGA: `iceprog zerosoc_hello.bit`

Building the FPGA bitstream requires the following prerequisites:
- [SiliconCompiler](https://github.com/siliconcompiler/siliconcompiler/)
- Surelog
- [sv2v](https://github.com/zachjs/sv2v),
- Yosys
- NextPNR-ice40 and the Icestorm tools (instructions for building/installing
these can be found [here](http://www.clifford.at/icestorm/)).

### ASIC
- To run the ASIC flow, run `python build.py -a validate`
    - Like with the FPGA flow, there's no need for the `-a` option if the build
      directory already exists.

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
