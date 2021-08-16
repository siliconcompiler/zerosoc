(* blackbox *)
module asic_core (
    input vdd,
    input vss,

    input [8:0]  we_din,
    output [8:0]  we_dout,
    output [8:0]  we_ie,
    output [8:0]  we_oen,
    output [143:0] we_tech_cfg,

    input [8:0]  no_din,
    output [8:0]  no_dout,
    output [8:0]  no_ie,
    output [8:0]  no_oen,
    output [143:0] no_tech_cfg,

    input [8:0]  so_din,
    output [8:0]  so_dout,
    output [8:0]  so_ie,
    output [8:0]  so_oen,
    output [143:0] so_tech_cfg,

    input [8:0]  ea_din,
    output [8:0]  ea_dout,
    output [8:0]  ea_ie,
    output [8:0]  ea_oen,
    output [143:0] ea_tech_cfg
);

endmodule
