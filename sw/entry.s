# Exception handler - for now, just loops forever.
.org 0x00
_exception_handler:
  j _exception_handler

# Main code entry point
.org 0x80
_entry:
    # TODO: should do more reset (set up exception-handling stuff, clear all regs)

    # Set up the global pointer. This requires that we disable linker relaxations
    # (or it will be relaxed to `mv gp, gp`).
    .option push
    .option norelax
    la  gp, __global_pointer$
    .option pop

    # set stack pointer
    la sp, _stack_end

    # call main function
    call main

_hang:
    # hang if main returns
    j _hang
