.ps2

.create "scripts/data/codecave.bin", 0x1f00000

kerning_table:
  .incbin "scripts/data/kerning.bin"

.include "asm/functions/calculate_str_width.asm"
.include "asm/functions/text_last_line_pixel_width.asm"
.include "asm/functions/text_max_line_pixel_width.asm"
.include "asm/functions/glyph_render_width.asm"

.close
