ROM_DEPTH := 2048

PREFIX := riscv32-unknown-elf-

PERIPHERALS := gpio uart

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
ASFLAGS := -march=rv32i -mabi=ilp32
OBJDUMPFLAGS := --disassemble-all --source --section-headers --demangle
LDFLAGS := -Wl,-melf32lriscv -nostdlib
BIN2COEFLAGS := --width 32 --depth $(ROM_DEPTH) --fill 0

all: hello.mem

lib/zerosoc.o: lib/zerosoc.h

gen/%_regs.h:
	@mkdir -p gen/
	../hw/opentitan/util/regtool.py -D -o $@ ../hw/opentitan/hw/ip/$*/data/$*.hjson

# Pattern variables don't work here for some reason
../hw/opentitan/sw/device/lib/dif/dif_gpio.o: gen/gpio_regs.h
../hw/opentitan/sw/device/lib/dif/dif_uart.o: gen/uart_regs.h

%.bin: %.elf
	$(OBJCOPY) $< -O binary $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.s
	$(AS) $(ASFLAGS) -c $< -o $@

%.lst: %.elf
	$(OBJDUMP) $(OBJDUMPFLAGS) $< > $@

.SECONDARY:
%.elf: ram.ld %.o entry.o lib/zerosoc.o $(DIF_OBJS)
	$(CC) $(LDFLAGS) -T $^ -o $@

%.mem: %.bin
	bin2coe $(BIN2COEFLAGS) --mem -i $< -o $@

.PHONY: clean
clean:
	rm -f *.o *.elf *.bin *.mem lib/*.o gen/*.h $(DIF_OBJS)
