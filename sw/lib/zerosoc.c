#include "zerosoc.h"

#include "sw/device/lib/dif/dif_gpio.h"
#include "sw/device/lib/dif/dif_uart.h"

#define CLOCK_FREQ 6000000ULL
#define RAM_BASE_ADDR  0x00000000
#define UART_BASE_ADDR 0x40000000
#define GPIO_BASE_ADDR 0x40010000

bool init_peripherals(zerosoc_t *soc) {
    dif_gpio_params_t gpio_params = { mmio_region_from_addr(GPIO_BASE_ADDR) };
    if (dif_gpio_init(gpio_params, &soc->gpio) != kDifGpioOk)
      return false;

    dif_uart_params_t uart_params = { mmio_region_from_addr(UART_BASE_ADDR) };
    if (dif_uart_init(uart_params, &soc->uart) != kDifUartOk)
      return false;

    dif_uart_config_t config;
    config.baudrate = 9600;
    config.clk_freq_hz = CLOCK_FREQ;
    config.parity_enable = kDifUartToggleDisabled;
    config.parity = kDifUartParityEven;

    if (dif_uart_configure(&soc->uart, config) != kDifUartOk)
      return false;

    return true;
}

bool gpio_read(zerosoc_t *soc, int pin) {
    bool state;
    dif_gpio_result_t res = dif_gpio_read(&soc->gpio, pin, &state);
    return state;
}

void gpio_write(zerosoc_t *soc, int pin, bool state) {
    dif_gpio_result_t res = dif_gpio_write(&soc->gpio, pin, state);
}

size_t uart_write(zerosoc_t *soc, const char *buf, size_t len) {
  for (size_t i = 0; i < len; ++i) {
    if (dif_uart_byte_send_polled(&soc->uart, (uint8_t)buf[i]) != kDifUartOk) {
      return i;
    }
  }
  return len;
}

size_t uart_read(zerosoc_t *soc, char *buf, size_t max_len) {
  size_t i;
  for (i = 0; i < max_len; i++) {
    if (dif_uart_byte_receive_polled(&soc->uart, (uint8_t*) &buf[i]) != kDifUartOk)
      return i;

    if (buf[i] == '\r' || buf[i] == '\n') {
      // return i instead of i+1 to trim newline
      return i;
    }
  }
  return i;
}

size_t uart_bytes_available(zerosoc_t *soc) {
    size_t bytes;
    if (dif_uart_rx_bytes_available(&soc->uart, &bytes) != kDifUartOk)
      return -1;

    return bytes;
}

void delay(unsigned long msec) {
  unsigned long usec_cycles = (CLOCK_FREQ / 1000 / 8) * msec;

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
    return cycles / (CLOCK_FREQ / 1000);
}
