"""
Ys III graphics (_anm.bin) extractor & inserter.
"""
import os, shutil

from pathlib import Path
from struct import pack

from PIL import Image


NAXA_MAGIC = b'NAXA5010'
GBXA_MAGIC = b'GBXA2000'


def _intlit(b: bytes) -> int:
    return int.from_bytes(b, "little")

def _writeint(num, size):
    return num.to_bytes(size, byteorder="little")

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
        index = _intlit(graphic.read(4))           
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

        logFile.write(f"{filename}_{x}.png (index is {index:X}) is at {realOffset:X} (sprite offset is {sprOffset:X}) its size is {sprSize[0]:X}H and {sprSize[1]:X}W its data size is {sprDataSize:X} bytes\n")

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
    
def update_naxa(filepath: str | Path, insert_frames: bool = False):
    """
    Insert edited graphics back into an _anm.bin file.
    
    Args:
        filepath: Path to the _anm.bin file
        insert_frames: Whether to insert frame data (for files like menu00_anm.bin)
    """

    filepath = Path(filepath).resolve()
    filedir = filepath.parent
    filename = filepath.name

    origFile = open(filepath, "rb")

    filename = filename[:filename.rfind("_anm.bin")]

    input_dir = filedir / filename

    shutil.copy(filepath, filedir / f"{filename}_new.bin")

    newFile = open(filedir / f"{filename}_new.bin", "r+b")

    header = origFile.read(0x20)

    newFile.seek(0)
    newFile.write(header)

    clutSize = _intlit(header[0x8:0xC])
    clutOffset = _intlit(header[0xC:0x10])
    pxlOffset = _intlit(header[0x10:0x14])
    anmOffset = _intlit(header[0x14:0x18])

    bpp = 0

    if (clutSize == 256):
        bpp = 8
    elif (clutSize == 16):
        bpp = 4
    else:
        exit("other BPP formats not supported yet")

    palSize = 4

    with open(input_dir / f"{filename}_orig.pal", "rb") as palFile:
        clut = palFile.read(clutSize * palSize)

    newFile.seek(clutOffset)
    newFile.write(clut)

    if insert_frames:

        origFile.seek(anmOffset)
        newFile.seek(anmOffset)
        frameCount = _intlit(origFile.read(4))

        anmPadding = 16 - ((frameCount * 0x4 + 0x4) % 16)
        anmSize = (frameCount * 0x4 + 0x4) + anmPadding
        newFile.write(_writeint(frameCount, 4))

        frameOffset = anmSize

        for x in range(frameCount):
            
            size = os.stat(input_dir / f"{filename}_frame_{x}.bin").st_size
            newFile.write(_writeint(frameOffset, 4))
            frameOffset = frameOffset + size

        for x in range(anmPadding):
            newFile.write(b"\xFF")

        for x in range(frameCount):
            frame = open(input_dir / f"{filename}_frame_{x}.bin", "rb")
            frameData = frame.read()
            newFile.write(frameData)
            print(f"{filename}/{filename}_frame_{x}.bin written!")

    origFile.seek(pxlOffset + 8) # Read the first image offset to calculate how many images there are
    newFile.seek(pxlOffset)

    spriteCount = _intlit(origFile.read(4)) // 0x10 # Each sprite entry is 16 bytes long

    dataOffset = spriteCount * 0x10
    sprOffset = dataOffset

    padding = 0

    for x in range(spriteCount):
        graphic = Image.open(input_dir / f"{filename}_{x}.png", "r")
        size = graphic.width * graphic.height
        if bpp == 4:
            size = size // 2
            if (size % 16 != 0):
                padding = size % 16
            else:
                padding = 0
        
        if insert_frames:
            newFile.write(_writeint(graphic.height, 2))
            newFile.write(_writeint(graphic.width, 2))
        
        else:
            newFile.read(4)
        newFile.write(_writeint(graphic.height, 2))
        newFile.write(_writeint(graphic.width, 2))

        newFile.write(_writeint(sprOffset, 4))
        newFile.read(4)
        #newFile.write(_writeint(x, 4))
        sprOffset = sprOffset + size + padding

    for x in range(spriteCount):
        graphic = Image.open(input_dir / f"{filename}_{x}.png", "r")

        data = list(graphic.getdata())
        
        binData = b""
        if (bpp == 8):
            for i in range(len(data)):
                byte = data[i].to_bytes(1)
                binData = binData + byte
        elif (bpp == 4):
            for i in range(0, len(data), 2):
                byte1 = data[i]
                byte2 = data[i+1]
                if byte1 == 16:
                    byte1 = 1
                if byte2 == 16:
                    byte2 = 1
                byte2 = byte2 << 4
                byte = byte2 + byte1
                byte = byte.to_bytes(1)
                binData = binData + byte

        size = graphic.width * graphic.height
        if bpp == 4:
            size = size // 2
            if (size % 16 != 0):
                padding = size % 16
            else:
                padding = 0

        if (x != (spriteCount - 1)) or (padding != 0):      # No need to add padding to the last sprite
            for i in range(padding):
                binData = binData + b"\x00"
        
        newFile.write(binData)

        print(f"{filename}/{filename}_{x}.png written!")

    origFile.close()
    newFile.close()
    
    print(f"{filename}_new.bin saved!")

