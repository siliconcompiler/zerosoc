SV_SOURCES :=

SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_assert.sv

SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_secded_pkg.sv
SV_SOURCES += hw/opentitan/hw/top_earlgrey/rtl/top_pkg.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_pkg.sv
SV_SOURCES += hw/xbar_pkg.sv

SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_adapter_sram.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_err.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_rsp_intg_gen.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_fifo_sync.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_adapter_host.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_rsp_intg_chk.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_cmd_intg_gen.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_cmd_intg_chk.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_adapter_reg.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_socket_m1.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_socket_1n.sv
SV_SOURCES += hw/opentitan/hw/ip/tlul/rtl/tlul_err_resp.sv

SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_pkg.sv
SV_SOURCES += hw/opentitan/hw/ip/rv_core_ibex/rtl/rv_core_ibex.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_top.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_alu.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_compressed_decoder.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_csr.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_controller.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_counter.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_cs_registers.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_decoder.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_ex_block.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_fetch_fifo.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_id_stage.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_if_stage.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_load_store_unit.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_multdiv_fast.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_prefetch_buffer.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_pmp.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_register_file_ff.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_core.sv
SV_SOURCES += hw/opentitan/hw/vendor/lowrisc_ibex/rtl/ibex_wb_stage.sv

SV_SOURCES += hw/opentitan/hw/ip/uart/rtl/uart_reg_pkg.sv
SV_SOURCES += hw/opentitan/hw/ip/uart/rtl/uart_reg_top.sv
SV_SOURCES += hw/opentitan/hw/ip/uart/rtl/uart_rx.sv
SV_SOURCES += hw/opentitan/hw/ip/uart/rtl/uart_tx.sv
SV_SOURCES += hw/opentitan/hw/ip/uart/rtl/uart_core.sv
SV_SOURCES += hw/opentitan/hw/ip/uart/rtl/uart.sv

SV_SOURCES += hw/opentitan/hw/ip/gpio/rtl/gpio_reg_pkg.sv
SV_SOURCES += hw/opentitan/hw/ip/gpio/rtl/gpio_reg_top.sv
SV_SOURCES += hw/opentitan/hw/ip/gpio/rtl/gpio.sv

SV_SOURCES += hw/opentitan/hw/ip/lc_ctrl/rtl/lc_ctrl_pkg.sv
SV_SOURCES += hw/opentitan/hw/ip/lc_ctrl/rtl/lc_ctrl_state_pkg.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_util_pkg.sv
SV_SOURCES += hw/prim/prim_pkg.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_esc_pkg.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_ram_1p_pkg.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_subreg_arb.sv

SV_SOURCES += hw/prim/prim_ram_1p.sv
SV_SOURCES += hw/prim/prim_flop_2sync.sv
SV_SOURCES += hw/prim/prim_buf.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_fifo_sync.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_secded_64_57_enc.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_secded_64_57_dec.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_lc_sync.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_esc_receiver.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_diff_decode.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_intr_hw.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_subreg.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_subreg_ext.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_filter_ctr.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_arbiter_ppc.sv
SV_SOURCES += hw/opentitan/hw/ip/prim/rtl/prim_ram_1p_adv.sv
SV_SOURCES += hw/prim/prim_flop.sv
SV_SOURCES += hw/prim/prim_clock_gating.sv
SV_SOURCES += hw/opentitan/hw/ip/prim_generic/rtl/prim_generic_flop_2sync.sv
SV_SOURCES += hw/opentitan/hw/ip/prim_generic/rtl/prim_generic_clock_gating.sv
SV_SOURCES += hw/opentitan/hw/ip/prim_generic/rtl/prim_generic_ram_1p.sv
SV_SOURCES += hw/opentitan/hw/ip/prim_generic/rtl/prim_generic_buf.sv
SV_SOURCES += hw/opentitan/hw/ip/prim_generic/rtl/prim_generic_flop.sv

SV_SOURCES += hw/tl_dbg.sv
SV_SOURCES += hw/xbar.sv
SV_SOURCES += hw/top.sv

.PHONY: all
all: soc.v
	yosys -p 'read_verilog -sv soc.v; hierarchy -check'

.PHONY: clean
clean: soc.v

soc.v: $(SV_SOURCES)
	sv2v -I=hw/opentitan/hw/ip/prim/rtl/ -I=hw/opentitan/hw/dv/sv/dv_utils/ -DSYNTHESIS $^ > $@

# Simulation

ROM_DEPTH := 2048
ifndef PREFIX
PREFIX := $(shell if riscv64-unknown-elf-objdump -i 2>&1 | grep 'elf64-big' >/dev/null 2>&1; \
	then echo 'riscv64-unknown-elf-'; \
	elif riscv64-linux-gnu-objdump -i 2>&1 | grep 'elf64-big' >/dev/null 2>&1; \
	then echo 'riscv64-linux-gnu-'; \
	else echo "***" 1>&2; \
	echo "*** Error: Couldn't find an riscv64 version of GCC/binutils." 1>&2; \
	echo "*** To turn off this error, run 'make PREFIX= ...'." 1>&2; \
	echo "***" 1>&2; exit 1; fi)
endif

CC := $(PREFIX)gcc
AS := $(PREFIX)as
LD := $(PREFIX)ld
OBJCOPY := $(PREFIX)objcopy
OBJDUMP := $(PREFIX)objdump

CFLAGS := -O2 -march=rv32i -mabi=ilp32 -fdata-sections -ffunction-sections -ffreestanding
ASFLAGS := -march=rv32im -mabi=ilp32
OBJDUMPFLAGS := --disassemble-all --source --section-headers --demangle
LDFLAGS := -melf32lriscv -nostdlib
BIN2COEFLAGS := --width 32 --depth $(ROM_DEPTH) --fill 0

%.bin: %.elf
	$(OBJCOPY) $< -O binary $@

%.o: %.s
	$(AS) $(ASFLAGS) -c $< -o $@

%.lst: %.elf
	$(OBJDUMP) $(OBJDUMPFLAGS) $< > $@

%.elf: sw/rom.ld %.o
	@mkdir -p fw
	$(LD) $(LDFLAGS) -T $^ -o $@

%.mem: %.bin
	bin2coe $(BIN2COEFLAGS) --mem -i $< -o $@

sim/soc_tb.out: sim/soc_tb.v soc.v
	iverilog -g2005-sv -v -o $@ $^