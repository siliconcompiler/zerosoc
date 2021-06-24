def setup_floorplan(fp, chip):
    # TODO: would be nice to have die area calculated from Yosys
    # stuff/utilization
    # TODO: would be nice to have core area calculated based on pad cell heights
    fp.create_die_area(200, 200, core_area=())

    pins_w = ['gpio[{i}]' for i in range(5)] + ['vss1', 'vdd1', 'vddio1'] + ['clk', 'rst', 'uart_rx', 'uart_tx']
    pins_n = ['gpio[{i}]' for i in range(5, 10)] + ['vss2', 'vdd2', 'vddio2'] + ['gpio[{i}]' for i in range(10, 14)]
    pins_e = ['gpio[{i}]' for i in range(14, 19)] + ['vss2', 'vdd2', 'vddio2'] + ['gpio[{i}]' for i in range(19, 23)]
    pins_s = ['gpio[{i}]' for i in range(23, 28)] + ['vss3', 'vdd3', 'vddio3'] + ['gpio[{i}]' for i in range(28, 32)]

    metal = 'm3'
    width = 1
    depth = 3
    fp.place_pins(pins_w, 'w', width, depth, metal)
    fp.place_pins(pins_n, 'n', width, depth, metal)
    fp.place_pins(pins_e, 'e', width, depth, metal)
    fp.place_pins(pins_s, 's', width, depth, metal)

    return fp