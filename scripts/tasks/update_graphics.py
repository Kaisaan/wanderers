import shutil
import sys
from pathlib import Path

from .extract_graphics import GRAPHICS_FILES, FRAMES
from libwanderers.graphics import insert_graphics

def copy_tree(src, dst):
    """Copy directory tree, merging with existing files."""
    src_path = Path(src)
    dst_path = Path(dst)
    
    if not src_path.exists():
        print(f"Warning: {src} does not exist, skipping")
        return
    
    dst_path.mkdir(parents=True, exist_ok=True)
    
    for item in src_path.rglob("*"):
        if item.is_file():
            relative_path = item.relative_to(src_path)
            dest_file = dst_path / relative_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_file)
            print(f"Copied {item} to {dest_file}")

def insert_all_graphics():
    """Insert edited graphics back into all _anm.bin files."""
    print("\nInserting edited graphics into _anm.bin files...")
    
    graphics_orig = Path("graphics/orig")
    graphics_processed = Path("graphics/processed")
    graphics_frames = Path("graphics/frames")
    
    # Merge processed and frames into orig
    print("\nMerging processed graphics into orig...")
    copy_tree(graphics_processed, graphics_orig)
    
    print("\nMerging frame data into orig...")
    copy_tree(graphics_frames, graphics_orig)
    
    # Insert graphics into each file
    for name in GRAPHICS_FILES.keys():
        anm_file = graphics_orig / f"{name}_anm.bin"
        if anm_file.exists():
            print(f"\nInserting {name}...")
            insert_frames = (name in FRAMES)
            insert_graphics(anm_file, insert_frames)
        else:
            print(f"Warning: {anm_file} not found, skipping")
    
    # Copy _new.bin files back to DATA
    print("\nCopying patched graphics back to DATA...")
    for name, dest_path in GRAPHICS_FILES.items():
        new_file = graphics_orig / f"{name}_new.bin"
        if new_file.exists():
            dest = Path(dest_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(new_file, dest)
            print(f"Copied {new_file} to {dest}")
        else:
            print(f"Warning: {new_file} not found, skipping")
    
    print("\nGraphics insertion complete!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python insert.py <filepath> [frame]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    insert_frames = len(sys.argv) == 3 and sys.argv[2] == "frame"
    
    insert_graphics(filepath, insert_frames)