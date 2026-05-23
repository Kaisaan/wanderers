.erroronwarning on
.ps2

.open "translated/SLPM_625.32", 0xfff80

.org 0x1743d0
.include "asm/text_last_line_width.asm"

.org 0x174340
.include "asm/text_line_count.asm"

.org 0x174280
.include "asm/text_max_line_width.asm"

// Patch calls to text_last_line_width and text_max_line_width
// They return # characters. We want # pixels.
.org 0x174b9c
jal text_last_line_pixel_width

.org 0x174bb0
jal text_max_line_pixel_width

.org 0x174c68
jal text_last_line_pixel_width

// Eliminate iMaxLineCh * 0x14: result already in pixels, just stash in s1.
.org 0x174bb8
nop
.org 0x174bc0
nop
.org 0x174bc8
move s1,v0

// Eliminate iLastLineW * 0x14: feed s5 straight into the widget_send_msg
// x-coord. The lw at 0x174e18 between these is unrelated and stays.
.org 0x174e14
nop
.org 0x174e1c
nop
.org 0x174e20
move v0,s5

// Shift book
.org 0x174e34
addiu a2,v0,0x0

// Narrower space: BuildTextCommandList 0x20 dispatcher advance 0xA -> 0x8.
.org 0x0010f7c4
addiu a0,s3,0x8

// Variable-width font: BuildTextCommandList per-glyph cursor advance.
// Half-width ASCII path now indexes kerning_table[s1[0]] instead
// of advancing sCursorX (s3) by a fixed 0xA. Highlighted multi-byte
// and full-width paths keep their original +0xA / +0x14 advance,
// implemented as two chained `addiu 0xa` so all paths fit in 12 slots.
// t0/t1 are scratch and aren't read by anything between 0x10ff90 and
// the next loop iteration.
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

.close

// New code, tables, etc go here
.include "asm/codecave.asm"
