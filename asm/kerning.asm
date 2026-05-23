// Variable-width font / kerning patches.
// Codecave helpers live in asm/codecave.asm.

.org 0x1743d0
.include "asm/functions/text_last_line_width.asm"

.org 0x174340
.include "asm/functions/text_line_count.asm"

.org 0x174280
.include "asm/functions/text_max_line_width.asm"

// Rewire call sites from char-count helpers to pixel-width helpers.
.org 0x174b9c
jal text_last_line_pixel_width

.org 0x174bb0
jal text_max_line_pixel_width

.org 0x174c68
jal text_last_line_pixel_width

// Drop iMaxLineCh * 0x14: result is already in pixels.
.org 0x174bb8
nop
.org 0x174bc0
nop
.org 0x174bc8
move s1,v0

// Drop iLastLineW * 0x14; result is already in pixels.
.org 0x174e14
nop
.org 0x174e1c
nop
.org 0x174e20
move v0,s5

// Shift book
.org 0x174e34
addiu a2,v0,0x0

// For spaces only advance 8px instead of previous 10
.org 0x0010f7c4
addiu a0,s3,0x8

// VWF: If glyph is ASCII, look up its width
.org 0x0010ff60
bne   s5,a2,0x0010ff80
sb    a0,0x6(a1)
lbu   t0,0x0(s1)
lui   t1,hi(kerning_table)
addu  t1,t1,t0
lbu   t0,lo(kerning_table)(t1)
b     0x0010ff90
addu  s3,s3,t0

.org 0x0010ff80
beq   s8,a2,0x0010ff90
addiu s3,s3,0xa
b     0x0010ff90
addiu s3,s3,0xa

// Render ASCII glyphs at full 24px width instead of squishing into 20.
// Delay slot at 0x0011027c (`li a2,0x1`) is preserved.
.org 0x00110278
j     compute_glyph_render_width
