# ZeroSoC FPGA

ZeroSoC includes an option to build a bitstream targeting the Icebreaker dev
board. It also includes a demo program, `sw/hello.c`, that will blink the
Icebreaker LEDs and output messages over UART. The speed of the blinking can be
adjusted using the onboard buttons or by entering the characters `f`, `s`, or
`r` via a UART console.

## Building firmware

Building the firmware requires installing the [RISC-V
toolchain](https://github.com/riscv/riscv-gnu-toolchain). We've tested the
firmware build with a toolchain configured using `--with-arch=rv32i
--with-abi=ilp32`, built for Newlib. In addition, a prebuilt multilib toolchain can be
downloaded from Embecosm:
```
$ wget https://buildbot.embecosm.com/job/riscv32-gcc-centos7/67/artifact/riscv32-embecosm-gcc-centos7-20210530.tar.gz
$ tar xvf riscv32-embecosm-gcc-centos7-20210530.tar.gz --strip-components=1 -C ~/.local/
```

Generating a `.mem` file requires the Python utility
[bin2coe](https://github.com/anishathalye/bin2coe).

Once these prerequisites are installed, cd into `sw/` and run `make
gen/gpio_regs.h`, followed by `make`.

## Building bitstream

Once the firmware is built, build an FPGA bistream by running:
```
./build.py --fpga
```

Next, to embed the firmware in the FPGA bitstream, run:
```
make zerosoc_hello.bit
```

Finally, to flash this bitstream on a connected Icebreaker  dev board, run:
```
iceprog zerosoc_hello.bit
```
