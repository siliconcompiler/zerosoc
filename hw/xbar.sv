module xbar (
    input clk_i,
    input rst_ni,
    input tlul_pkg::tl_h2d_t tl_corei_i,
    output tlul_pkg::tl_d2h_t tl_corei_o,
    input tlul_pkg::tl_h2d_t tl_cored_i,
    output tlul_pkg::tl_d2h_t tl_cored_o,
    input tlul_pkg::tl_h2d_t tl_ram_i,
    output tlul_pkg::tl_d2h_t tl_ram_o,
    input tlul_pkg::tl_h2d_t tl_uart_i,
    output tlul_pkg::tl_d2h_t tl_uart_o,
    input tlul_pkg::tl_h2d_t tl_gpio_i,
    output tlul_pkg::tl_d2h_t tl_gpio_o,
  );
  import tlul_pkg::*;
  import xbar_pkg::*;

  tl_h2d_t tl_dmem_out_arb_h2d [3];
  tl_d2h_t tl_dmem_out_arb_d2h [3];
  tl_h2d_t tl_ram_in_arb_h2d [2];
  tl_d2h_t tl_ram_in_arb_d2h [2];

  assign tl_ram_in_arb_h2d[0] = tl_dmem_out_arb_h2d[0];
  assign tl_dmem_out_arb_d2h[0] = tl_ram_in_arb_d2h[0];
  assign tl_ram_in_arb_h2d[1] = tl_corei_i;
  assign tl_corei_o = tl_ram_in_arb_d2h[1];

  assign tl_gpio_o = tl_dmem_out_arb_h2d[1];
  assign tl_dmem_out_arb_d2h[1] = tl_gpio_i;
  assign tl_uart_o = tl_dmem_out_arb_h2d[2];
  assign tl_dmem_out_arb_d2h[2] = tl_uart_i;

  logic [1:0] dev_sel_dmem_out_arb;

  always_comb begin
    // default steering to generate error response if address is not within the range
    dev_sel_dmem_out_arb = 2'd3;
    if ((tl_cored_i.a_address & ~(ADDR_MASK_RAM)) == ADDR_SPACE_RAM) begin
      dev_sel_dmem_out_arb = 2'd0;
    end else if ((tl_cored_i.a_address & ~(ADDR_MASK_GPIO)) == ADDR_SPACE_GPIO) begin
      dev_sel_dmem_out_arb = 2'd1;
    end else if ((tl_cored_i.a_address & ~(ADDR_MASK_UART)) == ADDR_SPACE_UART) begin
      dev_sel_dmem_out_arb = 2'd2;
    end
  end

  tlul_socket_1n #(
    .HReqDepth (4'h0),
    .HRspDepth (4'h0),
    .DReqDepth (16'h0),
    .DRspDepth (16'h0),
    .N         (3)
  ) dmem_out_arb (
    .clk_i        (clk_i),
    .rst_ni       (rst_ni),
    .tl_h_i       (tl_cored_i),
    .tl_h_o       (tl_cored_o),
    .tl_d_o       (tl_dmem_out_arb_h2d),
    .tl_d_i       (tl_dmem_out_arb_d2h),
    .dev_select_i (dev_sel_dmem_out_arb)
  );

  tlul_socket_m1 #(
    .HReqDepth (12'h0),
    .HRspDepth (12'h0),
    .DReqDepth (4'h0),
    .DRspDepth (4'h0),
    .M         (2)
  ) ram_in_arb (
    .clk_i        (clk_i),
    .rst_ni       (rst_ni),
    .tl_h_i       (tl_ram_in_arb_h2d),
    .tl_h_o       (tl_ram_in_arb_d2h),
    .tl_d_i       (tl_ram_o),
    .tl_d_o       (tl_ram_i)
  );

 endmodule