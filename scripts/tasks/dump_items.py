"""
Dump the item name table from extracted/SLPM_625.32 to a CSV.
"""

import csv
import os
import struct
import sys


ELF = os.path.join("extracted", "SLPM_625.32")
BASE_PTR = 0xFFF80
TABLE_FOFFSET = 0x135240
TABLE_MAX_BYTES = 0x400  # walk this far; bail on the first non-pointer


def read_cstring_sjis(fp, foffset, maxlen=256):
    fp.seek(foffset)
    raw = fp.read(maxlen)
    end = raw.find(b"\x00")
    if end != -1:
        raw = raw[:end]
    return raw.decode("shift-jis", errors="replace")


def extract_name(s):
    # Long-form entries are "Name：description" (full-width colon U+FF1A).
    # Newlines in the description live after the ：, so a plain split works.
    idx = s.find("：")
    if idx != -1:
        return s[:idx]
    return s


def dump_items(csv_path):
    with open(ELF, "rb") as fp:
        fp.seek(TABLE_FOFFSET)
        raw = fp.read(TABLE_MAX_BYTES)

        ptrs = []
        for off in range(0, len(raw), 4):
            (p,) = struct.unpack_from("<I", raw, off)
            if p != 0 and (p < BASE_PTR or p > 0x800000):
                break
            ptrs.append(p)

        with open(csv_path, "w", newline="", encoding="utf-8") as out:
            writer = csv.writer(out)
            writer.writerow(["ID", "Name"])
            for idx, p in enumerate(ptrs):
                if p == 0:
                    continue
                name = extract_name(read_cstring_sjis(fp, p - BASE_PTR))
                if not name:
                    continue
                writer.writerow([f"0x{idx:02x}", name])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/tasks/dump_items.py <out.csv>")
        sys.exit(1)
    dump_items(sys.argv[1])
