// Dummy shim for Lattice primitive to prevent Verilator lint from throwing an
// error. Yosys synthesis will replace this implementation with the proper cell.

module SB_HFOSC #(
    parameter CLKHF_DIV = "0b11"
) (
    input CLKHFPU,
    input CLKHFEN,
    output CLKHF
);

endmodule
