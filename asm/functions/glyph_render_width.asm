// Pick the textbox renderer's per-glyph quad width: 0x18 for ASCII
// (BuildTextCommandList tags ASCII as (ch<<8)|0x20), else 0x14.
compute_glyph_render_width:
    addu  t0,a1,s0                // &cmd
    lhu   t0,0x4(t0)              // cmd.slot
    sll   t0,t0,0x2               // * sizeof(FontCacheSlot)
    lw    a3,-0x7d3c(gp)          // g_pFontCacheTable
    addu  t0,t0,a3
    lbu   t0,0x2(t0)              // low byte of wUsCharcode
    li    a3,0x14
    addiu t0,t0,-0x20             // 0 iff ASCII
    bne   t0,zero,@ret
    nop
    li    a3,0x18
@ret:
    j     0x00110280              // back to insn after trampoline's delay slot
    nop
