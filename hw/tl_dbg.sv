module tl_dbg(
  input  tlul_pkg::tl_h2d_t tl_h2d,
  input tlul_pkg::tl_d2h_t tl_d2h
);

import tlul_pkg::*;

logic                         tl_h2d_a_valid;
tl_a_op_e                     tl_h2d_a_opcode;
logic                  [2:0]  tl_h2d_a_param;
logic  [top_pkg::TL_SZW-1:0]  tl_h2d_a_size;
logic  [top_pkg::TL_AIW-1:0]  tl_h2d_a_source;
logic   [top_pkg::TL_AW-1:0]  tl_h2d_a_address;
logic  [top_pkg::TL_DBW-1:0]  tl_h2d_a_mask;
logic   [top_pkg::TL_DW-1:0]  tl_h2d_a_data;
tl_a_user_t                   tl_h2d_a_user;
logic                         tl_h2d_d_ready;

logic                         tl_d2h_d_valid;
tl_d_op_e                     tl_d2h_d_opcode;
logic                  [2:0]  tl_d2h_d_param;
logic  [top_pkg::TL_SZW-1:0]  tl_d2h_d_size;   // Bouncing back a_size
logic  [top_pkg::TL_AIW-1:0]  tl_d2h_d_source;
logic  [top_pkg::TL_DIW-1:0]  tl_d2h_d_sink;
logic   [top_pkg::TL_DW-1:0]  tl_d2h_d_data;
logic  [top_pkg::TL_DUW-1:0]  tl_d2h_d_user;
logic                         tl_d2h_d_error;

logic                         tl_d2h_a_ready;

assign tl_h2d_a_valid = tl_h2d.a_valid;
assign tl_h2d_a_opcode = tl_h2d.a_opcode;
assign tl_h2d_a_param = tl_h2d.a_param;
assign tl_h2d_a_size = tl_h2d.a_size;
assign tl_h2d_a_source = tl_h2d.a_source;
assign tl_h2d_a_address = tl_h2d.a_address;
assign tl_h2d_a_mask = tl_h2d.a_mask;
assign tl_h2d_a_data = tl_h2d.a_data;
assign tl_h2d_a_user = tl_h2d.a_user;
assign tl_h2d_d_ready = tl_h2d.d_ready;

assign tl_d2h_d_valid = tl_d2h.d_valid;
assign tl_d2h_d_opcode = tl_d2h.d_opcode;
assign tl_d2h_d_param = tl_d2h.d_param;
assign tl_d2h_d_size = tl_d2h.d_size;
assign tl_d2h_d_source = tl_d2h.d_source;
assign tl_d2h_d_sink = tl_d2h.d_sink;
assign tl_d2h_d_data = tl_d2h.d_data;
assign tl_d2h_d_user = tl_d2h.d_user;
assign tl_d2h_d_error = tl_d2h.d_error;
assign tl_d2h_a_ready = tl_d2h.a_ready;

endmodule