MEMORY
{
    rom (rx): ORIGIN = 0x80, LENGTH = 8k
    ram (rw): ORIGIN = 0x1080, LENGTH = 16k
}

STACK_SIZE = 512;

SECTIONS
{
    . = 0x0;
    /* Fill with zeros to put entry point at boot vector
       source: https://stackoverflow.com/q/45348540
    */
    .fill : {
        FILL(0x0)
        . = 0x7C;      /* Note shorter to accommodate following LONG */
        LONG(0x0) /* Deliberately reversed to demonstrate the result */
    } > fill

    .text : { *(.text) } > rom
    .data : { *(.data) } > ram
    .bss : { *(.bss) } > ram
    .stack (NOLOAD) : {
        _stack_bottom = .;
        . = . + STACK_SIZE;
        _stack_start = .;
    } > ram
}


