.org 0x1743d0
text_last_line_width:
    daddu v0,zero,zero
    addiu v1,zero,0xA
    addiu t0,zero,0xFF
    addiu a1,zero,0xFC
    addiu a3,zero,0xFD
@loop:
    lbu t1,0x0(a0)
    beq t1,zero,@end
    nop
    bne t1,t0,@check_ff_fc
    nop
    lbu a2,0x1(a0)
    bne a2,a3,@check_ff_fc
    nop
    beq zero,zero,@loop
    addiu a0,a0,0x3
@check_ff_fc:
    bne t1,t0,@check_ascii
    nop
    lbu a2,0x1(a0)
    bne a2,a1,@check_ascii
    nop
    beq zero,zero,@loop
    addiu a0,a0,0x3
@check_ascii:
    slti at,t1,0x81
    bne t1,v1,@increment_v0
    nop
    daddu v0,zero,zero
    beq zero,zero,@loop
    addiu a0,a0,0x1
@increment_v0:
    beq at,zero,@advance_2
    addiu v0,v0,0x1
    beq zero,zero,@loop
    addiu a0,a0,0x1
@advance_2:
    beq zero,zero,@loop
    addiu a0,a0,0x2
@end:
    jr ra
    nop
