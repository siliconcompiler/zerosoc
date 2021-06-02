/*
 * ZeroSoC linker script
 *
 * Roughly based on OpenTitan's boot ROM linker script, with modifications for
 * our purposes.
 * https://github.com/lowRISC/opentitan/blob/master/sw/device/boot_rom/rom_link.ld
 */

/**
  * Link libgcc statically into address space
  */
GROUP(-lgcc)

/**
 * Indicate that there are no dynamic libraries, whatsoever.
 */
__DYNAMIC = 0;

_ram_size = 8k;

/**
 * Fixed-size stack at end of RAM
 */
_stack_size = 200;
_stack_end = _ram_size;
_stack_start = _stack_end - _stack_size;

MEMORY {
    ram (rwx): ORIGIN = 0, LENGTH = _ram_size - _stack_size
    ram_stack (rw): ORIGIN = _ram_size - _stack_size, LENGTH = _stack_size
}

SECTIONS {
  /**
   * Standard text section, containing program code.
   */
  .text : ALIGN(4) {
    *(.text)
    *(.text.*)
  } > ram

  /**
   * Read-only data section, containing all large compile-time constants, like
   * strings.
   */
  .rodata : ALIGN(4) {
    /* Small read-only data comes before regular read-only data for the same
     * reasons as in the data section */
    *(.srodata)
    *(.srodata.*)
    *(.rodata)
    *(.rodata.*)
  } > ram

  /**
   * "Intitial data" section, the initial values of the mutable data section
   * initialized at runtime.
   */
  .idata : ALIGN(4) {
    _data_init_start = .;
  } > ram

  /**
   * Standard mutable data section.
   * TODO: this may need to be set up in code.
   */
  .data : ALIGN(4) {
    _data_start = .;
    __global_pointer$ = . + 2048;

    /* Small data should come before larger data. This helps to ensure small
     * globals are within 2048 bytes of the value of `gp`, making their accesses
     * hopefully only take one instruction. */
    *(.sdata)
    *(.sdata.*)

    /* Other data will likely need multiple instructions to load, so we're less
     * concerned about address materialisation taking more than one instruction.
     */
    *(.data)
    *(.data.*)
    . = ALIGN(4);
    _data_end = .;
  } > ram

  /**
   * Standard BSS section.
   * TODO: should this be zeroed in code?
   */
  .bss : ALIGN(4) {
    _bss_start = .;
    /* Small BSS comes before regular BSS for the same reasons as in the data
     * section */
    *(.sbss)
    *(.sbss.*)
    *(.bss)
    *(.bss.*)
    . = ALIGN(4);
    _bss_end = .;
  } > ram

  /* Discarded Sections (Not needed in device images). */
  /DISCARD/ : {
    /* We don't keep unwind information */
    *(.eh_frame)
    *(.eh_frame_hdr)

    /* Compiler Information */
    *(.comment)
    *(.comment.*)

    /* Other Notes */
    *(.note)
    *(.note.*)

    /* Relocations */
    *(.rela.*)
    *(.rela.dyn)

    /* STAB Debugging Info */
    *(.stab)
    *(.stab.*)
    *(.stabstr)

    /* Debug info */
    *(.debug_info)
    *(.debug_abbrev)
    *(.debug_aranges)
    *(.debug_line)
    *(.debug_loc)
    *(.debug_ranges)
    *(.debug_str)
    *(.debug_frame)

    /* COMMON Sections */
    *(COMMON)
  }
}
