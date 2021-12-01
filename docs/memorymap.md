# Memory map

Putting this here as a single source of truth between `hw/xbar_pkg.sv` and
`sw/devices.h`. Having a generator for these files could be useful!

(These addresses are based on the addresses used in OpenTitan, but can be
changed/finalized once full set of peripherals is complete)

Peripheral | Base Address
-----------|-------------
RAM        | 0x00000000
UART       | 0x40000000
GPIO       | 0x40010000

