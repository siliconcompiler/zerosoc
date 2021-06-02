#include "peripherals.h"

#include "sw/device/lib/dif/dif_gpio.h"
#include "sw/device/lib/dif/dif_uart.h"

#define LOOPS_PER_MSEC (6 * 125) // 6 MHz *  1/1000 sec/ms * 8 cycles/loop

void sleep_ms(unsigned long msec) {
  unsigned long usec_cycles = LOOPS_PER_MSEC * msec;

  int out; /* only to notify compiler of modifications to |loops| */
  asm volatile(
      "1: nop             \n" // 1 cycle
      "   nop             \n" // 1 cycle
      "   nop             \n" // 1 cycle
      "   nop             \n" // 1 cycle
      "   addi %1, %1, -1 \n" // 1 cycle
      "   bnez %1, 1b     \n" // 3 cycles
      : "=&r" (out)
      : "0" (usec_cycles)
  );
}

uint64_t mcycle_read(void) {
  uint32_t cycle_low = 0;
  uint32_t cycle_high = 0;
  uint32_t cycle_high_2 = 0;
  asm volatile(
      "read%=:"
      "  csrr %0, mcycleh;"     // Read `mcycleh`.
      "  csrr %1, mcycle;"      // Read `mcycle`.
      "  csrr %2, mcycleh;"     // Read `mcycleh` again.
      "  bne  %0, %2, read%=;"  // Try again if `mcycle` overflowed before
                                // reading `mcycleh`.
      : "+r"(cycle_high), "=r"(cycle_low), "+r"(cycle_high_2)
      :);
  return (uint64_t)cycle_high << 32 | cycle_low;
}

uint64_t millis() {
    uint64_t cycles = mcycle_read();
    return cycles / 6000;
}

void gpio_init (dif_gpio_t *gpio) {
    dif_gpio_params_t params = { mmio_region_from_addr(GPIO_BASE_ADDR) };
    dif_gpio_result_t res = dif_gpio_init(params, gpio);
}

bool gpio_read(dif_gpio_t *gpio, int pin) {
    bool state;
    dif_gpio_read(gpio, pin, &state);
    return state;
}

void gpio_write(dif_gpio_t *gpio, int pin, bool state) {
    dif_gpio_write(gpio, pin, state);
}

void uart_init (dif_uart_t *uart) {
    dif_uart_params_t params = { mmio_region_from_addr(UART_BASE_ADDR) };
    dif_uart_result_t res = dif_uart_init(params, uart);

    dif_uart_config_t config;
    config.baudrate = 9600;
    config.clk_freq_hz = 6000000;
    config.parity_enable = kDifUartToggleDisabled;
    config.parity = kDifUartParityEven;

    dif_uart_configure(uart, config);
}

size_t uart_write(dif_uart_t *uart, const char *buf, size_t len) {
  for (size_t i = 0; i < len; ++i) {
    if (dif_uart_byte_send_polled(uart, (uint8_t)buf[i]) != kDifUartOk) {
      return i;
    }
  }
  return len;
}

size_t uart_read(dif_uart_t *uart, char *buf, size_t max_len) {
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

bool uart_available(dif_uart_t *uart) {
    size_t bytes;
    dif_uart_rx_bytes_available(uart, &bytes);

    return bytes > 0;
}
