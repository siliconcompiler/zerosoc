#include <stdio.h>

#include "lib/peripherals.h"

#include "sw/device/lib/dif/dif_gpio.h"
#include "sw/device/lib/dif/dif_uart.h"

const int MIN_DELAY = 100;
const int DEFAULT_DELAY = 800;
const int MAX_DELAY = 1500;
const int DELAY_INC = 100;

int main() {
  dif_gpio_t gpio;
  gpio_init(&gpio);

  dif_uart_t uart;
  uart_init(&uart);

  size_t written = uart_write(&uart, "Hello world!\r\n", 14);

  bool btn1, btn2, btn3;
  bool prev_btn1 = false;
  bool prev_btn2 = false;
  bool prev_btn3 = false;

  int led = 0;
  int time = DEFAULT_DELAY;
  uint64_t last_changed = millis();

  while (true) {
    // Light up next LED after `time` milliseconds elapse
    if (millis() - last_changed > time) {
      gpio_write(&gpio, led, false);
      led++;
      if (led >= 5) led = 0;
      gpio_write(&gpio, led, true);
      last_changed = millis();
    }

    // Read UART
    // expect "f", "s", or "r"
    char cmd = '\0';
    if (uart_available(&uart)) {
      uart_read(&uart, &cmd, 1);
    }

    // Read buttons
    btn1 = gpio_read(&gpio, 0);
    bool btn1_up = btn1 && !prev_btn1;
    prev_btn1 = btn1;

    btn2 = gpio_read(&gpio, 1);
    bool btn2_up = btn2 && !prev_btn2;
    prev_btn2 = btn2;

    btn3 = gpio_read(&gpio, 2);
    bool btn3_up = btn3 && !prev_btn3;
    prev_btn3 = btn3;

    // Adjust `time` accordingly based on input
    if (cmd == 's' || btn1_up) {
      time += DELAY_INC;
      if (time > MAX_DELAY) time = MAX_DELAY;
      uart_write(&uart, "Slower...\r\n", 11);
    }

    if (cmd == 'r' || btn2_up) {
      time = DEFAULT_DELAY;
      uart_write(&uart, "Reset...\r\n", 10);
    }

    if (cmd == 'f' || btn3_up) {
      time -= DELAY_INC;
      if (time < MIN_DELAY) time = MIN_DELAY;
      uart_write(&uart, "Faster...\r\n", 11);
    }
  }
}
