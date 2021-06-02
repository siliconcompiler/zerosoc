#include "lib/zerosoc.h"

const int MIN_DELAY = 100;
const int DEFAULT_DELAY = 800;
const int MAX_DELAY = 1500;
const int DELAY_INC = 100;

int main() {
  zerosoc_t soc;
  init_peripherals(&soc);

  uart_write(&soc, "Hello world!\r\n", 14);

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
      gpio_write(&soc, led, false);
      led++;
      if (led >= 5) led = 0;
      gpio_write(&soc, led, true);
      last_changed = millis();
    }

    // Read UART
    // expect "f", "s", or "r"
    char cmd = '\0';
    if (uart_bytes_available(&soc) > 0) {
      uart_read(&soc, &cmd, 1);
    }

    // Read buttons
    btn1 = gpio_read(&soc, 0);
    bool btn1_up = btn1 && !prev_btn1;
    prev_btn1 = btn1;

    btn2 = gpio_read(&soc, 1);
    bool btn2_up = btn2 && !prev_btn2;
    prev_btn2 = btn2;

    btn3 = gpio_read(&soc, 2);
    bool btn3_up = btn3 && !prev_btn3;
    prev_btn3 = btn3;

    // Adjust `time` accordingly based on input
    if (cmd == 's' || btn1_up) {
      time += DELAY_INC;
      if (time > MAX_DELAY) time = MAX_DELAY;
      uart_write(&soc, "Slower...\r\n", 11);
    }

    if (cmd == 'r' || btn2_up) {
      time = DEFAULT_DELAY;
      uart_write(&soc, "Reset...\r\n", 10);
    }

    if (cmd == 'f' || btn3_up) {
      time -= DELAY_INC;
      if (time < MIN_DELAY) time = MIN_DELAY;
      uart_write(&soc, "Faster...\r\n", 11);
    }
  }
}
