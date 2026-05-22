"""
Ys III text codec.

The game stores Shift-JIS text bitwise-NOT'd (XOR 0xFF) with inline
control codes for color (FF FC XX) and frame-delay sleeps (FF FD XX).
The renderer (FUN_0010f560 in SLPM_625.32) also accepts equivalent
ASCII color tags of the form #XX -- we emit those for parity with
Lost Kefin's DSL style.

This module is independent of the script .bin format; it's used
anywhere obfuscated text appears (script dialog, menu strings, etc.).
"""

import re


# Text color control codes. The renderer accepts both the 3-byte binary
# form FF FC XX and the equivalent 3-char ASCII form (#XX); we emit the
# ASCII form on decode.
COLOR_CODES = {
    0: "#bk",  # black
    1: "#bl",  # blue
    2: "#re",  # red
    3: "#gr",  # green
    4: "#pi",  # pink
    5: "#yl",  # yellow / gold
    6: "#wh",  # white
    7: "#gl",  # gray (renderer's default branch; any unknown value hits gray)
}


def read_string(io, length) -> str:
    """
    Decode a string from the game's obfuscated form.
    1. Read `length` bytes and invert each (XOR 0xFF) -- Ys III stores
       text bitwise-NOT'd.
    2. Replace FF FC XX with the matching #XX color tag.
    3. Replace FF FD XX with <sleep XX> (frame delay).
    4. Decode shift-jis, escape newlines.
    """
    s = bytes(b ^ 0xFF for b in io.read(length))

    out = s[:]
    for i in range(len(s) - 2):
        if s[i] == 0xFF and s[i + 1] == 0xFC:
            tag = COLOR_CODES.get(s[i + 2], f"<color {s[i + 2]}>")
            out = out.replace(s[i : i + 3], tag.encode("shift-jis"))
        elif s[i] == 0xFF and s[i + 1] == 0xFD:
            tag = f"<sleep {s[i + 2]}>"
            out = out.replace(s[i : i + 3], tag.encode("shift-jis"))

    decoded = out.decode("shift-jis")
    decoded = decoded.replace("\n", "\\n")
    return decoded


def encode_string(s):
    """
    Inverse of read_string. Returns [u8 length][len bytes XOR'd 0xFF].
    """
    s = s.replace("\\n", "\n")

    encoded = s.encode("shift-jis")

    while b"<sleep " in encoded:
        encoded = re.sub(
            rb"<sleep (\d+)>",
            lambda m: b"\xff\xfd" + int(m.group(1)).to_bytes(1, "little"),
            encoded,
        )
    for code, tag in COLOR_CODES.items():
        encoded = encoded.replace(
            tag.encode("shift-jis"),
            b"\xff\xfc" + code.to_bytes(1, "little"),
        )
    # Fallback for color values not in the named table.
    while b"<color " in encoded:
        encoded = re.sub(
            rb"<color (\d+)>",
            lambda m: b"\xff\xfc" + int(m.group(1)).to_bytes(1, "little"),
            encoded,
        )

    obfuscated = bytes(b ^ 0xFF for b in encoded)
    return len(obfuscated).to_bytes(1, "little") + obfuscated
