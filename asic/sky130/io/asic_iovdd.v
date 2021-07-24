module asic_iovdd #(
    parameter DIR = "NO",
    parameter TYPE = "SOFT"
) (
    inout vdd,
    inout vss,
    inout vddio,
    inout vssio,
    inout poc
);

    // TODO: what to do with poc?

    sky130_ef_io__vccd_hvc_pad iovdd (
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