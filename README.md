# Ys III: Wanderers From Ys (PS2) English Translation [SLPM-62532]
Repo for translating Ys III: Wanderers From Ys on PS2

# Notes
- Game uses the same graphics format as Lost Kefin (NAXA5010 header)
- Some graphics have a GBXA2000 header which is just like the other format without any of the frame info (so single, static images)
- Uses the same kscript format as Lost Kefin except pointer space is 0x800 bytes large
- Shift-JIS values seem to be XOR encrypted? (look at function at 00174A8C)
- DATA.BIN can be extract the same way as Lost Kefin

# Credits
- Everdred for figuring out the kscript format and making many scripts with Lost Kefin that can be reused for this one
