#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyyaml",
# ]
# ///
"""Round-trip the Ys III credits script.

to-yaml extracts the original command stream from SLPM_625.32.
to-asm emits asm/credits.asm from scripts/data/credits.yaml.
"""

import argparse
import re
import struct
from pathlib import Path

import yaml

SCRIPT_VADDR = 0x235490
RAM_BASE = 0xFFF80
CMD_SIZE = 0x18
NULL_STR = 0x2511A8

ELF_PATH = Path("extracted/SLPM_625.32")
POINTERS_PATH = Path("asm/pointers.asm")
YAML_PATH = Path("scripts/data/credits.yaml")
ASM_PATH = Path("asm/credits.asm")

OP_MOVIE, OP_TEXT, OP_WAIT, OP_SLIDE, OP_CLEAR, OP_END = 1, 2, 3, 5, 6, 0xFFFFFFFF

DEFAULTS = {
    "text": {"hold": 0x8, "slide": 0x18},
    "wait": {"frames": 0x96},
    "clear": {"hold": 0x28, "slide": 0x18},
}


def vaddr_to_off(vaddr: int) -> int:
    """Convert a RAM virtual address to a file offset."""
    return vaddr - RAM_BASE


CREDITS_HEADER = "// Credits Text"
ENDING_HEADER = "// Ending Text"


def credit_labels(pointers: Path) -> list[str]:
    """Read the ordered credit string labels from pointers.asm."""
    lines = pointers.read_text(encoding="utf-8").splitlines()
    try:
        start = next(
            i for i, line in enumerate(lines) if line.strip() == CREDITS_HEADER
        )
        end = next(
            i for i in range(start + 1, len(lines)) if lines[i].strip() == ENDING_HEADER
        )
    except StopIteration:
        raise ValueError(f"{pointers}: could not find the Credits Text section")
    addrs = [
        m.group(1)
        for line in lines[start:end]
        if (m := re.match(r"\s*@L([0-9A-Fa-f]+):", line))
    ]
    if not addrs:
        raise ValueError(f"{pointers}: no @L labels under {CREDITS_HEADER!r}")
    return [f"credstr_{a}" for a in addrs[1:]]


