#include <stdio.h>

#include "lib/peripherals.h"

#include "sw/device/lib/dif/dif_gpio.h"
#include "sw/device/lib/dif/dif_uart.h"

// Simple program to toggle GPIO pin 0 in a loop

int main() {
  dif_gpio_t gpio;
  gpio_init(&gpio);

  dif_uart_t uart;
  uart_init(&uart);

  size_t written = uart_write(&uart, "Hello world!\r\n", 14);

  bool state = false;
  while (true)
  {
    dif_gpio_write(&gpio, 0, state);
    state = !state;
    sleep_ms(1000);
    }
}
