"""
Dump the in-SLPM font character table to scripts/data/font_table.txt.

Reads 1160 two-byte entries from TABLE_OFFSET (matching patch_font.py),
decodes each as Shift-JIS / cp932, strips the 0x20 padding that the
engine uses for ASCII entries, and writes one character per line.
The output file is the input format expected by patch_font.py's
patch_table().
"""

import sys
from pathlib import Path


TABLE_OFFSET = 0xD75D0
GLYPH_COUNT = 1160


def dump_font_table(slpm_path: str, out_path: str):
    slpm_path = Path(slpm_path)
    out_path = Path(out_path)

    if not slpm_path.exists():
        sys.exit(f"Error: {slpm_path} not found")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    chars = []
    with open(slpm_path, "rb") as slpm:
        slpm.seek(TABLE_OFFSET)
        for _ in range(GLYPH_COUNT):
            raw = slpm.read(2)
            char = raw.decode(encoding="cp932", errors="backslashreplace").lstrip(" ")
            chars.append(char)

    with open(out_path, "w", encoding="cp932") as fp:
        for ch in chars:
            fp.write(ch + "\n")

    print(f"Dumped {len(chars)} entries to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        dump_font_table("extracted/SLPM_625.32", "scripts/data/font_table.txt")
    elif len(sys.argv) == 2:
        dump_font_table(sys.argv[1], "scripts/data/font_table.txt")
    elif len(sys.argv) == 3:
        dump_font_table(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python dump_font_table.py [slpm_path] [out_path]")
        sys.exit(1)
