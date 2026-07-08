// Variable-width font / kerning patches.
// Codecave helpers live in asm/codecave.asm.

.org 0x1743d0
.include "asm/functions/text_last_line_width.asm"

.org 0x174340
.include "asm/functions/text_line_count.asm"

.org 0x174280
.include "asm/functions/text_max_line_width.asm"

////
// TextBubble
////
// Rewire call sites from char-count helpers to pixel-width helpers.
.org 0x174b9c
jal text_last_line_pixel_width

.org 0x174bb0
jal text_max_line_pixel_width

.org 0x174c68
jal text_last_line_pixel_width

// Drop iMaxLineCh * 0x14: result is already in pixels. Pad by 0x20 so the
// pagewait book glyph fits past the last line without overflowing the bubble.
.org 0x174bb8
nop
.org 0x174bc0
nop
.org 0x174bc8
addiu s1,v0,0x20

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

// Speed up TextBubble typewriter delay from 6 frames per glyph to 4.
.org 0x174b70
li a3,0x4

.org 0x174d58
li a3,0x4

// CutsceneText typewriter
.org 0x175134
li a3,0x4

// Shift Speaker Names to the right
.org 0x0015F0EC
addiu a1,zero,0x70

////
// CutsceneText
////

// Bugfix: CutsceneText message length was treated as a signed
// int which meant any message longer than 128 bytes would 
// overflow and crash the game.
.org 0x174fa4
lbu s0,0x0(v0)

.org 0x174f94
li a2,0x100       // memcpy size

.org 0x174fb8
andi a2,s0,0xff   // memcpy size
.org 0x174fbc
nop                   

.org 0x174fc8
andi v0,s0,0xff   // XOR-decode loop count
.org 0x174fcc
nop                   


// Same deal as TextBubble. Rewire call sites from char-count helpers to
// pixel-width helpers, then drop the glyph-count * 0x14 conversions.
.org 0x17509c
jal text_max_line_pixel_width

.org 0x1750dc
jal text_last_line_pixel_width

.org 0x1750a4
nop
.org 0x1750ac
nop
.org 0x1750b4
move s1,v0

// Drop iLastLineW * 0x14: result is already in pixels. s1 now holds the last
// line width, used to place the continue arrow at iVar8 + s1.
.org 0x1750e4
nop
.org 0x1750ec
nop
.org 0x1750f4
move s1,v0

// Shift book
.org 0x1751d0
addiu a2,v0,0x5

.org 0x1751cc
addiu a3,s0,0x26

// Make the text box wider
.org 0x1750e8
addiu a2,s1,0x30

// Recenter the box by shifting it left 16px
.org 0x1750d4
li v0,0x130



////
// TutorialControls
////

// Same deal as TextBubble. Rewire call sites from char-count helpers to
// pixel-width helpers, then drop the glyph-count * 0x14 conversions.
.org 0x1744a0
jal text_max_line_pixel_width

.org 0x1744ac
move s1,v0
.org 0x1744b0
nop
.org 0x1744b8
nop


////
// Shop
////

.org 0x17de98
addiu v0, zero, 0x0
addiu a2,zero,0x106
nop
nop
nop
addiu v0,v0,0x116



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

