"""
Ys III graphics (_anm.bin) extractor.
"""

from pathlib import Path
from struct import pack

from PIL import Image


NAXA_MAGIC = b'NAXA5010'
GBXA_MAGIC = b'GBXA2000'


def _intlit(b: bytes) -> int:
    return int.from_bytes(b, "little")


def fingerprint(filepath: str | Path) -> str | None:
    """
    Return 'naxa', 'gbxa', or None based on the file's 8-byte identifier.
    """
    with open(filepath, "rb") as f:
        ident = f.read(8)
    if ident == NAXA_MAGIC:
        return "naxa"
    if ident == GBXA_MAGIC:
        return "gbxa"
    return None


def _read_clut(graphic, output_dir: Path, filename: str, logFile, clutSize: int, clutOffset: int):
    """
    Reads the CLUT and writes to .pal. Returns (clut_bytes, bpp).
    8BPP CLUTs are swizzled in 0x80-byte rows; 4BPP CLUTs are used as-is.
    """
    palSize = 4

    if clutSize == 256:
        bpp = 8
        logFile.write(f"{filename} is 8BPP\n")
    elif clutSize == 16:
        bpp = 4
        logFile.write(f"{filename} is 4BPP\n")
    else:
        raise ValueError(f"unsupported CLUT size {clutSize}")

    sectionSize = 0x20

    graphic.seek(clutOffset)

    if bpp == 8:
        origclut = graphic.read(clutSize * palSize)
        with open(output_dir / f"{filename}_orig.pal", "wb") as palette:
            palette.write(origclut)
        print(f"{filename}/{filename}_orig.pal saved!")

        clut = b''
        for i in range(8):          # Swizzle the palette (there's probably a better way to do this, but it works!)
            palOffset = i * 0x80
            for sub in (0x00, 0x40, 0x20, 0x60):
                graphic.seek(clutOffset + palOffset + sub)
                clut += graphic.read(sectionSize)
        with open(output_dir / f"{filename}_swzl.pal", "wb") as palette:
            palette.write(clut)
        print(f"{filename}/{filename}_swzl.pal saved!")
        return clut, bpp

    clut = graphic.read(clutSize * palSize)
    with open(output_dir / f"{filename}_orig.pal", "wb") as palette:
        palette.write(clut)
    print(f"{filename}/{filename}_orig.pal saved!")
    return clut, bpp


def extract_naxa(filepath: str | Path, extract_frames: bool = False):
    filepath = Path(filepath).resolve()
    filedir = filepath.parent
    filename = filepath.name

    graphic = open(filepath, "rb")

    header = graphic.read(0x20)

    if header[0x0:0x8] != NAXA_MAGIC:
        raise ValueError(f"{filepath} is not a NAXA5010 file")

    filename = filename[:filename.rfind("_anm.bin")]
    output_dir = filedir / filename
    output_dir.mkdir(exist_ok=True)

    logFile = open(output_dir / f"{filename}.txt", "w", encoding="utf-8")
    logFile.write("naxa\n")

    clutSize = _intlit(header[0x8:0xC])
    clutOffset = _intlit(header[0xC:0x10])
    pxlOffset = _intlit(header[0x10:0x14])
    anmOffset = _intlit(header[0x14:0x18])
    logFile.write(f"pixel offset is {pxlOffset:X}\n")
    logFile.write(f"anm offset is {anmOffset:X}\n")

    clut, bpp = _read_clut(graphic, output_dir, filename, logFile, clutSize, clutOffset)

    graphic.seek(pxlOffset + 8) # Read the first image offset to calculate how many images there are

    sprCount = _intlit(graphic.read(4)) // 0x10 # Each sprite entry is 16 bytes long

    graphic.seek(pxlOffset)

    for x in range(sprCount):

        entry = x * 0x10

        graphic.seek(pxlOffset + entry)
        graphic.read(4)  # Skip sprWvram and sprHvram
        sprW = _intlit(graphic.read(2))
        sprH = _intlit(graphic.read(2))
        sprOffset = _intlit(graphic.read(4))
        graphic.read(4)  # Skip sprIndex
        sprSize = (sprH, sprW)
        sprDataSize = sprH * sprW
        realOffset = pxlOffset + sprOffset
        graphic.seek(realOffset)

        if bpp == 4:
            sprDataSize = sprDataSize // 2
            sprData4 = graphic.read(sprDataSize)

            with open(output_dir / f"{filename}_{x}_packed.bin", "wb") as bin: # Save the original indexing data separate from the image to help with re-insertion
                bin.write(sprData4)
            print(f"{filename}/{filename}_{x}_packed.bin saved!")

            sprData = b""
            for byte in sprData4:
                sprData += pack("bb", byte & 0xF, byte >> 4)
            with open(output_dir / f"{filename}_{x}_unpacked.bin", "wb") as bin:
                bin.write(sprData)
            print(f"{filename}/{filename}_{x}_unpacked.bin saved!")

        else:
            sprData = graphic.read(sprDataSize)
            with open(output_dir / f"{filename}_{x}_8bpp.bin", "wb") as bin:
                bin.write(sprData)

        sprite = Image.frombytes("P", sprSize, bytes(sprData))
        sprite.putpalette(clut, rawmode="RGBA")
        sprite.save(fp=output_dir / f"{filename}_{x}.png")
        print(f"{filename}/{filename}_{x}.png saved!")

        logFile.write(f"{filename}_{x}.png is at {realOffset:X} (sprite offset is {sprOffset:X}) its size is {sprSize[0]:X}H and {sprSize[1]:X}W its data size is {sprDataSize:X} bytes\n")

    if extract_frames:

        graphic.seek(anmOffset)

        anmCount = _intlit(graphic.read(4))

        frameSize = 0x70

        for x in range(anmCount):
            entry = x * 0x4
            graphic.seek(anmOffset + entry + 0x4) # Add 4 bytes since the first 4 holds anmCount

            frameOffset = _intlit(graphic.read(4))
            realOffset = frameOffset + anmOffset

            graphic.seek(realOffset)

            frameData = graphic.read(frameSize)

            with open(output_dir / f"{filename}_frame_{x}.bin", "wb") as frame:
                frame.write(frameData)
            print(f"{filename}/{filename}_frame_{x}.bin saved!")

            logFile.write(f"{filename}_frame_{x}.bin is at {realOffset:X}\n")

    graphic.close()
    logFile.close()


