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

wire [3:0] wmask;

assign wmask[0] = &wmask_i[7:0];
assign wmask[1] = &wmask_i[15:8];
assign wmask[2] = &wmask_i[23:16];
assign wmask[3] = &wmask_i[31:24];

generate
  if (Width == 32 && Depth == 512) begin : gen32x512
    sky130_sram_2kbyte_1rw1r_32x512_8 mem(
      .clk0(clk_i),
      .csb0(~req_i),
      .web0(~write_i),
      .wmask0(wmask),
      .addr0(addr_i),
      .din0(wdata_i),
      .dout0(rdata_o)
    );
  end else begin
    // error!
  end
endgenerate

endmodule
