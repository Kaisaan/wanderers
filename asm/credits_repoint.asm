// Point credits() at our relocated script in the codecave.
//
// play_ending_sequence builds the script address in a0 across two
// NON-contiguous instructions (a `li v0,1` / `lui at,0x82` sit between them and
// are consumed by the jal's delay-slot store), so we patch the two halves in
// place rather than emitting a `la`:
//
//   1b0220: lui   a0,0x23        -> lui   a0, hi(credits_script)
//   1b0224: li    v0,0x1            (untouched -- needed by the delay slot)
//   1b0228: lui   at,0x82          (untouched)
//   1b022c: addiu a0,a0,0x5490   -> addiu a0, a0, lo(credits_script)
//   1b0230: jal   credits
//   1b0234: sw    v0,-0x4020(at)   (delay slot)
//
// `credits_script` is defined in asm/credits.asm (included by asm/codecave.asm),
// resolved in the same armips pass.
.org 0x1b0220
lui a0, hi(credits_script)

.org 0x1b022c
addiu a0, a0, lo(credits_script)

// credits() keeps the movie path table and still-image archive ID table in
// separate globals. Repoint both table bases to the codecave copies so added
// movie command indices can resolve past the original tables.
//
//   1b0758: lui   v0,0x24        -> li    v0, credits_still_image_id_table
//   1b075c: sll   v1,s1,0x1         (moved down after the li macro)
//   1b0760: addiu v0,v0,0x3bf0
//   1b0764: addu  v0,v0,v1
.org 0x1b0758
li v0, credits_still_image_id_table
sll v1, s1, 0x1
addu v0, v0, v1

//   1b0800: lui   v0,0x24        -> li    v0, credits_movie_path_table
//   1b0804: sll   v1,s1,0x2         (moved down after the li macro)
//   1b0808: addiu v0,v0,0x3bc0
//   1b080c: addu  v0,v0,v1
.org 0x1b0800
li v0, credits_movie_path_table
sll v1, s1, 0x2
addu v0, v0, v1
