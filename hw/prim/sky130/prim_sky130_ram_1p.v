module prim_sky130_ram_1p
import prim_ram_1p_pkg::*;
#(

  parameter  int Width           = 32, // bit
  parameter  int Depth           = 512,
  parameter  int DataBitsPerMask = 1, // Number of data bits per bit of write mask
  parameter      MemInitFile     = "", // VMEM file to initialize the memory with

  localparam int Aw              = $clog2(Depth)  // derived parameter

) (
  input  logic             clk_i,

  input  logic             req_i,
  input  logic             write_i,
  input  logic [Aw-1:0]    addr_i,
  input  logic [Width-1:0] wdata_i,
  input  logic [Width-1:0] wmask_i,
  output logic [Width-1:0] rdata_o, // Read data. Data is returned one cycle after req_i is high.
  input ram_1p_cfg_t       cfg_i
);

la_spram #(.DW(Width), .AW(Aw)) mem(
  .clk(clk_i),
  .ce(req_i),
  .we(write_i),
  .wmask(wmask_i),
  .addr(addr_i),
  .din(wdata_i),
  .dout(rdata_o)
);

endmodule
