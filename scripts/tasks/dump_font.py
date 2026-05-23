# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pillow",
# ]
# ///
"""
Dump every glyph in the in-SLPM font to a separate PNG under font/.

Reads the 16-color RGBA CLUT and each 24x24 4bpp glyph from SLPM_625.32
(offsets matching patch_font.py) and writes font/<i>.png.

The character table is dumped separately by dump_font_table.py.
"""

from pathlib import Path
from struct import pack
import sys

from PIL import Image


WIDTH = 24
HEIGHT = 24
PIXEL_OFFSET = 0xD7EF0
CLUT_OFFSET = 0x144770
GLYPH_COUNT = 1160

CLUT_SIZE = 16 * 4
BYTES_PER_GLYPH = WIDTH * HEIGHT // 2


def dump_font(slpm_path: str, out_dir: str):
    slpm_path = Path(slpm_path)
    out_dir = Path(out_dir)

    if not slpm_path.exists():
        sys.exit(f"Error: {slpm_path} not found")

    out_dir.mkdir(parents=True, exist_ok=True)

    with open(slpm_path, "rb") as slpm:
        slpm.seek(CLUT_OFFSET)
        clut = slpm.read(CLUT_SIZE)

        slpm.seek(PIXEL_OFFSET)
        for i in range(GLYPH_COUNT):
            char_data = slpm.read(BYTES_PER_GLYPH)

            img_data = b""
            for byte in char_data:
                img_data += pack("BB", byte & 0xF, byte >> 4)

            image = Image.frombytes("P", (WIDTH, HEIGHT), img_data)
            image.putpalette(clut, rawmode="RGBA")
            image.save(out_dir / f"{i}.png")

    print(f"Dumped {GLYPH_COUNT} glyphs to {out_dir}/")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        dump_font("extracted/SLPM_625.32", "font")
    elif len(sys.argv) == 2:
        dump_font(sys.argv[1], "font")
    elif len(sys.argv) == 3:
        dump_font(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python dump_font.py [slpm_path] [out_dir]")
        sys.exit(1)
