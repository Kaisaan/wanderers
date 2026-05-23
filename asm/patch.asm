.erroronwarning on
.ps2

.open "translated/SLPM_625.32", 0xfff80

.include "asm/kerning.asm"

.close

// New code, tables, etc go here
.include "asm/codecave.asm"
