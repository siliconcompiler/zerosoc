module zerosoc_tb();

reg clk;
reg rst;

wire uart_tx, uart_tx_en;
wire [31:0] gpio, gpio_en;

zerosoc #(
    .RamInitFile("sw/hello.mem")
) uut (
    .clk_i(clk),
    .rst_ni(rst),
    .uart_rx_i(1'b0),
    .uart_tx_o(uart_tx),
    .uart_tx_en_o(uart_tx_en),
    .gpio_i(32'b0),
    .gpio_o(gpio),
    .gpio_en_o(gpio_en)
);

initial begin
    forever #1 clk = !clk;
end

initial begin
    clk = 1'b0;
    rst = 1'b1;
    #5;
    rst = 1'b0;
    #5;
    rst = 1'b1;
    #10000;
    $finish;
end

initial begin
    // Set variables to be dumped to vcd file here
    $dumpfile("zerosoc.vcd");
    $dumpvars;
end

endmodule
