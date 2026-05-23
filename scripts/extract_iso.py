# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pillow",
# ]
# ///
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from libwanderers.archive import unpack
from libwanderers.script import bin_to_wscript
from scripts.tasks.extract_graphics import extract_all_graphics

STAGES = ["00", "01", "02", "03", "04", "05", "06"]


def main():
    print("Copy the original .iso next to this script and rename it to lostkefin.iso")

    if os.path.exists("extracted"):
        shutil.rmtree("extracted")
    print("Extracting bin...")
    subprocess.run(
        ["dumpsxiso", "-x", "extracted", "-s", "wanderers.xml", Path("Ys III - Wanderers from Ys (Japan).bin")],
        stdout=subprocess.PIPE,
        text=True,
        shell=False,
    )

    # Copy extracted to translated
    if os.path.exists("translated"):
        shutil.rmtree("translated")
    shutil.copytree("extracted", "translated")
    print("Done!")

    print("Unpacking DATA.BIN...")
    unpack("DATA.BIN")

    print("Decompiling script files into .wscript files...")
    if os.path.exists("decompiled"):
        shutil.rmtree("decompiled")
    os.makedirs("decompiled", exist_ok=True)
    for stage in STAGES:
        print(f"Decompiling stage {stage}...")
        src = Path(f"DATA/script/stage{stage}.bin")
        dst = Path(f"decompiled/stage{stage}.wscript")
        dst.write_text(bin_to_wscript(src.read_bytes()), encoding="utf-8")
    print("Done!")

    print("Extracting graphics...")
    extract_all_graphics()
    print("Done!")


if __name__ == "__main__":
    main()
