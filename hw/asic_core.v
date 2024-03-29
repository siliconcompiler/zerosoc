module asic_core (
    inout _vdd,
    inout _vss,

    input [8:0]  we_din,
    output [8:0]  we_dout,
    output [8:0]  we_ie,
    output [8:0]  we_oen,
    output [161:0] we_tech_cfg,

    input [8:0]  no_din,
    output [8:0]  no_dout,
    output [8:0]  no_ie,
    output [8:0]  no_oen,
    output [161:0] no_tech_cfg,

    input [8:0]  so_din,
    output [8:0]  so_dout,
    output [8:0]  so_ie,
    output [8:0]  so_oen,
    output [161:0] so_tech_cfg,

    input [8:0]  ea_din,
    output [8:0]  ea_dout,
    output [8:0]  ea_ie,
    output [8:0]  ea_oen,
    output [161:0] ea_tech_cfg
);

    wire uart_tx;
    wire uart_tx_en_o;

    wire [31:0] gpio_in;
    wire [31:0] gpio_out;
    wire [31:0] gpio_en_o;

    // Instantiate SoC
    zerosoc #(
        .RamDepth(`RAM_DEPTH),
        .ASIC(1)
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

    // WEST
    assign gpio_in[4:0] = we_din[4:0];
    assign clk = we_din[5];
    assign rst = we_din[6];
    assign uart_rx = we_din[7];
    // we_din[8] unused - uart_tx is an output

    assign we_dout = {uart_tx, 3'b000, gpio_out[4:0]};
    assign we_oen = {~uart_tx_en_o, 3'b111, ~gpio_en_o[4:0]};
    assign we_ie = ~we_oen; // ie is secretly ien for skywater

    // NORTH
    assign gpio_in[13:5] = no_din;
    assign no_dout = gpio_out[13:5];
    assign no_oen = ~gpio_en_o[13:5];
    assign no_ie = ~no_oen; // ie is secretly ien for skywater

    // EAST
    assign gpio_in[22:14] = ea_din;
    assign ea_dout = gpio_out[22:14];
    assign ea_oen = ~gpio_en_o[22:14];
    assign ea_ie = ~ea_oen; // ie is secretly ien for skywater

    // SOUTH
    assign gpio_in[31:23] = so_din;
    assign so_dout = gpio_out[31:23];
    assign so_oen = ~gpio_en_o[31:23];
    assign so_ie = ~so_oen; // ie is secretly ien for skywater

    // Tieoffs
    // Note that all enable signals used for power-on ramp are tied off to their
    // fixed steady-state values.
    generate
        genvar i;

        for(i=0;i<9;i=i+1)
            begin: we_tieoff
                wire tie_lo_esd, tie_hi_esd;
                assign tie_lo_esd = we_tech_cfg[i*18 + 16];
                assign tie_hi_esd = we_tech_cfg[i*18 + 17];

                assign we_tech_cfg[i*18 + 0] = 1'b1; // hld_h_n
                assign we_tech_cfg[i*18 + 1] = 1'b1; // enable_h
                assign we_tech_cfg[i*18 + 2] = tie_lo_esd; // enable_inp_h
                assign we_tech_cfg[i*18 + 3] = 1'b1; // enable_vdda_h
                assign we_tech_cfg[i*18 + 4] = 1'b1; // enable_vswitch_h DIFF!!
                assign we_tech_cfg[i*18 + 5] = 1'b1; // enable_vddio
                assign we_tech_cfg[i*18 + 6] = 1'b0; // ib_mode_sel
                assign we_tech_cfg[i*18 + 7] = 1'b0; // vtrip_sel
                assign we_tech_cfg[i*18 + 8] = 1'b0; // slow
                assign we_tech_cfg[i*18 + 9] = 1'b0; // hld_ovr
                assign we_tech_cfg[i*18 + 10] = 1'b0; // analog_en
                assign we_tech_cfg[i*18 + 11] = 1'b0; // analog_sel
                assign we_tech_cfg[i*18 + 12] = 1'b0; // analog_pol
                // strong pull-up, strong pull-down
                assign we_tech_cfg[i*18 + 15:i*18 + 13] = 3'b110; // dm[2:0]
            end

        for(i=0;i<9;i=i+1)
            begin: no_tieoff
                wire tie_lo_esd, tie_hi_esd;
                assign tie_lo_esd = no_tech_cfg[i*18 + 16];
                assign tie_hi_esd = no_tech_cfg[i*18 + 17];

                assign no_tech_cfg[i*18 + 0] = 1'b1; // hld_h_n
                assign no_tech_cfg[i*18 + 1] = 1'b1; // enable_h
                assign no_tech_cfg[i*18 + 2] = tie_lo_esd; // enable_inp_h
                assign no_tech_cfg[i*18 + 3] = 1'b1; // enable_vdda_h
                assign no_tech_cfg[i*18 + 4] = 1'b1; // enable_vswitch_h
                assign no_tech_cfg[i*18 + 5] = 1'b1; // enable_vddio
                assign no_tech_cfg[i*18 + 6] = 1'b0; // ib_mode_sel
                assign no_tech_cfg[i*18 + 7] = 1'b0; // vtrip_sel
                assign no_tech_cfg[i*18 + 8] = 1'b0; // slow
                assign no_tech_cfg[i*18 + 9] = 1'b0; // hld_ovr
                assign no_tech_cfg[i*18 + 10] = 1'b0; // analog_en
                assign no_tech_cfg[i*18 + 11] = 1'b0; // analog_sel
                assign no_tech_cfg[i*18 + 12] = 1'b0; // analog_pol
                // strong pull-up, strong pull-down
                assign no_tech_cfg[i*18 + 15:i*18 + 13] = 3'b110; // dm[2:0]
            end

        for(i=0;i<9;i=i+1)
            begin: ea_tieoff
                wire tie_lo_esd, tie_hi_esd;
                assign tie_lo_esd = ea_tech_cfg[i*18 + 16];
                assign tie_hi_esd = ea_tech_cfg[i*18 + 17];

                assign ea_tech_cfg[i*18 + 0] = 1'b1; // hld_h_n
                assign ea_tech_cfg[i*18 + 1] = 1'b1; // enable_h
                assign ea_tech_cfg[i*18 + 2] = tie_lo_esd; // enable_inp_h
                assign ea_tech_cfg[i*18 + 3] = 1'b1; // enable_vdda_h
                assign ea_tech_cfg[i*18 + 4] = 1'b1; // enable_vswitch_h
                assign ea_tech_cfg[i*18 + 5] = 1'b1; // enable_vddio
                assign ea_tech_cfg[i*18 + 6] = 1'b0; // ib_mode_sel
                assign ea_tech_cfg[i*18 + 7] = 1'b0; // vtrip_sel
                assign ea_tech_cfg[i*18 + 8] = 1'b0; // slow
                assign ea_tech_cfg[i*18 + 9] = 1'b0; // hld_ovr
                assign ea_tech_cfg[i*18 + 10] = 1'b0; // analog_en
                assign ea_tech_cfg[i*18 + 11] = 1'b0; // analog_sel
                assign ea_tech_cfg[i*18 + 12] = 1'b0; // analog_pol
                // strong pull-up, strong pull-down
                assign ea_tech_cfg[i*18 + 15:i*18 + 13] = 3'b110; // dm[2:0]
            end

        for(i=0;i<9;i=i+1)
            begin: so_tieoff
                wire tie_lo_esd, tie_hi_esd;
                assign tie_lo_esd = ea_tech_cfg[i*18 + 16];
                assign tie_hi_esd = ea_tech_cfg[i*18 + 17];

                assign so_tech_cfg[i*18 + 0] = 1'b1; // hld_h_n
                assign so_tech_cfg[i*18 + 1] = 1'b1; // enable_h
                assign so_tech_cfg[i*18 + 2] = tie_lo_esd; // enable_inp_h
                assign so_tech_cfg[i*18 + 3] = 1'b1; // enable_vdda_h
                assign so_tech_cfg[i*18 + 4] = 1'b1; // enable_vswitch_h
                assign so_tech_cfg[i*18 + 5] = 1'b1; // enable_vddio
                assign so_tech_cfg[i*18 + 6] = 1'b0; // ib_mode_sel
                assign so_tech_cfg[i*18 + 7] = 1'b0; // vtrip_sel
                assign so_tech_cfg[i*18 + 8] = 1'b0; // slow
                assign so_tech_cfg[i*18 + 9] = 1'b0; // hld_ovr
                assign so_tech_cfg[i*18 + 10] = 1'b0; // analog_en
                assign so_tech_cfg[i*18 + 11] = 1'b0; // analog_sel
                assign so_tech_cfg[i*18 + 12] = 1'b0; // analog_pol
                // strong pull-up, strong pull-down
                assign so_tech_cfg[i*18 + 15:i*18 + 13] = 3'b110; // dm[2:0]
            end
    endgenerate

endmodule
