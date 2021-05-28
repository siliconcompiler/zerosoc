#include "sw/device/lib/dif/dif_gpio.h"
#include "sw/device/lib/dif/dif_uart.h"

#include <stdio.h>

#include "devices.h"

void gpio_init (dif_gpio_t *gpio) {
    dif_gpio_params_t params = { mmio_region_from_addr(GPIO_BASE_ADDR) };
    dif_gpio_result_t res = dif_gpio_init(params, gpio);
}

void uart_init (dif_uart_t *uart) {
    dif_uart_params_t params = { mmio_region_from_addr(UART_BASE_ADDR) };
    dif_uart_result_t res = dif_uart_init(params, uart);

    dif_uart_config_t config;
    config.baudrate = 9600;
    config.clk_freq_hz = 6100000;
    config.parity_enable = kDifUartToggleDisabled;
    config.parity = kDifUartParityEven;

    dif_uart_configure(uart, config);
}

static size_t uart_write(dif_uart_t *uart, const char *buf, size_t len) {
  for (size_t i = 0; i < len; ++i) {
    if (dif_uart_byte_send_polled(uart, (uint8_t)buf[i]) != kDifUartOk) {
      return i;
    }
  }
  return len;
}

// Simple program to toggle GPIO pin 0 in a loop

int main() {
    dif_gpio_t gpio;
    gpio_init(&gpio);

    dif_uart_t uart;
    uart_init(&uart);

    size_t written = uart_write(&uart, "Hello world!\r\n", 13);

    bool state = false;
    while (true) {
        uart_write(&uart, state ? "on!\r\n" : "off\r\n", 5);
        for (int i = 0; i < 10000; i++) {
            // hacky way to get delay - write same value to GPIO in big loop
            // (empty loop doesn't work with optimization on)
            dif_gpio_write(&gpio, 0, state);
        }
        state = !state;
    }
}
