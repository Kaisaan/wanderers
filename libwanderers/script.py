"""
Ys III - Wanderers from Ys script .bin parser.

Decodes the binary script format into the DSL ("wscript") format and
back. The on-disk layout is:

    0x000..0x800   absolute pointer table (pairs of u32 index, u32 offset),
                   terminated by an index==0 entry.
    0x800..EOF     opcode stream; offsets in the pointer table are
                   relative to 0x800.
"""

import re
import sys
import json

from .characters import get_character_name, get_character_index


def format_value(value):
    """
    Format a value for DSL output, adding quotes if it contains spaces or special chars
    """
    if isinstance(value, str):
        if "\t" in value:
            raise ValueError(f"Tab in value: {value}")
        return value
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def instruction_to_dsl(instruction):
    """
    Convert a single instruction dict to DSL format
    """
    if not isinstance(instruction, dict) or "name" not in instruction:
        raise ValueError("Instruction must be a dict with a 'name' key")

    parts = [instruction["name"]]

    # Add all other keys as key:value pairs
    for key, value in instruction.items():
        if key != "name":  # Skip the name since it's already added
            formatted_value = format_value(value)
            parts.append(f"{key}:{formatted_value}")

    return "\t".join(parts)


def line_to_op(line: str):
    """
    Given a single line of a .wscript file, return the corresponding Operation
    Line is tab-delimited and looks like
    opcode	arg:value	arg2:value
    """
    line = line.strip()
    # parse until first space
    split = line.split("\t")
    operation = split[0]
    op = globals()[operation]

    kwargs = {}
    for term in split[1:]:
        if ":" not in term:
            print("Error")
            sys.exit(line)
        key, value = term.split(":", 1)

        if key == "arg":
            value = bytes.fromhex(value)
        else:
            try:
                value = int(value, 16)
            except ValueError:
                if value.startswith("["):
                    value = json.loads(value)
        kwargs[key] = value

    try:
        return op(**kwargs)
    except TypeError:
        if "arg" not in kwargs:
            kwargs["arg"] = b""
        return op(**kwargs)


# Text color control codes. The renderer (FUN_0010f560) accepts both the
# 3-byte binary form FF FC XX and the equivalent 3-char ASCII form (#XX);
# we emit the ASCII form for parity with Lost Kefin's DSL style.
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
    Decode a string from the script.
    1. Read `length` bytes and invert each (XOR 0xFF) -- Ys III stores
       script text bitwise-NOT'd in the .bin files.
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


class Operation:
    """
    Generic operation. For most opcodes where we just want to read their argument data
    and keep track of it, this is enough.
    """

    opcode: int
    size: int

    def __init__(self, arg: bytes):
        self.arg = arg

    def to_object(self):
        object = {"name": self.__class__.__name__, "arg": self.arg.hex()}
        if len(self.arg) == 0:
            del object["arg"]
        return object

    def to_bytes(self):
        return self.opcode.to_bytes(1, "little") + self.arg

    def __str__(self):
        object = self.to_object()
        return instruction_to_dsl(object)

    @classmethod
    def from_io(cls, io):
        arg = io.read(cls.size)
        return cls(arg)


class TutorialControls(Operation):
    opcode = 0x00
    size = 0


class EffectA(Operation):
    opcode = 0x01
    size = 1


class EffectAWithWait(Operation):
    opcode = 0x02
    size = 1


class EffectB(Operation):
    opcode = 0x03
    size = 1


class EffectBWithWait(Operation):
    opcode = 0x04
    size = 1


class EffectC(Operation):
    opcode = 0x05
    size = 1


class EffectCWithWait(Operation):
    opcode = 0x06
    size = 1


class EffectD(Operation):
    opcode = 0x07
    size = 1


class EffectDWithWait(Operation):
    opcode = 0x08
    size = 1


class WaitSceneReady(Operation):
    opcode = 0x09
    size = 0


class SceneActionA(Operation):
    opcode = 0x0A
    size = 0


class WaitFrames(Operation):
    opcode = 0x0B
    size = 2


class VNText(Operation):
    opcode = 0x0C

    def __init__(self, character_name: str, text: str):
        self.character_name = character_name
        self.text = text

    def to_object(self):
        return {
            "name": self.__class__.__name__,
            "character_name": self.character_name,
            "text": self.text,
        }

    def to_bytes(self):
        character_id = get_character_index(self.character_name)
        return (
            self.opcode.to_bytes(1, "little")
            + character_id.to_bytes(1, "little")
            + encode_string(self.text)
        )

    @classmethod
    def from_io(cls, io):
        speaker_id = int.from_bytes(io.read(1), "little")
        character_name = get_character_name(speaker_id) or f"Speaker_{speaker_id:02x}"
        s_len = int.from_bytes(io.read(1), "little")
        text = read_string(io, s_len)
        return cls(character_name, text)


