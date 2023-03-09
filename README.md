# ZeroSoC

ZeroSoC is a RISC-V SoC designed to demonstrate the capabilities of
[SiliconCompiler][sc]. ZeroSoC consists of an [Ibex core][ibex], UART and GPIO
peripherals from the [OpenTitan][opentitan] project, and 8 KB of RAM.

<p align="center">
  <img src="docs/img/zerosoc.png" height="360px"/>
</p>

## Getting Started

Clone the repository and all its submodules:

```console
$ git clone git@github.com:siliconcompiler/zerosoc.git
$ cd zerosoc
$ git checkout stable
$ git submodule update --init --recursive
$ pip install -r python-requirements.txt
```

Building ZeroSoC locally for ASIC or FPGA targets requires installing external
tools. This [page][tools] contains links to installation instructions for SC's
supported tools. The build script also supports remote builds, which do not
require installing additional tools.

**Note**: The ZeroSoC tip of main is considered unstable and may not be
compatible with the latest SiliconCompiler. To ensure compatibility, we
recommend checking out the [`stable`][stable] tag and using the most recent
release version of SC.

## Usage

[`build.py`](build.py) is ZeroSoC's build script, based around the SiliconCompiler Python
API. Running this script with no options initiates a local ZeroSoC ASIC build,
and runs DRC and LVS on the final GDS.

Running `build.py --help` gives information on additional options:

```
-h, --help        show this help message and exit
--core-only       Only build ASIC core GDS.
--top-only        Only integrate ASIC core into padring. Assumes core already built.
--floorplan       Break in floorplanning steps
--verify          Run DRC and LVS.
--remote          Run on remote server. Requires SC remote credentials.
```

## FPGA

For more details on how to run the ZeroSoC FPGA demo, see [here](docs/fpga.md).

## License

[Apache License 2.0](LICENSE)

[sc]: https://github.com/siliconcompiler/siliconcompiler
[ibex]: https://github.com/lowrisc/ibex
[opentitan]: https://github.com/lowrisc/opentitan
[tutorial]: https://docs.siliconcompiler.com/en/latest/tutorials/zerosoc.html
[tools]: https://docs.siliconcompiler.com/en/latest/reference_manual/tools.html
[stable]: https://github.com/siliconcompiler/zerosoc/tree/stable
