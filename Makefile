FW ?= hello

.PHONY: all
all: zerosoc_hello.bit

.PHONY: clean
clean:
	rm -f *.asc *.bit zerosoc.vcd
	make -C sw/ clean

zerosoc_%.asc: build/top_icebreaker/job0/apr/0/outputs/top_icebreaker.asc sw/%.mem
	icebram -v random.mem sw/$*.mem < $< > $@

zerosoc_%.bit: zerosoc_%.asc
	icepack $< $@

sw/%.mem: sw/%.c
	make -C sw/ $*.mem

# Simulation

sim/soc_tb.out: sim/zerosoc_tb.v zerosoc.v sw/hello.mem
	iverilog -g2005-sv -v -o $@ $< zerosoc_sim.v