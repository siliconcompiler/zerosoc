module asic_iobuf #(
    parameter DIR = "NO",
    parameter TYPE = "SOFT"
) (
    output din,
    input dout,
    input ie,
    input oen,
    input [7:0] cfg,

    inout poc,
    inout vdd,
    inout vss,
    inout vddio,
    inout vssio,

    inout pad
);

IOPAD iopad (
    .A(dout),
    .Y(din),
    .EN(oen),

    .PAD(pad)
);

endmodule
