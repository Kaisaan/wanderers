import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libwanderers.script import bin_to_wscript


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/tasks/decompile.py stage00.bin stage00.wscript")
        sys.exit(1)
    with open(sys.argv[1], "rb") as fp:
        wscript = bin_to_wscript(fp.read())
    with open(sys.argv[2], "w", encoding="utf-8") as fp:
        fp.write(wscript)
