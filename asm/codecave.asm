.ps2
.loadtable "asm/wanderers.tbl", "UTF8"   // for the new credit lines in credits.asm

.create "scripts/data/codecave.bin", 0x1f00000

kerning_table:
  .incbin "scripts/data/kerning.bin"

.include "asm/functions/calculate_str_width.asm"
.include "asm/functions/text_last_line_pixel_width.asm"
.include "asm/functions/text_max_line_pixel_width.asm"
.include "asm/functions/glyph_render_width.asm"
.include "asm/play_ending_sequence.asm"

// Text for the added Triangle prompt on the ending screen.
ending_fan_tl_credits_prompt:
.str "#GR△#WH: Fan TL Credits"
.align 4

// credits() indexes these in parallel for each movie command. The original
// movie paths are still resident in SLPM_625.32; only the added path lives here.
credits_ys3ed12_movie_path:
.string "cdrom0:\\YS3ED12.PSS;1"
.align 4

credits_movie_path_table:
.dw 0x0025eca0  // cdrom0:\MOVIE\YS3ED00.PSS;1
.dw 0x0025ecc0  // cdrom0:\MOVIE\YS3ED01.PSS;1
.dw 0x0025ece0  // cdrom0:\MOVIE\YS3ED02.PSS;1
.dw 0x0025ed00  // cdrom0:\MOVIE\YS3ED03.PSS;1
.dw 0x0025ed20  // cdrom0:\MOVIE\YS3ED04.PSS;1
.dw 0x0025ed40  // cdrom0:\MOVIE\YS3ED05.PSS;1
.dw 0x0025ed60  // cdrom0:\MOVIE\YS3ED06.PSS;1
.dw 0x0025ed80  // cdrom0:\MOVIE\YS3ED07.PSS;1
.dw 0x0025eda0  // cdrom0:\MOVIE\YS3ED08.PSS;1
.dw 0x0025edc0  // cdrom0:\MOVIE\YS3ED09.PSS;1
.dw 0x0025ede0  // cdrom0:\MOVIE\YS3ED10.PSS;1
.dw 0x0025ee00  // cdrom0:\MOVIE\YS3ED11.PSS;1
.dw credits_ys3ed12_movie_path

credits_still_image_id_table:
.dh 0x7
.dh 0x8
.dh 0x9
.dh 0xa
.dh 0xb
.dh 0xc
.dh 0xd
.dh 0xe
.dh 0xf
.dh 0x10
.dh 0x11
.dh 0x12
.dh 0x6
.align 4

// Relocated credits script for the alternate credits path.
.include "asm/credits.asm"

.close
