module asic_iobuf #(
    parameter DIR = "NO",
    parameter TYPE = "SOFT"
) (
    output din,
    input dout,
    input ie,
    input oen,
    input [7:0] cfg,

    inout poc,
    inout vdd,
    inout vss,
    inout vddio,
    inout vssio,

    inout pad
);

// TODO: hook up IO buffer config
//#  0    = pull_enable (1=enable)
//#  1    = pull_select (1=pull up)
//#  2    = slew limiter
//#  3    = shmitt trigger enable
//#  4    = ds[0]
//#  5    = ds[1]
//#  6    = ds[2]
//#  7    = ds[3]

// TODO: should do something with poc signal? maybe this has to do with
// power-on ramp pins such as enable_h

// TODO: might need to use "tielo"/"tiehi" signals for each of these instead of
// 0/1 constants -- see https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/designs/sky130hd/coyote_tc/ios.v

sky130_ef_io__gpiov2_pad_wrapped gpio ( 
    .OUT(dout),
    .OE_N(oen),
    .HLD_H_N(), // if 0, hold outputs at current state
    .ENABLE_H(), // if 0, hold outputs at hi-z (used on power-up)
    .ENABLE_INP_H(), // val doesn't matter when enable_h = 1
    .ENABLE_VDDA_H(),
    .ENABLE_VSWITCH_H(),
    .ENABLE_VDDIO(),
    .INP_DIS(~ie), // disable input when ie low
    .IB_MODE_SEL(), // use vddio based threshold
    .VTRIP_SEL(), // use cmos threshold
    .SLOW(),
    .HLD_OVR(), // don't care when hld_h_n = 1
    .ANALOG_EN(), // disable analog functionality
    .ANALOG_SEL(), // don't care
    .ANALOG_POL(), // don't care
    .DM(), // strong pull-up, strong pull-down
    .VDDIO(),
    .VDDIO_Q(), // level-shift reference for high-voltage output
    .VDDA(), // tied off to vddio b/c analog functionality not used
    .VCCD(), // core supply as level-shift reference
    .VSWITCH(), // not sure what this is for, but seems like vdda = vddio
    .VCCHIB(),
    .VSSA(),
    .VSSD(),
    .VSSIO_Q(),
    .VSSIO(),
    .PAD(pad),
    
    // Direction connection from pad to core (unused)
    .PAD_A_NOESD_H(),
    .PAD_A_ESD_0_H(),
    .PAD_A_ESD_1_H(),

    // Analog stuff (unused)
    .AMUXBUS_A(),
    .AMUXBUS_B(),

    .IN(din),
    // not sure what this output does, so leave disconnected
    .IN_H(),

    // these are used to control enable_inp_h, but we don't care about its val
    // so leave disconnected
    .TIE_HI_ESD(), 
    .TIE_LO_ESD()
);


endmodule
