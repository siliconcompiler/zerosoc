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
// CELLMAP = {PROP[7:0],SECTION[7:0],CELL[7:0],COMP[7:0],PIN[7:0]}
//##################################################

`include "la_iopadring.vh"

localparam CELLMAP = { // GPIO SECTION
                       {8'h0, 8'h0, LA_VSS,   8'h0, PIN_NONE},
                       {8'h0, 8'h0, LA_VDD,   8'h0, PIN_NONE},
                       {8'h0, 8'h0, LA_VDDIO, 8'h0, PIN_NONE},
                       {8'h0, 8'h0, LA_VSSIO, 8'h0, PIN_NONE},
                       {8'h0, 8'h0, LA_BIDIR, 8'h0, PIN_IO0},
                       {8'h0, 8'h0, LA_BIDIR, 8'h0, PIN_IO1},
                       {8'h0, 8'h0, LA_BIDIR, 8'h0, PIN_IO2},
                       {8'h0, 8'h0, LA_BIDIR, 8'h0, PIN_IO3},
                       {8'h0, 8'h0, LA_BIDIR, 8'h0, PIN_IO4},
                       {8'h0, 8'h0, LA_BIDIR, 8'h0, PIN_IO5},
                       {8'h0, 8'h0, LA_BIDIR, 8'h0, PIN_IO6},
                       {8'h0, 8'h0, LA_BIDIR, 8'h0, PIN_IO7},
                       {8'h0, 8'h0, LA_BIDIR, 8'h0, PIN_IO8}};
