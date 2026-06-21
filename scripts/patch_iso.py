# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-api-python-client",
#     "google-auth",
#     "pillow",
# ]
# ///
import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from libwanderers.archive import pack
from libwanderers.script import wscript_to_bin
from scripts.tasks.codecave import load_codecave_into_phdr2
from tasks.from_csv import from_csv
from tasks.from_sheets import from_sheets
from tasks.patch_font import patch_font_from_atlas
from tasks.update_graphics import insert_all_graphics

STAGES = ["00", "01", "02", "03", "04", "05", "06"]
PATCHED_BIN = "Ys III - Wanderers from Ys [English Patched].bin"
PATCHED_CUE = "Ys III - Wanderers from Ys [English Patched].cue"


def apply_csvs(csv_dir: str, wscript_dir: str):
    """
    Apply EN translations from <csv_dir>/stageNN.csv onto
    <wscript_dir>/stageNN.wscript in place. Silently skips stages with
    no CSV.
    """
    csv_path = Path(csv_dir)
    if not csv_path.is_dir():
        print(f"No {csv_dir}/ directory; skipping translation step.")
        return

    for stage in STAGES:
        csv_file = csv_path / f"stage{stage}.csv"
        wscript_file = Path(wscript_dir) / f"stage{stage}.wscript"
        if not csv_file.exists() or not wscript_file.exists():
            continue
        print(f"Applying {csv_file} to {wscript_file}")
        from_csv(str(wscript_file), str(csv_file), str(wscript_file))


def compile_all(wscript_dir: str, bin_dir: str):
    Path(bin_dir).mkdir(parents=True, exist_ok=True)
    for stage in STAGES:
        src = Path(wscript_dir) / f"stage{stage}.wscript"
        dst = Path(bin_dir) / f"stage{stage}.bin"
        if not src.exists():
            print(f"  {src} missing; skipping")
            continue
        print(f"  {src} -> {dst}")
        wscript = src.read_text(encoding="utf-8")
        dst.write_bytes(wscript_to_bin(wscript))


def generate_translated_xml(in_xml: str, out_xml: str):
    """
    Rewrite every source="extracted/..." in the ISO project XML to point
    at translated/... so mkpsxiso pulls the patched copies.
    """
    tree = ET.parse(in_xml)
    for elem in tree.iter():
        src = elem.get("source")
        if src and src.startswith("extracted/"):
            elem.set("source", "translated/" + src[len("extracted/"):])
    tree.write(out_xml, encoding="utf-8", xml_declaration=True)


def main(sheets: bool = False):
    if sheets:
        print("Pulling latest translations from Google Sheets...")
        from_sheets("decompiled")
    else:
        print("Applying translations from CSVs...")
        apply_csvs("csv", "decompiled")
    print("Done!")

    print("Compiling .wscript files to .bin...")

    """
    replace_wscript_block(
        "decompiled/stage00.wscript",
        "LABEL_000066",
        Path("scripts", "data", "debug.wscript").read_text(encoding="utf-8"),
    )
    """

    compile_all("decompiled", "DATA/script")
    print("Done!")

    print("Inserting graphics...")
    insert_all_graphics()
    print("Done!")

    shutil.copy(Path("scripts/data/YS3ED12.gbxa"), Path("DATA/ending/epilog2.bin"))
    print("Repacking DATA.BIN...")
    pack("DATA.BIN")
    print("Done!")

    print("Applying SLPM patches with armips...")
    subprocess.run(["armips", "asm/patch.asm"], check=True)
    print("Done!")

    print("Loading codecave.bin into PHDR2...")
    load_codecave_into_phdr2(Path("scripts/data/codecave.bin"), Path("translated/SLPM_625.32"))
    print("Done!")

    print("Patching font...")
    patch_font_from_atlas("scripts/data/font_atlas.png")
    print("Done!")

    print("Replacing OPENING...")
    shutil.copy("scripts/data/OPENING.PSS", "translated/MOVIE")
    print("Done!")

    print("Generating translated.xml...")
    generate_translated_xml("wanderers.xml", "translated.xml")
    print("Done!")

    print("Rebuilding ISO...")
    subprocess.run(
        [
            "mkpsxiso",
            "-y",
            "-o",
            PATCHED_BIN,
            "-c",
            PATCHED_CUE,
            "translated.xml",
        ],
        check=True,
    )
    print(f"Patched ISO saved to {PATCHED_BIN}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patch ISO with translations")
    parser.add_argument(
        "--sheets",
        action="store_true",
        help="Pull latest translations from Google Sheets. If unset, uses local CSV files.",
    )
    args = parser.parse_args()
    main(args.sheets)