def extract_gbxa(filepath: str | Path):
    filepath = Path(filepath).resolve()
    filedir = filepath.parent
    filename = filepath.name

    graphic = open(filepath, "rb")

    header = graphic.read(0x20)

    if header[0x0:0x8] != GBXA_MAGIC:
        raise ValueError(f"{filepath} is not a GBXA2000 file")

    filename = filename[:filename.rfind(".bin")]
    output_dir = filedir / filename
    output_dir.mkdir(exist_ok=True)

    logFile = open(output_dir / f"{filename}.txt", "w", encoding="utf-8")
    logFile.write("gbxa\n")

    clutSize = _intlit(header[0x8:0xC])
    clutOffset = _intlit(header[0xC:0x10])
    pxlOffset = _intlit(header[0x10:0x14])
    sprW = _intlit(header[0x14:0x16])
    sprH = _intlit(header[0x16:0x18])
    blockW = _intlit(header[0x18:0x1A])
    blockH = _intlit(header[0x1A:0x1C])
    gfxW = _intlit(header[0x1C:0x1E])
    gfxH = _intlit(header[0x1E:0x20])
    logFile.write(f"pixel offset is {pxlOffset:X}\n")
    logFile.write(f"Block size is {sprW} ({sprW:X}H) pixels wide and {sprH} ({sprH:X}H) pixels high\n")
    logFile.write(f"Graphic size is {blockW} ({blockW:X}H) blocks wide and {blockH} ({blockH:X}H) high\n")
    logFile.write(f"The full image is {gfxW} ({gfxW:X}H) pixels wide and {gfxH} ({gfxH:X}H) pixels high\n")

    clut, _bpp = _read_clut(graphic, output_dir, filename, logFile, clutSize, clutOffset)

    full = Image.new("P", (gfxH, gfxW))

    graphic.seek(pxlOffset)

    for j in range(blockH * blockW):
        sprData = graphic.read(sprH * sprW)
        sprite = Image.frombytes("P", (sprH, sprW), sprData)
        sprite.putpalette(clut, rawmode="RGBA")

        x = (j % (blockH))          # Funny math stuff to get proper coordinates
        y = (j // (blockH))

        full.paste(sprite, (x*sprW, y*sprH))
        sprite.save(fp=output_dir / f"{filename}_{j}.png")
        print(f"{filename}_{j}.png saved!")

    full.putpalette(clut, rawmode="RGBA")
    full.save(fp=output_dir / f"{filename}_full.png")
    print(f"{filename}_full.png saved!")

    graphic.close()
    logFile.close()


def extract_graphics(filepath: str | Path, extract_frames: bool = False):
    """
    Fingerprint the file by its 8-byte identifier and dispatch to the
    matching format-specific extractor. extract_frames is ignored for
    GBXA files (no animation table).
    """
    fmt = fingerprint(filepath)
    if fmt == "naxa":
        extract_naxa(filepath, extract_frames)
    elif fmt == "gbxa":
        extract_gbxa(filepath)
    else:
        raise ValueError(f"{filepath}: unknown graphics identifier (not NAXA5010 or GBXA2000)")
