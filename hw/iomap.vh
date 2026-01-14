//##################################################
// PIN ORDER (PER SIDE)
//##################################################

localparam [15:0] PIN_IO0     = 16'h0000;
localparam [15:0] PIN_IO1     = 16'h0001;
localparam [15:0] PIN_IO2     = 16'h0002;
localparam [15:0] PIN_IO3     = 16'h0003;
localparam [15:0] PIN_IO4     = 16'h0004;
localparam [15:0] PIN_IO5     = 16'h0005;
localparam [15:0] PIN_IO6     = 16'h0006;
localparam [15:0] PIN_IO7     = 16'h0007;
localparam [15:0] PIN_IO8     = 16'h0008;

localparam [15:0] PIN_NONE     = 16'h00FF;

//##################################################
// CELLMAP = {PROP[15:0],SECTION[15:0],CELL[15:0],COMP[15:0],PIN[15:0]}
//##################################################

`include "la_padring.vh"

localparam CELLMAP = { // GPIO SECTION
                       {16'h0000, 16'h0000, LA_VSS,   16'h0000, PIN_NONE},
                       {16'h0000, 16'h0000, LA_VDD,   16'h0000, PIN_NONE},
                       {16'h0000, 16'h0000, LA_VDDIO, 16'h0000, PIN_NONE},
                       {16'h0000, 16'h0000, LA_VSSIO, 16'h0000, PIN_NONE},
                       {16'h0000, 16'h0000, LA_BIDIR, 16'h0000, PIN_IO0},
                       {16'h0000, 16'h0000, LA_BIDIR, 16'h0000, PIN_IO1},
                       {16'h0000, 16'h0000, LA_BIDIR, 16'h0000, PIN_IO2},
                       {16'h0000, 16'h0000, LA_BIDIR, 16'h0000, PIN_IO3},
                       {16'h0000, 16'h0000, LA_BIDIR, 16'h0000, PIN_IO4},
                       {16'h0000, 16'h0000, LA_BIDIR, 16'h0000, PIN_IO5},
                       {16'h0000, 16'h0000, LA_BIDIR, 16'h0000, PIN_IO6},
                       {16'h0000, 16'h0000, LA_BIDIR, 16'h0000, PIN_IO7},
                       {16'h0000, 16'h0000, LA_BIDIR, 16'h0000, PIN_IO8}};
