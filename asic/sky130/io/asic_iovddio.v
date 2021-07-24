module asic_iovddio #( 
    parameter DIR = "NO",
    parameter TYPE = "SOFT"
) (
    inout vdd,
    inout vss,
    inout vddio,
    inout vssio,
    inout poc
);

sky130_ef_io__vddio_hvc_pad iovddio (
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