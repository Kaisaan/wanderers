.org 0x1b0220
lui a0, hi(credits_script)

.org 0x1b022c
addiu a0, a0, lo(credits_script)

.org 0x1b0758
li v0, credits_still_image_id_table
sll v1, s1, 0x1
addu v0, v0, v1

.org 0x1b0800
li v0, credits_movie_path_table
sll v1, s1, 0x2
addu v0, v0, v1