def decode(bin_bytes: bytes, labels: list[str]) -> list[dict]:
    """Decode a credits script slice into YAML commands."""
    commands: list[dict] = []
    nxt = iter(labels)
    for i in range(len(bin_bytes) // CMD_SIZE):
        x, y, op, a0, a1, ptr = struct.unpack_from("<6I", bin_bytes, i * CMD_SIZE)
        commands.append(_decode_one(x, y, op, a0, a1, ptr, nxt))
        if op == OP_END:
            extra = list(nxt)
            if extra:
                raise ValueError(f"{len(extra)} more credit labels than text commands")
            return commands
    raise ValueError(
        f"{len(bin_bytes)} bytes with no -1 terminator "
        "(truncated, or not a credits script?)"
    )


def _decode_one(x, y, op, a0, a1, ptr, nxt) -> dict:
    """Decode one six-word VM command."""
    if op == OP_MOVIE and (x, y, a1, ptr) == (0, 0, 0, NULL_STR):
        return {"op": "movie", "index": a0}
    if op == OP_TEXT and ptr != NULL_STR:
        try:
            label = next(nxt)
        except StopIteration:
            raise ValueError(
                "more text commands than Credits Text labels in pointers.asm"
            )
        cmd = {"op": "text", "x": x, "y": y, "label": label}
        defaults = DEFAULTS["text"]
        if a0 != defaults["hold"]:
            cmd["hold"] = a0
        if a1 != defaults["slide"]:
            cmd["slide"] = a1
        return cmd
    if op == OP_WAIT and (x, y, a1, ptr) == (0, 0, 0, NULL_STR):
        cmd = {"op": "wait"}
        defaults = DEFAULTS["wait"]
        if a0 != defaults["frames"]:
            cmd["frames"] = a0
        return cmd
    if op == OP_SLIDE and (x, y, ptr) == (0, 0, NULL_STR):
        return {"op": "slide", "hold": a0, "slide": a1}
    if op == OP_CLEAR and ptr == NULL_STR:
        cmd = {"op": "clear", "start": x, "count": y}
        defaults = DEFAULTS["clear"]
        if a0 != defaults["hold"]:
            cmd["hold"] = a0
        if a1 != defaults["slide"]:
            cmd["slide"] = a1
        return cmd
    if op == OP_END and (x, y, a0, a1) == (0, 0, 0, 0):
        return {"op": "end"}
    return {"op": "raw", "words": [x, y, op, a0, a1, ptr]}


def _slug(text: str) -> str:
    """Build a label-safe slug from a new credit string."""
    s = re.sub(r"<[^>]*>", "", text).lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "line"


def new_strings(commands: list[dict]) -> tuple[dict[str, str], list[str]]:
    """Collect brand-new credit strings in first-seen order."""
    label_by_text: dict[str, str] = {}
    order: list[str] = []
    used: set[str] = set()
    for cmd in commands:
        if cmd.get("op") != "text" or cmd.get("label") or cmd.get("str") is None:
            continue
        text = cmd["str"]
        if text in label_by_text:
            continue
        base, label, n = f"cred_{_slug(text)}", f"cred_{_slug(text)}", 2
        while label in used:
            label, n = f"{base}_{n}", n + 1
        label_by_text[text] = label
        used.add(label)
        order.append(text)
    return label_by_text, order


def _words(cmd: dict) -> tuple[int, int, int, int, int, int]:
    """Encode one YAML command into the six VM words."""
    op = cmd["op"]
    if op == "movie":
        return (0, 0, OP_MOVIE, cmd["index"], 0, NULL_STR)
    if op == "text":
        return (
            cmd["x"],
            cmd["y"],
            OP_TEXT,
            cmd.get("hold", DEFAULTS["text"]["hold"]),
            cmd.get("slide", DEFAULTS["text"]["slide"]),
            0,
        )
    if op == "wait":
        return (
            0,
            0,
            OP_WAIT,
            cmd.get("frames", DEFAULTS["wait"]["frames"]),
            0,
            NULL_STR,
        )
    if op == "slide":
        return (0, 0, OP_SLIDE, cmd["hold"], cmd["slide"], NULL_STR)
    if op == "clear":
        return (
            cmd["start"],
            cmd["count"],
            OP_CLEAR,
            cmd.get("hold", DEFAULTS["clear"]["hold"]),
            cmd.get("slide", DEFAULTS["clear"]["slide"]),
            NULL_STR,
        )
    if op == "end":
        return (0, 0, OP_END, 0, 0, NULL_STR)
    if op == "raw":
        return tuple(cmd["words"])
    raise ValueError(f"unknown op: {op!r}")


def _h(v: int) -> str:
    """Format a value as compact lowercase hex."""
    return f"0x{v:x}"


class _FlowDict(dict):
    """Render one YAML command per line."""


class _Dumper(yaml.SafeDumper):
    pass


_Dumper.add_representer(
    int, lambda d, v: d.represent_scalar("tag:yaml.org,2002:int", f"0x{v:x}")
)
_Dumper.add_representer(
    _FlowDict,
    lambda d, v: d.represent_mapping("tag:yaml.org,2002:map", v, flow_style=True),
)


def to_yaml_text(commands) -> str:
    """Emit the flat YAML command list."""
    data = [_FlowDict(cmd) for cmd in commands]
    return yaml.dump(data, Dumper=_Dumper, sort_keys=False, allow_unicode=True)


def _asm_string(text: str) -> str:
    """Quote a string for armips output."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _asm_word(value: int) -> str:
    """Format a VM word as fixed-width lowercase hex."""
    return f"0x{value:08x}"


def to_asm_text(commands) -> str:
    """Emit the credits.asm include fragment."""
    new_labels, new_order = new_strings(commands)

    lines = [
        "// Ys III credits script -- generated by scripts/tasks/generate_credits.py.",
        "// Do not edit by hand; edit scripts/data/credits.yaml and re-run `to-asm`.",
        "",
        f"cred_null: equ 0x{NULL_STR:08x}",
        "",
        "credits_script:",
    ]
    for cmd in commands:
        lines.append(_asm_full(cmd, new_labels))

    if new_order:
        lines += [
            "",
            "// brand-new lines referenced by YAML `str` entries",
        ]
        for text in new_order:
            lines.append(f"{new_labels[text]}: .str {_asm_string(text)}")
        lines.append(".align 4")

    return "\n".join(lines) + "\n"


def _asm_full(cmd: dict, new_labels: dict[str, str]) -> str:
    """Emit one full `.dw` command row."""
    x, y, opc, a0, a1, ptr = _words(cmd)
    if cmd["op"] == "text":
        if cmd.get("label"):
            ptr_field = cmd["label"]
        elif cmd.get("str") is not None:
            ptr_field = new_labels[cmd["str"]]
        else:
            raise ValueError("a `text` command needs a `label` or a `str`")
    else:
        ptr_field = "cred_null" if ptr == NULL_STR else _asm_word(ptr)
    fields = [
        _asm_word(x),
        _asm_word(y),
        _asm_word(opc),
        _asm_word(a0),
        _asm_word(a1),
        ptr_field,
    ]
    return f".dw {', '.join(fields)}  // {_describe(cmd)}"


def _describe(cmd: dict) -> str:
    """Build the short trailing comment for an ASM command."""
    op = cmd["op"]
    if op == "movie":
        return f"movie {cmd['index']}"
    if op == "text":
        return (
            f"text -> {cmd['label']}"
            if cmd.get("label")
            else f'text "{cmd.get("str", "")}" (new)'
        )
    if op == "wait":
        return f"wait {_h(cmd.get('frames', DEFAULTS['wait']['frames']))}"
    if op == "slide":
        return "slide all off-screen"
    if op == "clear":
        return f"clear lines [{cmd['start']}, {cmd['start'] + cmd['count']})"
    if op == "end":
        return "end"
    return "raw"


def load_yaml(path: Path) -> list[dict]:
    """Load the flat YAML command list."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path}: expected a list of commands")
    return data


