module asic_iocut #(
    parameter DIR = "NO",
    parameter TYPE = "SOFT"
) (
    inout vdd,
    inout vss,
    inout vddio,
    inout vssio,
    inout poc
);

bb_iocell bb (
    .vdd(vdd),
    .vss(vss),
    .vddio(vddio),
    .vssio(vssio),
    .poc(poc)
);

endmodule