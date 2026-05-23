text_last_line_pixel_width:
    daddu t8,a0,zero
    addiu t0,zero,0xFF
    addiu t1,zero,0xFC
    addiu t2,zero,0xFD
    addiu t3,zero,0xA
@loop:
    lbu t4,0x0(a0)
    beq t4,zero,@done
    nop
    bne t4,t0,@check_newline
    nop
    lbu t5,0x1(a0)
    bne t5,t2,@check_ff_fc
    nop
    beq zero,zero,@loop
    addiu a0,a0,0x3
@check_ff_fc:
    bne t5,t1,@check_newline
    nop
    beq zero,zero,@loop
    addiu a0,a0,0x3
@check_newline:
    bne t4,t3,@check_ascii
    nop
    addiu a0,a0,0x1
    beq zero,zero,@loop
    daddu t8,a0,zero
@check_ascii:
    slti at,t4,0x81
    beq at,zero,@advance_2
    nop
    beq zero,zero,@loop
    addiu a0,a0,0x1
@advance_2:
    beq zero,zero,@loop
    addiu a0,a0,0x2
@done:
    daddu a0,t8,zero
    j calculate_str_width
    nop
