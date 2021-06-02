def setup_floorplan(fp, chip):
    fp.create_die_area(200, 200)

    pins = ['clk', 'rst', 'uart_rx', 'uart_tx'] + [f'gpio[{i}]' for i in range(32)]
    N = len(pins) / 4 # pins per side

    metal = 'm3'
    width = 1
    depth = 3
    fp.place_pins(pins[0:N], 'w', width, depth, metal)
    fp.place_pins(pins[N:2*N], 'n', width, depth, metal)
    fp.place_pins(pins[2*N:3*N], 'e', width, depth, metal)
    fp.place_pins(pins[3*N:], 's', width, depth, metal)

    return fp