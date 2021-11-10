module prim_ice40_clock_gating #(
    parameter bit NoFpgaGate = 1'b0
  ) (
    input        clk_i,
    input        en_i,
    input        test_en_i,
    output logic clk_o
  );

  // TODO: can implement a proper clock gate using SB_GB_IO primitive
 
  assign clk_o = clk_i;
  
endmodule
