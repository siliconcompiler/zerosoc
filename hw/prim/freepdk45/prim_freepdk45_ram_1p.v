module prim_freepdk45_ram_1p
import prim_ram_1p_pkg::*;
#(

  parameter  int Width           = 32, // bit
  parameter  int Depth           = 128,
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

generate
  if (Width == 32 && Depth == 2048) begin
    sram_32x2048_1rw mem (
      .rd_out(rdata_o),
      .addr_in(addr_i),
      .we_in(write_i),
      .wd_in(wdata_i),
      .w_mask_in(wmask_i),
      .clk(clk_i),
      .ce_in(req_i)
    );
  end else begin
    // error!
  end
endgenerate

endmodule
