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

/*
 * Read bytes over UART until we hit a newline or read max length bytes
 */
static size_t uart_read(dif_uart_t *uart, char *buf, size_t max_len) {
  size_t i;
  for (i = 0; i < max_len; i++) {
    dif_uart_byte_receive_polled(uart, (uint8_t*) &buf[i]);
    if (buf[i] == '\r' || buf[i] == '\n') {
      // return i instead of i+1 to trim newline
      return i;
    }
  }
  return i;
}

// Simple program to toggle GPIO pin 0 in a loop

int main() {
    dif_gpio_t gpio;
    gpio_init(&gpio);

    dif_uart_t uart;
    uart_init(&uart);

    size_t written = uart_write(&uart, "Hello world!\r\n", 14);

    bool state = false;
    while (true) {
      char buf[100];
      size_t bytes_read = uart_read(&uart, buf, 100);
      uart_write(&uart, "You said: ", 10);
      uart_write(&uart, buf, bytes_read);
      uart_write(&uart, "\r\n", 2);
      dif_gpio_write(&gpio, 0, state);
      state = !state;
    }
}
