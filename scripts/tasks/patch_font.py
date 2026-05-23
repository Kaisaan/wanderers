from io import BufferedReader
import sys
from pathlib import Path
from PIL import Image


WIDTH = 24
HEIGHT = 24
PIXEL_OFFSET = 0xD7EF0
CLUT_OFFSET = 0x144770
GLYPH_COUNT = 1160
BYTES_PER_GLYPH = WIDTH * HEIGHT // 2
CLUT_SIZE = 16 * 4

TABLE_OFFSET = 0xD75D0


def patch_table(file: BufferedReader, glyph_count: int):
    file.seek(TABLE_OFFSET)
    table_f = open("scripts/data/font_table.txt", "r", encoding="cp932")
    for i, line in enumerate(table_f.readlines()):
        if i >= glyph_count:
            break

        b = line.rstrip("\n\r").encode("cp932")
        if len(b) == 1:
            b = b"\x20" + b

        file.write(b)


class Glyph:
    def __init__(self, palette: list[list[int]], pixels: list[int]):
        self.palette = palette
        self.pixels = pixels

    def rotate_column(self, amount: int):
        """
        Shift right by amount pixels. The rightmost column "rotates" to the leftmost column.
        """
        amount = amount % WIDTH
        if amount == 0:
            return

        new_pixels = []
        for row in range(HEIGHT):
            row_start = row * WIDTH
            row_pixels = self.pixels[row_start : row_start + WIDTH]
            rotated_row = row_pixels[-amount:] + row_pixels[:-amount]
            new_pixels.extend(rotated_row)

        self.pixels = new_pixels

    @classmethod
    def from_png(cls, image: Image.Image):
        if image.size != (WIDTH, HEIGHT):
            raise ValueError(f"Image size must be {WIDTH}x{HEIGHT}")

        rgb_palette = image.getpalette()
        transparency = image.info.get("transparency", b"")

        palette = []
        num_colors = 16
        for i in range(num_colors):
            color = []
            if i >= (len(rgb_palette) // 3):
                color.append(0)
                color.append(0)
                color.append(128)
                palette.append(color)
                continue

            color.append(rgb_palette[i * 3])
            color.append(rgb_palette[i * 3 + 1])
            color.append(rgb_palette[i * 3 + 2])

            if transparency == 0:
                alpha = 128
            else:
                if i < len(transparency):
                    alpha = int(transparency[i] // 1.5)
                else:
                    alpha = 128
            if alpha == 127 or alpha > 128:
                alpha = 128

            color.append(alpha)
            palette.append(color)

        return cls(palette, list(image.getdata()))

    def to_bytes(self) -> bytes:
        result = b""
        for i in range(0, len(self.pixels), 2):
            p1 = self.pixels[i]
            p2 = self.pixels[i + 1]
            result += int.to_bytes((p2 << 4) | (p1 & 0xF), 1)
        return result


def read_original_clut(original_slpm_path: Path) -> list[list[int]]:
    with open(original_slpm_path, "rb") as f:
        f.seek(CLUT_OFFSET)
        raw = f.read(CLUT_SIZE)
    return [list(raw[i * 4 : i * 4 + 4]) for i in range(16)]


def build_remap_lut(
    old_palette: list[list[int]], new_palette: list[list[int]]
) -> list[int]:
    transparent_new = next(
        (j for j, c in enumerate(new_palette) if c[3] == 0), None
    )
    lut = []
    for old in old_palette:
        if old[3] == 0 and transparent_new is not None:
            lut.append(transparent_new)
            continue
        best_idx = 0
        best_dist = None
        for j, new in enumerate(new_palette):
            d = sum((a - b) ** 2 for a, b in zip(old, new))
            if best_dist is None or d < best_dist:
                best_dist = d
                best_idx = j
        lut.append(best_idx)
    return lut


def remap_unpatched_glyphs(slpm, lut: list[int], start: int):
    if lut == list(range(16)):
        return 0
    count = GLYPH_COUNT - start
    slpm.seek(PIXEL_OFFSET + start * BYTES_PER_GLYPH)
    data = bytearray(slpm.read(count * BYTES_PER_GLYPH))
    for i, byte in enumerate(data):
        data[i] = (lut[byte >> 4] << 4) | lut[byte & 0xF]
    slpm.seek(PIXEL_OFFSET + start * BYTES_PER_GLYPH)
    slpm.write(bytes(data))
    return count


def patch_font_from_atlas(
    atlas_path: str,
    slpm_path: str = "translated/SLPM_625.32",
    original_slpm_path: str = "extracted/SLPM_625.32",
):
    """
    Patch the game font from a single atlas PNG file into the SLPM file.

    The atlas is a single column of WIDTHxHEIGHT glyphs stacked vertically.

    Args:
        atlas_path: Path to the atlas PNG file
        slpm_path: Path to the SLPM_625.32 file to patch
        original_slpm_path: Path to the untouched SLPM, used to read the
            original CLUT so unpatched glyphs can be remapped onto the new one.
    """
    atlas_path = Path(atlas_path)
    slpm_path = Path(slpm_path)
    original_slpm_path = Path(original_slpm_path)

    if not slpm_path.exists():
        sys.exit(f"Error: {slpm_path} not found")

    if not atlas_path.exists():
        sys.exit(f"Error: {atlas_path} not found")

    if not original_slpm_path.exists():
        sys.exit(f"Error: {original_slpm_path} not found")

    atlas = Image.open(atlas_path)

    # Validate atlas dimensions
    if atlas.width != WIDTH:
        sys.exit(f"Error: Atlas width must be {WIDTH}, got {atlas.width}")

    glyph_count = atlas.height // HEIGHT
    if atlas.height % HEIGHT != 0:
        sys.exit(
            f"Error: Atlas height must be a multiple of {HEIGHT}, got {atlas.height}"
        )

    print(f"Atlas contains {glyph_count} glyphs")

    original_clut = read_original_clut(original_slpm_path)
    new_palette = None
    prev_palette = None

    with open(slpm_path, "r+b") as slpm:
        patch_table(slpm, glyph_count=glyph_count)
        for i in range(glyph_count):
            # Crop the glyph from the atlas
            top = i * HEIGHT
            bottom = top + HEIGHT
            glyph_image = atlas.crop((0, top, WIDTH, bottom))

            glyph = Glyph.from_png(glyph_image)

            if prev_palette is not None and prev_palette != glyph.palette:
                print(f"Previous palette: {prev_palette}")
                print(f"Current palette: {glyph.palette}")
                sys.exit("Error: Glyphs in atlas have >1 palette")
            prev_palette = glyph.palette

            if i == 0:
                # Write the palette once at the start
                new_palette = glyph.palette
                slpm.seek(CLUT_OFFSET)
                palette_bytes = bytes(
                    [component for color in glyph.palette for component in color]
                )
                slpm.write(palette_bytes)

            # Write the glyph pixels
            slpm.seek(PIXEL_OFFSET + i * BYTES_PER_GLYPH)
            slpm.write(glyph.to_bytes())

        remapped = 0
        if new_palette is not None and glyph_count < GLYPH_COUNT:
            lut = build_remap_lut(original_clut, new_palette)
            remapped = remap_unpatched_glyphs(slpm, lut, glyph_count)

    print(f"Patched {glyph_count} glyphs from {atlas_path} into {slpm_path}")
    if remapped:
        print(f"Remapped {remapped} unpatched glyphs onto the new CLUT")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        patch_font_from_atlas(sys.argv[1])
    elif len(sys.argv) == 3:
        patch_font_from_atlas(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python patch_font.py <atlas.png> [slpm_path]")
        sys.exit(1)
