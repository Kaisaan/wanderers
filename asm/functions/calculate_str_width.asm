calculate_str_width:
    daddu v0,zero,zero
    addiu t0,zero,0xFF
    addiu t1,zero,0xFC
    addiu t2,zero,0xFD
    addiu t3,zero,0xA
@loop:
    lbu t4,0x0(a0)
    beq t4,zero,@end
    nop
    bne t4,t3,@check_ff
    nop
    beq zero,zero,@loop
    addiu a0,a0,0x1
@check_ff:
    bne t4,t0,@check_ascii
    nop
    lbu t5,0x1(a0)
    bne t5,t1,@check_ff_fd
    nop
    beq zero,zero,@loop
    addiu a0,a0,0x3
@check_ff_fd:
    bne t5,t2,@check_ascii
    nop
    beq zero,zero,@loop
    addiu a0,a0,0x3
@check_ascii:
    slti at,t4,0x81
    beq at,zero,@handle_multibyte
    nop
    // 0x20 -> 0x8 to match the patched 0x10f7c4 space dispatcher.
    addiu at,zero,0x20
    beq t4,at,@space_case
    nop
    li t6,kerning_table
    addu t6,t6,t4
    lbu t7,0x0(t6)
    addu v0,v0,t7
    beq zero,zero,@loop
    addiu a0,a0,0x1
@space_case:
    addiu v0,v0,0x8
    beq zero,zero,@loop
    addiu a0,a0,0x1
@handle_multibyte:
    // Multi-byte: +0x14 to match BuildTextCommandList (0x10f7f4 / 0x10ff80).
    addiu v0,v0,0x14
    beq zero,zero,@loop
    addiu a0,a0,0x2
@end:
    jr ra
    nop
