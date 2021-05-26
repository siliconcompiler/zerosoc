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

PERIPHERALS := gpio

REGS_HDRS := $(patsubst %,gen/%_regs.h, $(PERIPHERALS))

DIF_SRCS := $(patsubst %,../hw/opentitan/sw/device/lib/dif/dif_%.c, $(PERIPHERALS))
DIF_HEADERS := $(DIF_SRCS:.c=.h)
DIF_OBJS := $(DIF_SRCS:.c=.o)

CC := $(PREFIX)gcc
AS := $(PREFIX)as
LD := $(PREFIX)ld
OBJCOPY := $(PREFIX)objcopy
OBJDUMP := $(PREFIX)objdump

CFLAGS := -O2 -march=rv32i -mabi=ilp32 -fdata-sections -ffunction-sections -ffreestanding -I../hw/opentitan/ -Igen/
ASFLAGS := -march=rv32im -mabi=ilp32
OBJDUMPFLAGS := --disassemble-all --source --section-headers --demangle
LDFLAGS := -melf32lriscv -nostdlib
BIN2COEFLAGS := --width 32 --depth $(ROM_DEPTH) --fill 0

gen/%_regs.h:
	@mkdir -p gen/
	../hw/opentitan/util/regtool.py -D -o $@ ../hw/opentitan/hw/ip/$*/data/$*.hjson

%.bin: %.elf
	$(OBJCOPY) $< -O binary $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.s
	$(AS) $(ASFLAGS) -c $< -o $@

%.lst: %.elf
	$(OBJDUMP) $(OBJDUMPFLAGS) $< > $@

.SECONDARY:
%.elf: rom.ld %.o $(DIF_OBJS) entry.o
	@mkdir -p fw
	$(LD) $(LDFLAGS) -T $^ -o $@

%.mem: %.bin
	bin2coe $(BIN2COEFLAGS) --mem -i $< -o $@
