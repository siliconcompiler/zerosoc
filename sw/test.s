.global _reset
.type _reset, %function
_reset:
addi x1, x1, 1
jal x0, _reset
