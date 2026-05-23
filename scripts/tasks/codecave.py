# /// script
# requires-python = ">=3.10"
# ///
"""
Load scripts/data/codecave.bin into PHDR2 of translated/SLPM_625.32 so the
PS2 ELF loader copies it into RAM at vaddr CODECAVE_VADDR at boot. 
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path


CODECAVE_VADDR = 0x01F00000

PHDR2_FILE_OFF = 0x54
ALIGN = 0x10

# Original SLPM ends here (after section headers). Anything past this is
# appended content we own and can truncate.
ORIGINAL_SLPM_END = 0x15F530


def _round_up(n: int, align: int) -> int:
    return (n + align - 1) & ~(align - 1)


def load_codecave_into_phdr2(codecave_path: Path, slpm_path: Path):

    if not slpm_path.exists():
        raise FileNotFoundError(f"{slpm_path} not found")
    if not codecave_path.exists():
        raise FileNotFoundError(f"error: {codecave_path} not found")

    data = bytearray(slpm_path.read_bytes())

    # Align before appending so the new p_offset stays aligned.
    pad = _round_up(len(data), ALIGN) - len(data)
    data.extend(b"\x00" * pad)

    cave_offset = len(data)
    cave_bytes = codecave_path.read_bytes()
    data.extend(cave_bytes)

    # Pad the cave content itself to alignment so the file ends clean.
    cave_filesz = _round_up(len(cave_bytes), ALIGN)
    data.extend(b"\x00" * (cave_filesz - len(cave_bytes)))

    struct.pack_into(
        "<8I", data, PHDR2_FILE_OFF,
        1,                  # p_type = PT_LOAD
        cave_offset,        # p_offset
        CODECAVE_VADDR,     # p_vaddr
        CODECAVE_VADDR,     # p_paddr
        cave_filesz,        # p_filesz
        cave_filesz,        # p_memsz
        7,                  # p_flags = R+W+X (codecave is executable)
        ALIGN,              # p_align
    )

    slpm_path.write_bytes(bytes(data))

    print(f"Loaded codecave.bin ({len(cave_bytes)} bytes, padded to "
          f"0x{cave_filesz:x}) at vaddr 0x{CODECAVE_VADDR:08x} "
          f"(file offset 0x{cave_offset:x})")


if __name__ == "__main__":
    sys.exit(load_codecave_into_phdr2())
