module top_asic (
    inout vdd,
    inout vss,

    inout no_vddio,
    inout no_vssio,
    inout [8:0] no_pad,

    inout so_vddio,
    inout so_vssio,
    inout [8:0] so_pad,

    inout ea_vddio,
    inout ea_vssio,
    inout [8:0] ea_pad,

    inout we_vddio,
    inout we_vssio,
    inout [8:0] we_pad
);

    wire [8:0]  we_din;
    wire [8:0]  we_dout;
    wire [71:0] we_cfg;
    wire [8:0]  we_ie;
    wire [8:0]  we_oen;
    wire [143:0] we_tech_cfg;

    wire [8:0]  no_din;
    wire [8:0]  no_dout;
    wire [71:0] no_cfg;
    wire [8:0]  no_ie;
    wire [8:0]  no_oen;
    wire [143:0] no_tech_cfg;

    wire [8:0]  so_din;
    wire [8:0]  so_dout;
    wire [71:0] so_cfg;
    wire [8:0]  so_ie;
    wire [8:0]  so_oen;
    wire [143:0] so_tech_cfg;

    wire [8:0]  ea_din;
    wire [8:0]  ea_dout;
    wire [71:0] ea_cfg;
    wire [8:0]  ea_ie;
    wire [8:0]  ea_oen;
    wire [143:0] ea_tech_cfg;

    oh_padring #(
        .TYPE("SOFT"),
        .NO_DOMAINS(1),
        .NO_GPIO(9),
        .NO_VDDIO(1),
        .NO_VSSIO(1),
        .NO_VDD(1),
        .NO_VSS(1),
        .SO_DOMAINS(1),
        .SO_GPIO(9),
        .SO_VDDIO(1),
        .SO_VSSIO(1),
        .SO_VDD(1),
        .SO_VSS(1),
        .EA_DOMAINS(1),
        .EA_GPIO(9),
        .EA_VDDIO(1),
        .EA_VSSIO(1),
        .EA_VDD(1),
        .EA_VSS(1),
        .WE_DOMAINS(1),
        .WE_GPIO(9),
        .WE_VDDIO(1),
        .WE_VSSIO(1),
        .WE_VDD(1),
        .WE_VSS(1),
        .TECH_CFG_WIDTH(16)
    ) padring (
        .vss,
        .vdd,

        .we_vddio,
        .we_vssio,
        .we_pad,
        .we_din,
        .we_dout,
        .we_cfg,
        .we_ie,
        .we_oen,
        .we_tech_cfg,

        .no_vddio,
        .no_vssio,
        .no_pad, // pad
        .no_din, // data from pad
        .no_dout, // data to pad
        .no_cfg, // config
        .no_ie, // input enable
        .no_oen, // output enable (bar)
        .no_tech_cfg,

        .so_vddio,
        .so_vssio,
        .so_pad, // pad
        .so_din, // data from pad
        .so_dout, // data to pad
        .so_cfg, // config
        .so_ie, // input enable
        .so_oen, // output enable (bar)
        .so_tech_cfg,

        .ea_vddio,
        .ea_vssio,
        .ea_pad, // pad
        .ea_din, // data from pad
        .ea_dout, // data to pad
        .ea_cfg, // config
        .ea_ie, // input enable
        .ea_oen // output enable (bar)
        .ea_tech_cfg
    );

    oh_pads_corner corner_sw (
        .vdd(vdd),
        .vss(vss),
        .vddio(vddio),
        .vssio(vssio)
    );

    oh_pads_corner corner_nw (
        .vdd(vdd),
        .vss(vss),
        .vddio(vddio),
        .vssio(vssio)
    );

    oh_pads_corner corner_ne (
        .vdd(vdd),
        .vss(vss),
        .vddio(vddio),
        .vssio(vssio)
    );

    oh_pads_corner corner_se (
        .vdd(vdd),
        .vss(vss),
        .vddio(vddio),
        .vssio(vssio)
    );

    assign we_cfg = 72'b0;
    assign no_cfg = 72'b0;
    assign ea_cfg = 72'b0;
    assign so_cfg = 72'b0;

endmodule
