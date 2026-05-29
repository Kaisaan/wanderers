# Ys III: Wanderers From Ys (PS2) English Translation [SLPM-62532]
Repo for translating Ys III: Wanderers From Ys on PS2

# Overview
If you want updates be sure to [join the Discord server](https://discord.gg/JnqvyDryen)  
[Link to translation spreadsheets](https://docs.google.com/spreadsheets/d/10h_j4RCCrUQtMjdgoMcrJcWS6CIDrvKm5Dv0k0JE2iY/edit?usp=sharing)

# Hacking Notes
- Game uses the same graphics format as Lost Kefin (NAXA5010 header)
- Some graphics have a GBXA2000 header which is just like the other format without any of the frame info (so single, static images)
- Uses the same script container format as Lost Kefin except pointer space is 0x800 bytes large. Uses different opcodes.
- Shift-JIS values seem to be XOR encrypted? (look at function at 00174A8C)
- DATA.BIN can be extract the same way as Lost Kefin

# Contributors
- Everdred - Work on the Variable Width Font (VWF), lots of script work (a lot from the work on *Lost Kefin*), cheatcode development
- Josep - Translation Work
- Etokapa - Graphics Editing

# Special Thanks
- Everyone that supported and helped with *Lost Kefin*'s translation

