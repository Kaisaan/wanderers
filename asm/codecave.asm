.ps2

.open "scripts/data/codecave.bin", 0x1f00000


kerning_table:
  .incbin "scripts/data/kerning.bin"

.include "asm/calculate_str_width.asm"
.include "asm/text_last_line_pixel_width.asm"
.include "asm/text_max_line_pixel_width.asm"

.close
