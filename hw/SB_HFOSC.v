// Dummy shim for Lattice primitive to prevent Verilator lint from throwing an
// error. Yosys synthesis will replace this implementation with the proper cell.

module SB_HFOSC #(
    // Fixed width ensures that sv2v doesn't insert an extra string width
    // parameter when converting top-level
    parameter [31:0] CLKHF_DIV = "0b11"
) (
    input CLKHFPU,
    input CLKHFEN,
    output CLKHF
);

endmodule