def update_gbxa(filepath: str | Path):
    """
    Insert edited graphics back into a .bin file.
    
    Args:
        filepath: Path to the .bin file
    """

    filepath = Path(filepath).resolve()
    filedir = filepath.parent
    filename = filepath.name

    origFile = open(filepath, "rb")

    filename = filename[:filename.rfind(".bin")]

    input_dir = filedir / filename

    shutil.copy(filepath, filedir / f"{filename}_new.bin")

    newFile = open(filedir / f"{filename}_new.bin", "r+b")

    header = origFile.read(0x20)

    newFile.seek(0)
    newFile.write(header)

    clutSize = _intlit(header[0x8:0xC])
    clutOffset = _intlit(header[0xC:0x10])
    pxlOffset = _intlit(header[0x10:0x14])
    sprW = _intlit(header[0x14:0x16])
    sprH = _intlit(header[0x16:0x18])
    blockW = _intlit(header[0x18:0x1A])
    blockH = _intlit(header[0x1A:0x1C])
    gfxW = _intlit(header[0x1C:0x1E])
    gfxH = _intlit(header[0x1E:0x20])

    bpp = 0

    if (clutSize == 256):
        bpp = 8
    elif (clutSize == 16):
        exit("GBXA with 4BPP graphics not supported yet")
    else:
        exit("other BPP formats not supported yet")

    palSize = 4

    with open(input_dir / f"{filename}_orig.pal", "rb") as palFile:
        clut = palFile.read(clutSize * palSize)

    newFile.seek(clutOffset)
    newFile.write(clut)

    for x in range(blockW * blockH):
        graphic = Image.open(input_dir / f"{filename}_{x}.png", "r")

        data = list(graphic.getdata())

        binData = b""
        if (bpp == 8):
            for i in range(len(data)):
                byte = data[i].to_bytes(1)
                binData = binData + byte

        newFile.write(binData)
        
        print(f"{filename}/{filename}_{x}.png written!")

    newFile.close()
    origFile.close()

def insert_graphics(filepath: str | Path, extract_frames: bool = False):
    """
    Fingerprint the file by its 8-byte identifier and dispatch to the
    matching format-specific extractor. extract_frames is ignored for
    GBXA files (no animation table).
    """
    fmt = fingerprint(filepath)
    if fmt == "naxa":
        update_naxa(filepath, extract_frames)
    elif fmt == "gbxa":
        update_gbxa(filepath)
    else:
        raise ValueError(f"{filepath}: unknown graphics identifier (not NAXA5010 or GBXA2000)")
