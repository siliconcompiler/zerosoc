module asic_top (
    inout vdd,
    inout vss,
    inout vddio,
    inout vssio,

    inout [8:0] no_pad,
    inout [8:0] so_pad,
    inout [8:0] ea_pad,
    inout [8:0] we_pad
);

    wire [8:0]  we_din;
    wire [8:0]  we_dout;
    wire [8:0]  we_ie;
    wire [8:0]  we_oen;
    wire [161:0] we_tech_cfg;

    wire [8:0]  no_din;
    wire [8:0]  no_dout;
    wire [8:0]  no_ie;
    wire [8:0]  no_oen;
    wire [161:0] no_tech_cfg;

    wire [8:0]  so_din;
    wire [8:0]  so_dout;
    wire [8:0]  so_ie;
    wire [8:0]  so_oen;
    wire [161:0] so_tech_cfg;

    wire [8:0]  ea_din;
    wire [8:0]  ea_dout;
    wire [8:0]  ea_ie;
    wire [8:0]  ea_oen;
    wire [161:0] ea_tech_cfg;

    asic_core core (
        ._vdd(vdd),
        ._vss(vss),

        .we_din,
        .we_dout,
        .we_ie,
        .we_oen,
        .we_tech_cfg,

        .no_din,
        .no_dout,
        .no_ie,
        .no_oen,
        .no_tech_cfg,

        .so_din,
        .so_dout,
        .so_ie,
        .so_oen,
        .so_tech_cfg,

        .ea_din,
        .ea_dout,
        .ea_ie,
        .ea_oen,
        .ea_tech_cfg
    );

   //#############################
   // PADRING
   //#############################
   // All IO related "tech" parameters in the .vh file
`include "iomap.vh"
    wire [7:0] ioring;

   la_iopadring #(.RINGW(8),
                  .CFGW(18),
                  //north
                  .NO_NPINS(9),
                  .NO_NCELLS(13),
                  .NO_NSECTIONS(1),
                  .NO_CELLMAP(CELLMAP),
                  //east
                  .EA_NPINS(9),
                  .EA_NCELLS(13),
                  .EA_NSECTIONS(1),
                  .EA_CELLMAP(CELLMAP),
                  //south
                  .SO_NPINS(9),
                  .SO_NCELLS(13),
                  .SO_NSECTIONS(1),
                  .SO_CELLMAP(CELLMAP),
                  //west
                  .WE_NPINS(9),
                  .WE_NCELLS(13),
                  .WE_NSECTIONS(1),
                  .WE_CELLMAP(CELLMAP))
   padring(// Inouts
                .no_pad         (no_pad),
                .ea_pad         (ea_pad),
                .so_pad         (so_pad),
                .we_pad         (we_pad),
                .no_aio         (),
                .ea_aio         (),
                .so_aio         (),
                .we_aio         (),
                .no_vddio       (vddio),
                .ea_vddio       (vddio),
                .so_vddio       (vddio),
                .we_vddio       (vddio),
                /*AUTOINST*/
                // Outputs
                .no_zp          (no_din),
                .no_zn          (),
                .ea_zp          (ea_din),
                .ea_zn          (),
                .so_zp          (so_din),
                .so_zn          (),
                .we_zp          (we_din),
                .we_zn          (),
                // Inouts
                .vss            (vss),
                .no_vdd         (vdd),
                .no_vssio       (vssio),
                .no_ioring      (ioring),
                .ea_vdd         (vdd),
                .ea_vssio       (vssio),
                .ea_ioring      (ioring),
                .so_vdd         (vdd),
                .so_vssio       (vssio),
                .so_ioring      (ioring),
                .we_vdd         (vdd),
                .we_vssio       (vssio),
                .we_ioring      (ioring),
                // Inputs
                .no_a           (no_dout),
                .no_ie          (no_ie),
                .no_oe          (~no_oen),
                .no_pe          ('b0),
                .no_ps          ('b0),
                .no_cfg         (no_tech_cfg),
                .ea_a           (ea_dout),
                .ea_ie          (ea_ie),
                .ea_oe          (~ea_oen),
                .ea_pe          ('b0),
                .ea_ps          ('b0),
                .ea_cfg         (ea_tech_cfg),
                .so_a           (so_dout),
                .so_ie          (so_ie),
                .so_oe          (~so_oen),
                .so_pe          ('b0),
                .so_ps          ('b0),
                .so_cfg         (so_tech_cfg),
                .we_a           (we_dout),
                .we_ie          (we_ie),
                .we_oe          (~we_oen),
                .we_pe          ('b0),
                .we_ps          ('b0),
                .we_cfg         (we_tech_cfg));

endmodule