class CutsceneText(Operation):
    opcode = 0x0D

    def __init__(self, text: str):
        self.text = text

    def to_object(self):
        return {"name": self.__class__.__name__, "text": self.text}

    def to_bytes(self):
        return self.opcode.to_bytes(1, "little") + encode_string(self.text)

    @classmethod
    def from_io(cls, io):
        s_len = int.from_bytes(io.read(1), "little")
        text = read_string(io, s_len)
        return cls(text)


class PlaceActor(Operation):
    opcode = 0x0E
    size = 6


class MoveCharacter(Operation):
    opcode = 0x0F
    size = 6


class MoveTwoCharacters(Operation):
    opcode = 0x10
    size = 6


class MoveCharactersIndep(Operation):
    opcode = 0x11
    size = 11


class MoveCharacterTo(Operation):
    opcode = 0x12
    size = 6


class ActorAction(Operation):
    opcode = 0x13
    size = 2


class SetActorVisible(Operation):
    opcode = 0x14
    size = 2


class HideActor(Operation):
    opcode = 0x15
    size = 1


class ShowActorEffect(Operation):
    opcode = 0x16
    size = 2


class SetActorField(Operation):
    opcode = 0x17
    size = 5


class ShowPortrait(Operation):
    opcode = 0x18
    size = 4


class HidePortrait(Operation):
    opcode = 0x19
    size = 2


class HideAllPortraits(Operation):
    opcode = 0x1A
    size = 1


class PlaySoundQueue(Operation):
    opcode = 0x1B
    size = 1


class StopAllSound(Operation):
    opcode = 0x1C
    size = 0


class PlaySfx(Operation):
    opcode = 0x1D
    size = 2


class PlayVoice(Operation):
    opcode = 0x1E
    size = 1


class StopVoice(Operation):
    opcode = 0x1F
    size = 0


class SetActorMapPos(Operation):
    opcode = 0x20
    size = 5


class CameraPan(Operation):
    opcode = 0x21
    size = 4


class SpecialCutsceneEvent(Operation):
    opcode = 0x22
    size = 1


class ShowFullscreenImage(Operation):
    opcode = 0x23
    size = 1


class HideFullscreenImage(Operation):
    opcode = 0x24
    size = 0


class SetMapEffect(Operation):
    opcode = 0x25
    size = 3


class NPCReactWithVoice(Operation):
    opcode = 0x26
    size = 1


class NPCReact(Operation):
    opcode = 0x27
    size = 1


class ChangeScene(Operation):
    opcode = 0x28
    size = 1


class CheckFlag(Operation):
    opcode = 0x29
    size = 1


class SetFlag(Operation):
    opcode = 0x2A
    size = 1


class ClearFlag(Operation):
    opcode = 0x2B
    size = 1


class CheckFlag2(Operation):
    opcode = 0x2C
    size = 1


class CheckEvent(Operation):
    opcode = 0x2D
    size = 1


class CheckItem(Operation):
    opcode = 0x2E
    size = 1


class ConditionalRelativeJump(Operation):
    opcode = 0x2F

    # Jump destination = (opcode_position + 1) + target, where target
    # is the raw `skip_len` byte from the script (i.e. relative to the
    # byte just after the opcode).
    def __init__(self, target: int, type: int, arg: int):
        self.target = target
        self.type = type
        self.arg = arg

    def to_object(self):
        return {
            "name": self.__class__.__name__,
            "target": hex(self.target),
            "type": hex(self.type),
            "arg": hex(self.arg),
        }

    def to_bytes(self):
        return (
            self.opcode.to_bytes(1, "little")
            + self.target.to_bytes(1, "little")
            + self.type.to_bytes(1, "little")
            + self.arg.to_bytes(1, "little")
        )

    @classmethod
    def from_io(cls, io):
        target = int.from_bytes(io.read(1), "little")
        type = int.from_bytes(io.read(1), "little")
        arg = int.from_bytes(io.read(1), "little")
        if type not in (0x29, 0x2C, 0x2D, 0x2E, 0x30):
            raise ValueError(f"Unknown conditional jump type {hex(type)}")
        return cls(target, type, arg)


class SkipByte(Operation):
    opcode = 0x30
    size = 1


