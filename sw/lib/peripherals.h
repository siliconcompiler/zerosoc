#ifndef PERIPHERALS_H

#define PERIPHERALS_H

#include "sw/device/lib/dif/dif_gpio.h"
#include "sw/device/lib/dif/dif_uart.h"

#define RAM_BASE_ADDR  0x00000000
#define UART_BASE_ADDR 0x40000000
#define GPIO_BASE_ADDR 0x40010000

void sleep_ms(unsigned long msec);
uint64_t millis();

void gpio_init (dif_gpio_t *gpio);
bool gpio_read(dif_gpio_t *gpio, int pin);
void gpio_write(dif_gpio_t *gpio, int pin, bool state);

void uart_init (dif_uart_t *uart);

size_t uart_write(dif_uart_t *uart, const char *buf, size_t len);
/*
 * Read bytes over UART until we hit a newline or read max length bytes
 */
size_t uart_read(dif_uart_t *uart, char *buf, size_t max_len);

bool uart_available(dif_uart_t *uart);

#endif
