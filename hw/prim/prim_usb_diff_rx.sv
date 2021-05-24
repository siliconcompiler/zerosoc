// Copyright lowRISC contributors.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0

// This file is auto-generated.


// This is to prevent AscentLint warnings in the generated
// abstract prim wrapper. These warnings occur due to the .*
// use. TODO: we may want to move these inline waivers
// into a separate, generated waiver file for consistency.
//ri lint_check_off OUTPUT_NOT_DRIVEN INPUT_NOT_READ
module prim_usb_diff_rx

#(

  parameter int CalibW = 32

) (
  input wire         input_pi,      // differential input
  input wire         input_ni,      // differential input
  input              input_en_i,    // input buffer enable
  input              core_pok_i,    // core power indication at VCC level
  input              pullup_p_en_i, // pullup enable for P
  input              pullup_n_en_i, // pullup enable for N
  input [CalibW-1:0] calibration_i, // calibration input
  output logic       input_o        // output of differential input buffer
);

  if (1) begin : gen_generic
    prim_generic_usb_diff_rx #(
      .CalibW(CalibW)
    ) u_impl_generic (
      .*
    );

  end

endmodule
//ri lint_check_on OUTPUT_NOT_DRIVEN INPUT_NOT_READ