class UnconditionalJump(Operation):
    opcode = 0x31

    def __init__(self, target_index: int):
        self.target_index = target_index

    def to_object(self):
        return {"name": self.__class__.__name__, "target_index": hex(self.target_index)}

    def to_bytes(self):
        return self.opcode.to_bytes(1, "little") + self.target_index.to_bytes(
            4, "little"
        )

    @classmethod
    def from_io(cls, io):
        target_index = int.from_bytes(io.read(4), "little")
        return cls(target_index)


class EndScript(Operation):
    opcode = 0x32
    size = 0


# 0xFF is a script-block terminator handled directly by the dispatcher,
# not by an opcode handler. We register it here so decompile.py can
# round-trip it -- functionally equivalent to EndScript (0x32).
class EndBlock(Operation):
    opcode = 0xFF
    size = 0


opcodes = {
    0x00: TutorialControls,
    0x01: EffectA,
    0x02: EffectAWithWait,
    0x03: EffectB,
    0x04: EffectBWithWait,
    0x05: EffectC,
    0x06: EffectCWithWait,
    0x07: EffectD,
    0x08: EffectDWithWait,
    0x09: WaitSceneReady,
    0x0A: SceneActionA,
    0x0B: WaitFrames,
    0x0C: VNText,
    0x0D: CutsceneText,
    0x0E: PlaceActor,
    0x0F: MoveCharacter,
    0x10: MoveTwoCharacters,
    0x11: MoveCharactersIndep,
    0x12: MoveCharacterTo,
    0x13: ActorAction,
    0x14: SetActorVisible,
    0x15: HideActor,
    0x16: ShowActorEffect,
    0x17: SetActorField,
    0x18: ShowPortrait,
    0x19: HidePortrait,
    0x1A: HideAllPortraits,
    0x1B: PlaySoundQueue,
    0x1C: StopAllSound,
    0x1D: PlaySfx,
    0x1E: PlayVoice,
    0x1F: StopVoice,
    0x20: SetActorMapPos,
    0x21: CameraPan,
    0x22: SpecialCutsceneEvent,
    0x23: ShowFullscreenImage,
    0x24: HideFullscreenImage,
    0x25: SetMapEffect,
    0x26: NPCReactWithVoice,
    0x27: NPCReact,
    0x28: ChangeScene,
    0x29: CheckFlag,
    0x2A: SetFlag,
    0x2B: ClearFlag,
    0x2C: CheckFlag2,
    0x2D: CheckEvent,
    0x2E: CheckItem,
    0x2F: ConditionalRelativeJump,
    0x30: SkipByte,
    0x31: UnconditionalJump,
    0x32: EndScript,
    0xFF: EndBlock,
}


def bin_to_wscript(bin_file: str, wscript_file: str):
    """
    Convert a .bin file to a .wscript file
    """
    script_indices = []
    script_pointers = []

    fp = open(bin_file, "rb")
    out_fp = open(wscript_file, "w", encoding="utf-8")

    # Parse through absolute pointer table first
    while True:
        if fp.tell() >= 0x800:
            break
        index = int.from_bytes(fp.read(0x4), "little")
        pointer = int.from_bytes(fp.read(0x4), "little")
        script_indices.append(index)
        script_pointers.append(pointer)
        if index == 0:
            break

    fp.seek(0x800)

    relative_pointers = []
    while True:
        current_pointer = fp.tell()

        if (current_pointer - 0x800) in script_pointers:
            i = script_pointers.index(current_pointer - 0x800)
            index = script_indices[i]
            out_fp.write(f"LABEL_{index:06x}:\n")
        if current_pointer in relative_pointers:
            if (current_pointer - 0x800) in script_pointers:
                sys.exit(
                    "Instruction is both a jump target and a script pointer. Everdred needs to handle this apparently"
                )
            idx = relative_pointers.index(current_pointer)
            out_fp.write(f"JMP_{idx:06x}\n")

        op_byte = fp.read(1)

        if op_byte == b"":
            break
        opcode = int.from_bytes(op_byte, "little")

        if opcode not in opcodes:
            raise ValueError(f"Unknown opcode {hex(opcode)}")
        op = opcodes[opcode].from_io(fp)

        if isinstance(op, ConditionalRelativeJump):
            # Destination = (opcode_pos + 1) + skip_len; after from_io reads
            # the 3 inline bytes, fp.tell() == opcode_pos + 4, so we subtract 3.
            jump_target = fp.tell() - 0x3 + op.target
            # Rewrite target to be an index
            op.target = len(relative_pointers)
            relative_pointers.append(jump_target)

        out_fp.write(f"  {str(op)}\n")

    out_fp.close()
    fp.close()
