.erroronwarning on
.ps2

.open "translated/SLPM_625.32", 0xfff80

.include "asm/text_last_line_width.asm"
.include "asm/text_line_count.asm"
.include "asm/text_max_line_width.asm"

.close
