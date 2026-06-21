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
from typing import Any, Iterator, TypeAlias, TypedDict, cast

import yaml  # type: ignore[import-untyped]

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

LAYOUT = {
    "section_x": 0x30,
    "section_y": 0x60,
    "title_x": 0x30,
    "row_y": 0x90,
    "name_x": 0x90,
    "line_step": 0x18,
}

LINE_ROLE_X = {
    "section": LAYOUT["section_x"],
    "title": LAYOUT["title_x"],
    "heading": LAYOUT["title_x"],
    "name": LAYOUT["name_x"],
}

Command: TypeAlias = dict[str, Any]
TextRef: TypeAlias = str | dict[str, str]


class Line(TypedDict, total=False):
    section: TextRef
    title: TextRef
    heading: TextRef
    name: TextRef


class WaitSpec(TypedDict, total=False):
    frames: int


class ClearSpec(TypedDict, total=False):
    start: int
    count: int
    hold: int
    slide: int


class Page(TypedDict, total=False):
    movie: int
    start_row: int
    lines: list[Line]
    wait: WaitSpec
    clear: ClearSpec


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


def decode(bin_bytes: bytes, labels: list[str]) -> list[Command]:
    """Decode a credits script slice into YAML commands."""
    commands: list[Command] = []
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


def _decode_one(
    x: int, y: int, op: int, a0: int, a1: int, ptr: int, nxt: Iterator[str]
) -> Command:
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


def new_strings(commands: list[Command]) -> tuple[dict[str, str], list[str]]:
    """Collect brand-new credit strings in first-seen order."""
    label_by_text: dict[str, str] = {}
    order: list[str] = []
    used: set[str] = set()
    for cmd in commands:
        if cmd.get("op") != "text" or cmd.get("label") or cmd.get("str") is None:
            continue
        text = cast(str, cmd["str"])
        if text in label_by_text:
            continue
        base, label, n = f"cred_{_slug(text)}", f"cred_{_slug(text)}", 2
        while label in used:
            label, n = f"{base}_{n}", n + 1
        label_by_text[text] = label
        used.add(label)
        order.append(text)
    return label_by_text, order


def _words(cmd: Command) -> tuple[int, int, int, int, int, int]:
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
        return cast(tuple[int, int, int, int, int, int], tuple(cmd["words"]))
    raise ValueError(f"unknown op: {op!r}")


def _h(v: int) -> str:
    """Format a value as compact lowercase hex."""
    return f"0x{v:x}"


class _FlowDict(dict[str, Any]):
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


def to_yaml_text(commands: list[Command]) -> str:
    """Emit the flat YAML command list."""
    data = [_FlowDict(cmd) for cmd in commands]
    return yaml.dump(data, Dumper=_Dumper, sort_keys=False, allow_unicode=True)


def _asm_string(text: str) -> str:
    """Quote a string for armips output."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _asm_word(value: int) -> str:
    """Format a VM word as fixed-width lowercase hex."""
    return f"0x{value:08x}"


def to_asm_text(commands: list[Command]) -> str:
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


def _asm_full(cmd: Command, new_labels: dict[str, str]) -> str:
    """Emit one full `.dw` command row."""
    x, y, opc, a0, a1, ptr = _words(cmd)
    if cmd["op"] == "text":
        if cmd.get("label"):
            ptr_field = cast(str, cmd["label"])
        elif cmd.get("str") is not None:
            ptr_field = new_labels[cast(str, cmd["str"])]
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
    return f".dw {', '.join(fields)}"


def _text_ref(value: TextRef) -> dict[str, str]:
    """Normalize a semantic text reference into a text command payload."""
    if type(value) is str:
        return {"label": value}

    text_ref = cast(dict[str, str], value)
    has_label = "label" in text_ref
    has_str = "str" in text_ref
    if has_label == has_str:
        raise ValueError("text must have exactly one of label or str")
    key = "label" if has_label else "str"
    text = text_ref[key]
    return {key: text}


def _text_cmd(x: int, y: int, value: TextRef) -> Command:
    """Build a low-level text command from a semantic text reference."""
    cmd = {"op": "text", "x": x, "y": y}
    cmd.update(_text_ref(value))
    return cmd


def _page_lines(lines: list[Line], start_row: int = 0) -> tuple[list[Command], int]:
    """Expand one semantic page into low-level text commands."""
    row = start_row
    commands = []
    for line in lines:
        line_map = cast(dict[str, TextRef], line)
        roles = [role for role in LINE_ROLE_X if role in line_map]
        if len(roles) != 1:
            allowed = ", ".join(sorted(LINE_ROLE_X))
            raise ValueError(f"line must have one of {allowed}")
        unknown = sorted(set(line_map) - set(LINE_ROLE_X))
        if unknown:
            raise ValueError("line has unknown field(s): " + ", ".join(unknown))

        role = roles[0]
        if role == "section":
            y = LAYOUT["section_y"]
        else:
            y = LAYOUT["row_y"] + (row * LAYOUT["line_step"])
            row += 1
        commands.append(_text_cmd(LINE_ROLE_X[role], y, line_map[role]))
    return commands, row


def _page_wait(wait: WaitSpec) -> Command:
    """Build the wait command after a semantic page."""
    cmd: Command = {"op": "wait"}
    if "frames" in wait:
        cmd["frames"] = wait["frames"]
    return cmd


def _page_clear(clear: ClearSpec, default_count: int) -> Command:
    """Build the clear command after a semantic page."""
    cmd: Command = {
        "op": "clear",
        "start": clear.get("start", 1),
        "count": clear.get("count", default_count),
    }
    for key in ("hold", "slide"):
        if key in clear:
            cmd[key] = clear[key]
    return cmd


def yaml_to_commands(pages: list[Page]) -> list[Command]:
    """Expand credits pages into the low-level command stream."""
    if not pages:
        raise ValueError("credits YAML must be a non-empty list")

    commands: list[Command] = []
    allowed = {"movie", "start_row", "lines", "wait", "clear"}
    for page in pages:
        unknown = sorted(set(page) - allowed)
        if unknown:
            raise ValueError("page has unknown field(s): " + ", ".join(unknown))

        if "movie" in page:
            commands.append(
                {
                    "op": "movie",
                    "index": page["movie"],
                }
            )

        lines, clear_count = _page_lines(page["lines"], page.get("start_row", 0))
        commands.extend(lines)

        wait: WaitSpec = page.get("wait", {})
        clear: ClearSpec = page.get("clear", {})
        commands.append(_page_wait(wait))
        commands.append(_page_clear(clear, clear_count))

    commands.append({"op": "end"})
    return commands


def cmd_to_yaml(args: argparse.Namespace) -> None:
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


def cmd_to_asm(args: argparse.Namespace) -> None:
    """Handle the to-asm subcommand."""
    pages = cast(list[Page], yaml.safe_load(args.yaml.read_text(encoding="utf-8")))
    commands = yaml_to_commands(pages)
    text = to_asm_text(commands)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"wrote {args.out}  (include from asm/codecave.asm)")


def main() -> None:
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
