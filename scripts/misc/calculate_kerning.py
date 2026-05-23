# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "fonttools",
# ]
# ///

"""Calculate average kerning for each character in a TTF font."""

import argparse
import csv
from fontTools.ttLib import TTFont

# Character set to analyze (from original kerning.csv)
CHARACTERS = [
    '!', '!', '"', "&", "'", '(', ')', '*', '+', ',', '-', '.', '/',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ':', ';', '?',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '[', ']', 
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '~'
]


def get_kerning_value(font: TTFont, glyph1: str, glyph2: str) -> int:
    """Get kerning value between two glyphs from GPOS or kern table."""
    # Try GPOS table first (more modern)
    if "GPOS" in font:
        gpos = font["GPOS"]
        for lookup in gpos.table.LookupList.Lookup:
            for subtable in lookup.SubTable:
                if hasattr(subtable, "ExtractKerning"):
                    kern = subtable.ExtractKerning(glyph1, glyph2)
                    if kern:
                        return kern
                # PairPos format
                if hasattr(subtable, "Coverage") and hasattr(subtable, "PairSet"):
                    try:
                        if glyph1 in subtable.Coverage.glyphs:
                            idx = subtable.Coverage.glyphs.index(glyph1)
                            pair_set = subtable.PairSet[idx]
                            for pair in pair_set.PairValueRecord:
                                if pair.SecondGlyph == glyph2:
                                    if hasattr(pair.Value1, "XAdvance"):
                                        return pair.Value1.XAdvance
                    except (AttributeError, IndexError, KeyError):
                        pass

    # Fall back to kern table (older format)
    if "kern" in font:
        kern_table = font["kern"]
        for table in kern_table.kernTables:
            if hasattr(table, "kernTable"):
                key = (glyph1, glyph2)
                if key in table.kernTable:
                    return table.kernTable[key]

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Calculate average kerning for each character in a TTF font."
    )
    parser.add_argument("font", help="Path to the TTF font file")
    parser.add_argument(
        "-o", "--output",
        default="kerning_output.csv",
        help="Output CSV file path (default: kerning_output.csv)"
    )
    parser.add_argument(
        "-s", "--shift",
        type=int,
        default=-1,
        help="Shift all output values by this amount (default: -1)"
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=21,
        help="Font size in pixels (default: 21)"
    )
    args = parser.parse_args()

    # Load font
    font = TTFont(args.font)

    # Get units per em for scaling
    units_per_em = font["head"].unitsPerEm
    scale = args.font_size / units_per_em

    # Get cmap to convert characters to glyph names
    cmap = font.getBestCmap()

    # Get advance widths from hmtx table
    hmtx = font["hmtx"]

    results = []

    for idx, char in enumerate(CHARACTERS):
        code_point = ord(char)
        if code_point not in cmap:
            print(f"Warning: '{char}' not in font cmap")
            continue

        glyph_name = cmap[code_point]
        base_advance = hmtx[glyph_name][0]  # (advance, lsb)

        # Calculate average advance across all following characters
        total_advance = 0
        count = 0

        for next_char in CHARACTERS:
            next_code = ord(next_char)
            if next_code not in cmap:
                continue

            next_glyph = cmap[next_code]
            kern = get_kerning_value(font, glyph_name, next_glyph)
            advance = base_advance + kern
            total_advance += advance
            count += 1

        if count > 0:
            avg_advance_units = total_advance / count
            avg_advance_px = avg_advance_units * scale
            avg_advance_rounded = round(avg_advance_px + args.shift)
        else:
            avg_advance_rounded = round((base_advance * scale) + args.shift)

        results.append((idx, char, avg_advance_rounded))

    # Write output CSV
    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "char", "width"])
        for idx, char, width in results:
            writer.writerow([idx, char, width])

    print(f"Output written to {args.output}")

    font.close()


if __name__ == "__main__":
    main()
