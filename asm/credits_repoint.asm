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
