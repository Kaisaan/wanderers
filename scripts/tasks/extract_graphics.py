import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libwanderers.graphics import extract_graphics


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
            extract_frames = (name in FRAMES)
            extract_graphics(anm_file, extract_frames)

    print("\nGraphics extraction complete!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_graphic.py <filepath> [frame]")
        sys.exit(1)

    filepath = sys.argv[1]
    extract_frames = len(sys.argv) == 3 and sys.argv[2] == "frame"

    extract_graphics(filepath, extract_frames)
