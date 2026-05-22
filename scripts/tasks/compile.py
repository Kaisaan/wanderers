import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libwanderers.script import wscript_to_bin


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/tasks/compile.py stage00.wscript stage00.bin")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as fp:
        bin_data = wscript_to_bin(fp.read())
    with open(sys.argv[2], "wb") as fp:
        fp.write(bin_data)
