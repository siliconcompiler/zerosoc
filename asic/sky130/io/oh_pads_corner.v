//#############################################################################
//# Function: Corner Pads                                                     #
//# Copyright: OH Project Authors. ALl rights Reserved.                       #
//# License:  MIT (see LICENSE file in OH repository)                         # 
//#############################################################################

module oh_pads_corner
  (//feed through signals
   inout 	       vddio, // io supply
   inout 	       vssio, // io ground
   inout 	       vdd, // core supply
   inout 	       vss // common ground
   );

  sky130_ef_io__corner_pad corner (
    .VDDIO(),
    .VDDIO_Q(),
    .VDDA(),
    .VCCD(),
    .VSWITCH(),
    .VCCHIB(),
    .VSSA(),
    .VSSD(),
    .VSSIO_Q(),
    .VSSIO(),

    .AMUXBUS_A(),
    .AMUXBUS_B()
  );

endmodule // oh_pads_corner

