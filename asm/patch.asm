.erroronwarning on
.ps2

.open "translated/SLPM_625.32", 0xfff80

.include "asm/kerning.asm"
.include "asm/pointers.asm"
.include "asm/credits_repoint.asm"
.include "asm/play_ending_sequence_repoint.asm"
.include "asm/equip_menu_layout.asm"

// Fix buffer size calculator to
// round up when calculating quadwords

.org 0x1179C0
mult v0,a3,a1
addiu v0,v0,0x1f 
jr ra
sra v0,v0,0x05
default_case:
jr ra
daddu v0,zero,zero

.org 0x117964
beq v0,zero,default_case

.close

// New code, tables, etc go here
.include "asm/codecave.asm"
