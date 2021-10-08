(* blackbox *)
module asic_core (
    inout _vdd,
    inout _vss,
    inout _vddio,

    input [8:0]  we_din,
    output [8:0]  we_dout,
    output [8:0]  we_ie,
    output [8:0]  we_oen,
    inout [161:0] we_tech_cfg,

    input [8:0]  no_din,
    output [8:0]  no_dout,
    output [8:0]  no_ie,
    output [8:0]  no_oen,
    inout [161:0] no_tech_cfg,

    input [8:0]  so_din,
    output [8:0]  so_dout,
    output [8:0]  so_ie,
    output [8:0]  so_oen,
    inout [161:0] so_tech_cfg,

    input [8:0]  ea_din,
    output [8:0]  ea_dout,
    output [8:0]  ea_ie,
    output [8:0]  ea_oen,
    inout [161:0] ea_tech_cfg
);

endmodule
