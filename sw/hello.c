#include "sw/device/lib/dif/dif_gpio.h"

#include "devices.h"

// Simple program to toggle GPIO pin 0 in a loop

int main() {
    dif_gpio_t gpio;

    dif_gpio_params_t gpio_params = { mmio_region_from_addr(GPIO_BASE_ADDR) };

    dif_gpio_result_t res = dif_gpio_init(gpio_params, &gpio);

    bool state = false;
    while (true) {
        res = dif_gpio_write(&gpio, 0, state);
        state = !state;

        for (int i = 0; i < 5; i++);
    }
}