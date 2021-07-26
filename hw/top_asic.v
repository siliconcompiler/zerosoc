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

    wire uart_tx;
    wire uart_tx_en_o;

    wire [31:0] gpio_in;
    wire [31:0] gpio_out;
    wire [31:0] gpio_en_o;

    // Instantiate SoC
    zerosoc #(
        .RamDepth(`RAM_DEPTH)
    ) soc (
        .clk_i(clk),
        .rst_ni(rst),

        .uart_rx_i(uart_rx),
        .uart_tx_o(uart_tx),
        .uart_tx_en_o(uart_tx_en_o),

        .gpio_i(gpio_in),
        .gpio_o(gpio_out),
        .gpio_en_o(gpio_en_o)
    );

    wire [8:0]  we_din;
    wire [8:0]  we_dout;
    wire [71:0] we_cfg;
    wire [8:0]  we_ie;
    wire [8:0]  we_oen;

    wire [8:0]  no_din;
    wire [8:0]  no_dout;
    wire [71:0] no_cfg;
    wire [8:0]  no_ie;
    wire [8:0]  no_oen;

    wire [8:0]  so_din;
    wire [8:0]  so_dout;
    wire [71:0] so_cfg;
    wire [8:0]  so_ie;
    wire [8:0]  so_oen;

    wire [8:0]  ea_din;
    wire [8:0]  ea_dout;
    wire [71:0] ea_cfg;
    wire [8:0]  ea_ie;
    wire [8:0]  ea_oen;

/*
    // Padring I/O
    // HACK: we can't expose these as module I/O, since that screws up OpenROAD
    // PnR. Instead, just make them wires and mark them as keep.
    (* keep *) wire vdd;
    (* keep *) wire vss;

    (* keep *) wire no_vddio;
    (* keep *) wire no_vssio;
    (* keep *) wire [8:0] no_pad;

    (* keep *) wire so_vddio;
    (* keep *) wire so_vssio;
    (* keep *) wire [8:0] so_pad;

    (* keep *) wire ea_vddio;
    (* keep *) wire ea_vssio;
    (* keep *) wire [8:0] ea_pad;

    (* keep *) wire we_vddio;
    (* keep *) wire we_vssio;
    (* keep *) wire [8:0] we_pad;
    */

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
        .WE_VSS(1)
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

        .no_vddio,
        .no_vssio,
        .no_pad, // pad
        .no_din, // data from pad
        .no_dout, // data to pad
        .no_cfg, // config
        .no_ie, // input enable
        .no_oen, // output enable (bar)

        .so_vddio,
        .so_vssio,
        .so_pad, // pad
        .so_din, // data from pad
        .so_dout, // data to pad
        .so_cfg, // config
        .so_ie, // input enable
        .so_oen, // output enable (bar)

        .ea_vddio,
        .ea_vssio,
        .ea_pad, // pad
        .ea_din, // data from pad
        .ea_dout, // data to pad
        .ea_cfg, // config
        .ea_ie, // input enable
        .ea_oen // output enable (bar)
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

    // WEST
    assign gpio_in[4:0] = we_din[4:0];
    assign clk = we_din[5];
    assign rst = we_din[6];
    assign uart_rx = we_din[7];
    // we_din[8] unused - uart_tx is an output

    assign we_dout = {uart_tx, 3'b000, gpio_out[4:0]};
    assign we_oen = {~uart_tx_en_o, 3'b111, ~gpio_en_o[4:0]};
    assign we_ie = we_oen;
    assign we_cfg = 72'b0;

    // NORTH
    assign gpio_in[13:5] = no_din;
    assign no_dout = gpio_out[13:5];
    assign no_oen = ~gpio_en_o[13:5];
    assign no_ie = no_oen;
    assign no_cfg = 72'b0;

    // EAST
    assign gpio_in[22:14] = ea_din;
    assign ea_dout = gpio_out[22:14];
    assign ea_oen = ~gpio_en_o[22:14];
    assign ea_ie = ea_oen;
    assign ea_cfg = 72'b0;

    // SOUTH
    assign gpio_in[31:23] = so_din;
    assign so_dout = gpio_out[31:23];
    assign so_oen = ~gpio_en_o[31:23];
    assign so_ie = so_oen;
    assign so_cfg = 72'b0;

endmodule
