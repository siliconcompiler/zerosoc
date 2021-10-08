module asic_iobuf #(
    parameter DIR = "NO",
    parameter TYPE = "SOFT",
    parameter TECH_CFG_WIDTH = 16,
    parameter TECH_RING_WIDTH = 8
) (
    output din,
    input dout,
    input ie,
    input oen,
    input [7:0] cfg,
    inout [TECH_CFG_WIDTH-1:0] tech_cfg,

    inout poc,
    inout vdd,
    inout vss,
    inout vddio,
    inout vssio,
    inout [TECH_RING_WIDTH-1:0] ring,

    inout pad
);

/*
 * Wrapper for Skywater130 gpiov2 pad cell to interface with OH generic padring
 * library.
 *
 * This wrapper must contain wiring only, no logic.
 *
 * Notes:
 * - The logic for `ie` is inverted here -- input is enabled when `ie` is low,
 *   and disabled when `ie` is high.
 * - All signals ending in _h need to use the VDDIO logic level.
 *
 * Documentation:
 * https://skywater-pdk.readthedocs.io/en/latest/contents/libraries/sky130_fd_io/docs/user_guide.html
 */

sky130_ef_io__gpiov2_pad_wrapped gpio (
    .IN(din),
    .OUT(dout),
    .OE_N(oen),
    .INP_DIS(ie),
    .PAD(pad),

    // If 0, hold outputs at current state
    .HLD_H_N(tech_cfg[0]),
    // If 0, hold outputs at hi-z (used on power-up)
    .ENABLE_H(tech_cfg[1]),
    // Determines input buffer state when enable_h is 0. Val doesn't matter when
    // enable_h is 1. Must be tied off to tie_hi_esd or tie_lo_esd.
    .ENABLE_INP_H(tech_cfg[2]),
    // Whether to enable the analog power domain in GPIO cell
    .ENABLE_VDDA_H(tech_cfg[3]),
    // Whether the VSWITCH power supply is enabled
    .ENABLE_VSWITCH_H(tech_cfg[4]),
    // Whether VDDIO is enabled
    .ENABLE_VDDIO(tech_cfg[5]),
    // These signals both control the input voltage threshold
    .IB_MODE_SEL(tech_cfg[6]),
    .VTRIP_SEL(tech_cfg[7]),
    // Output slew rate
    .SLOW(tech_cfg[8]),
    // Determine "flow-through" functionality when hld_h_n = 0
    .HLD_OVR(tech_cfg[9]),
    // Whether to enable analog functionality
    .ANALOG_EN(tech_cfg[10]),
    // Select between AMUXBUS_A and AMUXBUS_B
    .ANALOG_SEL(tech_cfg[11]),
    // Selects output polarity in analog mode
    .ANALOG_POL(tech_cfg[12]),
    // Drive strength
    .DM(tech_cfg[15:13]),

    .VDDIO(vddio),
    // level-shift reference for high-voltage output
    .VDDIO_Q(ring[0]),
    .VDDA(ring[6]),
    // core supply as level-shift reference
    .VCCD(vdd),
    .VSWITCH(ring[1]),
    .VCCHIB(ring[2]),
    .VSSA(ring[7]),
    .VSSD(vss),
    .VSSIO_Q(ring[3]),
    .VSSIO(vssio),

    // Direct connection from pad to core (unused)
    .PAD_A_NOESD_H(),
    .PAD_A_ESD_0_H(),
    .PAD_A_ESD_1_H(),

    // Analog stuff (unused)
    .AMUXBUS_A(ring[4]),
    .AMUXBUS_B(ring[5]),

    // Input signal in IO power domain
    .IN_H(),

    // These are used to tie off enable_inp_h
    .TIE_LO_ESD(tech_cfg[16]),
    .TIE_HI_ESD(tech_cfg[17])
);


endmodule
