#ifndef PERIPHERALS_H

#define PERIPHERALS_H

#include "sw/device/lib/dif/dif_gpio.h"
#include "sw/device/lib/dif/dif_uart.h"

typedef struct zerosoc_t {
    dif_gpio_t gpio;
    dif_uart_t uart;
} zerosoc_t;

bool init_peripherals(zerosoc_t *soc);

bool gpio_read(zerosoc_t *soc, int pin);
void gpio_write(zerosoc_t *soc, int pin, bool state);

void uart_init (zerosoc_t *soc);
size_t uart_write(zerosoc_t *soc, const char *buf, size_t len);
/*
 * Read bytes over UART until we hit a newline or read max length bytes
 */
size_t uart_read(zerosoc_t *soc, char *buf, size_t max_len);
size_t uart_bytes_available(zerosoc_t *soc);

void delay(unsigned long msec);
uint64_t millis();

#endif
