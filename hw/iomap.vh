//##################################################
// PIN ORDER (PER SIDE)
//##################################################

localparam [7:0] PIN_IO0     = 8'h00;
localparam [7:0] PIN_IO1     = 8'h01;
localparam [7:0] PIN_IO2     = 8'h02;
localparam [7:0] PIN_IO3     = 8'h03;
localparam [7:0] PIN_IO4     = 8'h04;
localparam [7:0] PIN_IO5     = 8'h05;
localparam [7:0] PIN_IO6     = 8'h06;
localparam [7:0] PIN_IO7     = 8'h07;
localparam [7:0] PIN_IO8     = 8'h08;

localparam [7:0] PIN_NONE     = 8'hFF;

//##################################################
// CELLMAP = {SECTION#,PIN#,CELLTYPE}
//##################################################

`include "la_iopadring.vh"

localparam CELLMAP = { // GPIO SECTION
                       {8'h0,PIN_NONE,LA_VSS},
                       {8'h0,PIN_NONE,LA_VDD},
                       {8'h0,PIN_NONE,LA_VDDIO},
                       {8'h0,PIN_NONE,LA_VSSIO},
                       {8'h0,PIN_IO0,LA_BIDIR},
                       {8'h0,PIN_IO1,LA_BIDIR},
                       {8'h0,PIN_IO2,LA_BIDIR},
                       {8'h0,PIN_IO3,LA_BIDIR},
                       {8'h0,PIN_IO4,LA_BIDIR},
                       {8'h0,PIN_IO5,LA_BIDIR},
                       {8'h0,PIN_IO6,LA_BIDIR},
                       {8'h0,PIN_IO7,LA_BIDIR},
                       {8'h0,PIN_IO8,LA_BIDIR}};
