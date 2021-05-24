// Copyright lowRISC contributors.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0

// This file is auto-generated.


// This is to prevent AscentLint warnings in the generated
// abstract prim wrapper. These warnings occur due to the .*
// use. TODO: we may want to move these inline waivers
// into a separate, generated waiver file for consistency.
//ri lint_check_off OUTPUT_NOT_DRIVEN INPUT_NOT_READ
module prim_flash

#(

  parameter int NumBanks       = 2,  // number of banks
  parameter int InfosPerBank   = 1,  // info pages per bank
  parameter int InfoTypes      = 1,  // different info types
  parameter int InfoTypesWidth = 1,  // different info types
  parameter int PagesPerBank   = 256,// data pages per bank
  parameter int WordsPerPage   = 256,// words per page
  parameter int DataWidth      = 32, // bits per word
  parameter int MetaDataWidth  = 12, // metadata such as ECC
  parameter int TestModeWidth  = 2

) (
  input clk_i,
  input rst_ni,
  input flash_phy_pkg::flash_phy_prim_flash_req_t [NumBanks-1:0] flash_req_i,
  output flash_phy_pkg::flash_phy_prim_flash_rsp_t [NumBanks-1:0] flash_rsp_o,
  output logic [flash_phy_pkg::ProgTypes-1:0] prog_type_avail_o,
  output init_busy_o,
  input tck_i,
  input tdi_i,
  input tms_i,
  output logic tdo_o,
  input lc_ctrl_pkg::lc_tx_t bist_enable_i,
  input lc_ctrl_pkg::lc_tx_t scanmode_i,
  input scan_en_i,
  input scan_rst_ni,
  input flash_power_ready_h_i,
  input flash_power_down_h_i,
  inout [TestModeWidth-1:0] flash_test_mode_a_io,
  inout flash_test_voltage_h_io,
  output logic flash_err_o,
  output ast_pkg::ast_dif_t fl_alert_src_o,
  input tlul_pkg::tl_h2d_t tl_i,
  output tlul_pkg::tl_d2h_t tl_o,
  input  devmode_i
);

  if (1) begin : gen_generic
    prim_generic_flash #(
      .MetaDataWidth(MetaDataWidth),
      .DataWidth(DataWidth),
      .WordsPerPage(WordsPerPage),
      .InfoTypesWidth(InfoTypesWidth),
      .InfoTypes(InfoTypes),
      .PagesPerBank(PagesPerBank),
      .NumBanks(NumBanks),
      .InfosPerBank(InfosPerBank),
      .TestModeWidth(TestModeWidth)
    ) u_impl_generic (
      .*
    );

  end

endmodule
//ri lint_check_on OUTPUT_NOT_DRIVEN INPUT_NOT_READ
