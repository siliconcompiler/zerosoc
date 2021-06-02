module top_asic (
    input clk,
    input rst,

    input uart_rx,
    output uart_tx,

    inout [31:0] gpio
);

    wire uart_tx_o;
    wire uart_tx_en_o;

    wire [31:0] gpio_i;
    wire [31:0] gpio_o;
    wire [31:0] gpio_en_o;

    // Instantiate SoC
    zerosoc soc (
        .clk_i(clk),
        .rst_ni(rst),

        .uart_rx_i(uart_rx),
        .uart_tx_o(uart_tx_o),
        .uart_tx_en_o(uart_tx_en_o),

        .gpio_i(gpio_i),
        .gpio_o(gpio_o),
        .gpio_en_o(gpio_en_o)
    );

    // Padring
    pad uart_tx_pad (
        .out_i(uart_tx_o),
        .oe_i(uart_tx_en_o),
        .in_o(),

        .inout_io(uart_tx)
    );

    generate
        genvar i;
        for (i = 0; i < 32; i++) begin : gen_gpio_pads
            pad gpio_pad (
                .out_i(gpio_o[i]),
                .oe_i(gpio_en_o[i]),
                .in_o(gpio_i[i]),

                .inout_io(gpio[i])
            );
        end
    endgenerate

endmodule
