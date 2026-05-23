import shutil
import sys
from pathlib import Path
from struct import pack
from PIL import Image


# Map of graphics files to extract (name without _anm.bin suffix -> source path in DATA)
GRAPHICS_FILES = {
    "df00": "DATA/bossname/07/df00_anm.bin",
    "df01": "DATA/bossname/07/df01_anm.bin",
    "dularn00": "DATA/bossname/00/dularn00_anm.bin",
    "dularn01": "DATA/bossname/00/dularn01_anm.bin",
    "elfeilu00": "DATA/bossname/01/elfeilu00_anm.bin",
    "elfeilu01": "DATA/bossname/01/elfeilu01_anm.bin",
    "gildias00": "DATA/bossname/06/gildias00_anm.bin",
    "gildias01": "DATA/bossname/06/gildias01_anm.bin",
    "girun00": "DATA/bossname/02/girun00_anm.bin",
    "girun01": "DATA/bossname/02/girun01_anm.bin",
    "gyalva00": "DATA/bossname/03/gyalva00_anm.bin",
    "gyalva01": "DATA/bossname/03/gyalva01_anm.bin",
    "istersiva00": "DATA/bossname/04/istersiva00_anm.bin",
    "istersiva01": "DATA/bossname/04/istersiva01_anm.bin",
    "ligaty00": "DATA/bossname/05/ligaty00_anm.bin",
    "ligaty01": "DATA/bossname/05/ligaty01_anm.bin",
    "shp_waku01": "DATA/shop/shp_waku01_anm.bin",
    "shp_waku03": "DATA/shop/shp_waku03_anm.bin",
    "shp_waku04": "DATA/shop/shp_waku04_anm.bin",
    "win_stage": "DATA/worldmap/win_stage_anm.bin",
    "win_stg": "DATA/window/win_stg_anm.bin",
    "win_town": "DATA/window/win_town_anm.bin",
    "zzs00": "DATA/bossname/08/zzs00_anm.bin"

}

FRAMES = []


def intlit(bytes):
    return int.from_bytes(bytes, "little")


