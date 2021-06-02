module pad (
    input out_i,
    input oe_i,
    output in_o,

    inout inout_io
);
    assign in_o = inout_io;
    assign inout_io = oe_i ? out_i : 1'bz;
endmodule
