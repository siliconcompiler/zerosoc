module asic_iovss #(
    parameter DIR = "NO",
    parameter TYPE = "SOFT"
) (
    inout vdd,
    inout vss,
    inout vddio,
    inout vssio,
    inout poc
);

sky130_ef_io__vssd_hvc_pad iovss (
    .VDDIO(),
    .VDDIO_Q(),
    .VDDA(),
    .VCCD(),
    .VSWITCH(),
    .VCCHIB(),
    .VSSA(),
    .VSSD(),
    .VSSIO_Q(),
    .VSSIO(),

    .AMUXBUS_A(),
    .AMUXBUS_B()
);

endmodule