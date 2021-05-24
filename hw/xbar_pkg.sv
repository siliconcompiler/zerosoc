package xbar_pkg;

  localparam logic [31:0] ADDR_SPACE_RAM         = 32'h 10000000;
  localparam logic [31:0] ADDR_SPACE_UART        = 32'h 40000000;
  localparam logic [31:0] ADDR_SPACE_GPIO        = 32'h 40010000;

  localparam logic [31:0] ADDR_MASK_RAM          = 32'h 000007ff;
  localparam logic [31:0] ADDR_MASK_UART         = 32'h 00000fff;
  localparam logic [31:0] ADDR_MASK_GPIO         = 32'h 00000fff;

endpackage
