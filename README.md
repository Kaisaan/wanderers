# Ys III: Wanderers From Ys (PS2) English Translation [SLPM-62532]
Repo for translating Ys III: Wanderers From Ys on PS2

# Overview
If you want updates be sure to [join the Discord server!](https://discord.gg/JnqvyDryen)  
[Link to translation spreadsheets](https://docs.google.com/spreadsheets/d/10h_j4RCCrUQtMjdgoMcrJcWS6CIDrvKm5Dv0k0JE2iY/edit?usp=sharing)

# Maps and Manual
There does not seem to be any scans of the game's manual available online.  
There are maps made by wagamamalullaby that are available to view [in this repo](https://github.com/Kaisaan/wanderers/tree/main/maps).

# Hacking Notes
- Game uses the same graphics format as Lost Kefin (NAXA5010 header)
- Some graphics have a GBXA2000 header (See [GraphicsFormat.md](https://github.com/Kaisaan/wanderers/blob/main/GraphicsFormat.md))
- Uses the same script container format as Lost Kefin except pointer space is 0x800 bytes large. Uses different opcodes.
- Text is Shift-JIS encoded with the data being bit-flipped
- DATA.BIN can be extracted the same way as Lost Kefin

# Contributors
- Kaisaan: Project Lead, Programming, Hacking, Testing
- Everdred: Programming, Hacking, Script development, made the VWF code, added in custom credits for the fan translation, helping with many technical issues
- JosepMC: Translation
- Etokapa: Editing the graphics and opening video, testing
- wagamamalullaby: Testing, testing on real hardware, making a proper guide and maps for the game
- Jazzysan: Testing, speedrunning this game
- DRAGONBLEAPIECE: Testing

# Related Materials
- Cheatcodes by [luc-ita](https://gamehacking.org/game/100381), and [TAK](https://www.ngemu.com/posts/1228814/)
- Guide by [Maturikasann's](http://maturikasann.web.fc2.com/ys/3_ps2.html)<sup>JP</sup>

# Special Thanks
- Everyone that supported and helped with *Lost Kefin*'s translation
- All supporters

