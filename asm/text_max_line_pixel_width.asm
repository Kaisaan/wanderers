// Calculate the width of the largest line
text_max_line_pixel_width:
    addiu sp,sp,-0x20
    sd ra,0x0(sp)
    sd s0,0x8(sp)
    sd s1,0x10(sp)
    sd s2,0x18(sp)
    daddu s0,zero,zero          // max width
    daddu s1,a0,zero            // start of current line
    daddu s2,a0,zero            // scan cursor
@reload:
    addiu t0,zero,0xFF
    addiu t1,zero,0xFC
    addiu t2,zero,0xFD
    addiu t3,zero,0xA
@loop:
    lbu t4,0x0(s2)
    beq t4,zero,@end_of_string
    nop
    bne t4,t0,@check_newline
    nop
    lbu t5,0x1(s2)
    bne t5,t2,@check_ff_fc
    nop
    beq zero,zero,@loop
    addiu s2,s2,0x3
@check_ff_fc:
    bne t5,t1,@check_newline
    nop
    beq zero,zero,@loop
    addiu s2,s2,0x3
@check_newline:
    bne t4,t3,@check_ascii
    nop
    sb zero,0x0(s2)
    daddu a0,s1,zero
    jal calculate_str_width
    nop
    addiu t3,zero,0xA
    sb t3,0x0(s2)
    slt at,s0,v0
    beq at,zero,@past_nl
    nop
    daddu s0,v0,zero
@past_nl:
    addiu s2,s2,0x1
    beq zero,zero,@reload
    daddu s1,s2,zero
@check_ascii:
    slti at,t4,0x81
    beq at,zero,@advance_2
    nop
    beq zero,zero,@loop
    addiu s2,s2,0x1
@advance_2:
    beq zero,zero,@loop
    addiu s2,s2,0x2
@end_of_string:
    daddu a0,s1,zero
    jal calculate_str_width
    nop
    slt at,s0,v0
    beq at,zero,@done
    nop
    daddu s0,v0,zero
@done:
    daddu v0,s0,zero
    ld ra,0x0(sp)
    ld s0,0x8(sp)
    ld s1,0x10(sp)
    ld s2,0x18(sp)
    jr ra
    addiu sp,sp,0x20