def cmd_to_yaml(args):
    """Handle the to-yaml subcommand."""
    elf = args.elf.read_bytes()
    off = vaddr_to_off(SCRIPT_VADDR)
    if off < 0 or off >= len(elf):
        raise ValueError(f"{args.elf}: {_h(SCRIPT_VADDR)} maps outside the file")

    commands = decode(elf[off:], credit_labels(args.pointers))
    text = to_yaml_text(commands)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"wrote {args.out}  ({len(commands)} commands)")


def cmd_to_asm(args):
    """Handle the to-asm subcommand."""
    commands = load_yaml(args.yaml)
    text = to_asm_text(commands)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"wrote {args.out}  (include from asm/codecave.asm)")


def main():
    """Parse arguments and dispatch the selected subcommand."""
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("to-yaml", help="SLPM_625.32 (+pointers.asm) -> credits.yaml")
    a.add_argument("elf", type=Path, nargs="?", default=ELF_PATH)
    a.add_argument("--pointers", type=Path, default=POINTERS_PATH)
    a.add_argument("--out", type=Path, default=YAML_PATH)
    a.set_defaults(func=cmd_to_yaml)

    a = sub.add_parser(
        "to-asm", help="credits.yaml -> asm/credits.asm (codecave include)"
    )
    a.add_argument("--yaml", type=Path, default=YAML_PATH)
    a.add_argument("--out", type=Path, default=ASM_PATH)
    a.set_defaults(func=cmd_to_asm)

    args = p.parse_args()
    try:
        args.func(args)
    except ValueError as e:
        raise SystemExit(f"error: {e}")


if __name__ == "__main__":
    main()