def extract_graphics(filepath: str | Path, extract_frames: bool = False):
    """
    Extract graphics from an _anm.bin file.
    
    Args:
        filepath: Path to the _anm.bin file
        extract_frames: Whether to extract frame data (for files like menu00_anm.bin)
    """
    filepath = Path(filepath).resolve()
    filedir = filepath.parent
    filename = filepath.name

    graphic = open(filepath, "rb")

    header = graphic.read(0x20)

    identifier = header[0x0:0x8]

    format = ""

    if (identifier == b'NAXA5010'):
        format = "naxa"
    elif (identifier == b'GBXA2000'):
        format = "gbxa"
    else:
        exit("Identifier not found! Might not be a graphics file.")

    if (format == "naxa"):
        filename = filename[:filename.rfind("_anm.bin")]
    else:
        filename = filename[:filename.rfind(".bin")]

    output_dir = filedir / filename
    output_dir.mkdir(exist_ok=True)

    logFile = open(output_dir / f"{filename}.txt", "w", encoding="utf-8")
    logFile.write(f"{format}\n")

    if (format == "naxa"):
        clutSize = intlit(header[0x8:0xC])
        clutOffset = intlit(header[0xC:0x10])
        pxlOffset = intlit(header[0x10:0x14])
        anmOffset = intlit(header[0x14:0x18])
        logFile.write(f"pixel offset is {pxlOffset:X}\n")
        logFile.write(f"anm offset is {anmOffset:X}\n")
    
    else:
        clutSize = intlit(header[0x8:0xC])
        clutOffset = intlit(header[0xC:0x10])
        pxlOffset = intlit(header[0x10:0x14])      
        sprW = intlit(header[0x14:0x16])
        sprH = intlit(header[0x16:0x18])
        blockW = intlit(header[0x18:0x1A])
        blockH = intlit(header[0x1A:0x1C])
        gfxW = intlit(header[0x1C:0x1E])
        gfxH = intlit(header[0x1E:0x20])
        logFile.write(f"pixel offset is {pxlOffset:X}\n")
        logFile.write(f"Block size is {sprW} ({sprW:X}H) pixels wide and {sprH} ({sprH:X}H) pixels high\n")
        logFile.write(f"Graphic size is {blockW} ({blockW:X}H) blocks wide and {blockH} ({blockH:X}H) high\n")
        logFile.write(f"The full image is {gfxW} ({gfxW:X}H) pixels wide and {gfxH} ({gfxH:X}H) pixels high\n")

    bpp = 0

    if (clutSize == 256):
        bpp = 8
        logFile.write(f"{filename} is 8BPP\n")
    elif (clutSize == 16):
        bpp = 4
        logFile.write(f"{filename} is 4BPP\n")
    else:
        exit("other BPP formats not supported yet")

    palSize = 4

    sectionSize = 0x20

    clut = b''

    palOffset = 0

    graphic.seek(clutOffset)

    clutPos = clutOffset

    if bpp == 8:

        origclut = graphic.read(clutSize * palSize)

        with open(output_dir / f"{filename}_orig.pal", "wb") as palette:
            palette.write(origclut)
        print(f"{filename}/{filename}_orig.pal saved!")

        graphic.seek(clutOffset)

        for i in range(8):          # Swizzle the palette (there's probably a better way to do this, but it works!)
            palOffset = i * 0x80

            clutPos = (clutOffset + (palOffset + 0))
            graphic.seek(clutPos)
            colours = graphic.read(sectionSize)
            clut = clut + colours

            clutPos = (clutOffset + (palOffset + (0x40)))
            graphic.seek(clutPos)
            colours = graphic.read(sectionSize)
            clut = clut + colours

            clutPos = (clutOffset + (palOffset + (0x20)))
            graphic.seek(clutPos)
            colours = graphic.read(sectionSize)
            clut = clut + colours

            clutPos = (clutOffset + (palOffset + (0x60)))
            graphic.seek(clutPos)
            colours = graphic.read(sectionSize)
            clut = clut + colours
        with open(output_dir / f"{filename}_swzl.pal", "wb") as palette:
            palette.write(clut)
        print(f"{filename}/{filename}_swzl.pal saved!")

    elif bpp == 4:
        clut = graphic.read(clutSize * palSize)
        with open(output_dir / f"{filename}_orig.pal", "wb") as palette:
            palette.write(clut)
        print(f"{filename}/{filename}_orig.pal saved!")
    
    if (format == "gbxa"):

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

        exit()

 
    if (format != "naxa"):
        exit("This shouldn't happen.")

    graphic.seek(pxlOffset + 8) # Read the first image offset to calculate how many images there are

    sprCount = intlit(graphic.read(4)) // 0x10 # Each sprite entry is 16 bytes long

    graphic.seek(pxlOffset)

    for x in range(sprCount):

        entry = x * 0x10

        graphic.seek(pxlOffset + entry)
        graphic.read(4)  # Skip sprWvram and sprHvram
        sprW = intlit(graphic.read(2))
        sprH = intlit(graphic.read(2))
        sprOffset = intlit(graphic.read(4))
        graphic.read(4)  # Skip sprIndex
        sprSize = (sprH, sprW)
        sprDataSize = sprH * sprW
        realOffset = pxlOffset + sprOffset
        graphic.seek(realOffset)

        if (bpp == 4):
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

        anmCount = intlit(graphic.read(4))

        frameSize = 0x70

        for x in range(anmCount):
            entry = x * 0x4
            graphic.seek(anmOffset + entry + 0x4) # Add 4 bytes since the first 4 holds anmCount

            frameOffset = intlit(graphic.read(4))
            realOffset = frameOffset + anmOffset

            graphic.seek(realOffset)

            frameData = graphic.read(frameSize)

            with open(output_dir / f"{filename}_frame_{x}.bin", "wb") as frame:
                frame.write(frameData)
            print(f"{filename}/{filename}_frame_{x}.bin saved!")
            
            logFile.write(f"{filename}_frame_{x}.bin is at {realOffset:X}\n")
    
    graphic.close()
    logFile.close()


def extract_all_graphics():
    """Extract graphics from all _anm.bin files."""
    print("\nExtracting graphics from _anm.bin files...")
    
    # Create graphics/orig directory
    graphics_orig = Path("graphics/orig")
    if graphics_orig.exists():
        shutil.rmtree(graphics_orig)
    graphics_orig.mkdir(parents=True, exist_ok=True)
    
    # Copy _anm.bin files to graphics/orig
    for name, source_path in GRAPHICS_FILES.items():
        source = Path(source_path)
        if source.exists():
            dest = graphics_orig / f"{name}_anm.bin"
            print(f"Copying {source} to {dest}")
            shutil.copy2(source, dest)
        else:
            print(f"Warning: {source} not found, skipping")
    
    # Extract graphics from each file
    for name in GRAPHICS_FILES.keys():
        anm_file = graphics_orig / f"{name}_anm.bin"
        if anm_file.exists():
            print(f"\nExtracting {name}...")
            # Special case for menu00: extract frame data
            extract_frames = (name in FRAMES)
            extract_graphics(anm_file, extract_frames)
    
    print("\nGraphics extraction complete!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python graphics.py <filepath> [frame]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    extract_frames = len(sys.argv) == 3 and sys.argv[2] == "frame"
    
    extract_graphics(filepath, extract_frames)


