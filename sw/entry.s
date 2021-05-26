.global _entry
_entry:
    # # set up scratch space for saving regs on exception handler
    # la x1, _mscratch
    # csrw mscratch, x1
    # # set up exception handler
    # la x1, _handler
    # csrw mtvec, x1

    # set stack pointer
    la sp, _stack_start

    # call main function
    call main

_hang:
    # hang forever
    jal x0, _hang
