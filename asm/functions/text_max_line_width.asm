text_max_line_width:
    daddu t2,zero,zero
    daddu v0,zero,zero
    addiu v1,zero,0xA
    addiu t0,zero,0xFF
    addiu a1,zero,0xFC
    addiu a3,zero,0xFD
@loop:
    lbu t1,0x0(a0)
    bne t1,zero,@check_ff_fd
    nop
    addiu v1,t2,0x1
    slt at,v0,v1
    beq at,zero,@end
    nop
    beq zero,zero,@end
    daddu v0,v1,zero
@check_ff_fd:
    bne t1,t0,@check_ff_fc
    nop
    lbu a2,0x1(a0)
    bne a2,a3,@check_ff_fc
    nop
    beq zero,zero,@loop
    addiu a0,a0,0x3
@check_ff_fc:
    bne t1,t0,@check_newline
    nop
    lbu a2,0x1(a0)
    bne a2,a1,@check_newline
    nop
    beq zero,zero,@loop
    addiu a0,a0,0x3
@check_newline:
    bne t1,v1,@update_width
    nop
    daddu t2,zero,zero
    beq zero,zero,@loop
    addiu a0,a0,0x1
@update_width:
    addiu t2,t2,0x1
    slt at,v0,t2
    beq at,zero,@check_ascii
    nop
    daddu v0,t2,zero
@check_ascii:
    slti at,t1,0x81
    beq at,zero,@advance_2
    nop
    beq zero,zero,@loop
    addiu a0,a0,0x1
@advance_2:
    beq zero,zero,@loop
    addiu a0,a0,0x2
@end:
    jr ra
    nop
