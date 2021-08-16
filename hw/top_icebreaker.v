module top_icebreaker (
    input CLK,
    input BTN_N,

	input RX,
  	output TX,

    input BTN1,
    input BTN2,
    input BTN3,

    output LED1,
    output LED2,
    output LED3,
    output LED4,
    output LED5
);

    wire clk_6mhz;

    SB_HFOSC #(
        .CLKHF_DIV("0b11") // 6mhz
    ) clock_gen (
        .CLKHFPU(1'b1),
        .CLKHFEN(1'b1),
        .CLKHF(clk_6mhz)
    );

    wire [2:0] gpio_in;
    assign gpio_in[0] = BTN1;
    assign gpio_in[1] = BTN2;
    assign gpio_in[2] = BTN3;

    wire [31:0] gpio_out;
    assign LED1 = gpio_out[0];
    assign LED2 = gpio_out[1];
    assign LED3 = gpio_out[2];
    assign LED4 = gpio_out[3];
    assign LED5 = gpio_out[4];

`define MAKE_MEM_PATH(filename) `"`MEM_ROOT/filename`"

    zerosoc #(
        .RamInitFile(`MAKE_MEM_PATH(random.mem)),
        .RamDepth(2048),
        .ASIC(0)
    ) soc(
        .clk_i(clk_6mhz),
        .rst_ni(BTN_N),

        .uart_rx_i(RX),
        .uart_tx_o(TX),
        .uart_tx_en_o(),

        .gpio_i({29'b0, gpio_in}),
        .gpio_o(gpio_out),
        .gpio_en_o()
    );

endmodule
