"""
Ys III - Wanderers from Ys script .bin parser.

Decodes the binary script format into the DSL ("wscript") format and
back. The on-disk layout is:

    0x000..0x800   absolute pointer table (pairs of u32 index, u32 offset),
                   terminated by an index==0 entry.
    0x800..EOF     opcode stream; offsets in the pointer table are
                   relative to 0x800.
"""

import io
import sys
import json

from .characters import get_character_name, get_character_index
from .text import read_string, encode_string


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


class TextBubble(Operation):
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


class GiveItem(Operation):
    opcode = 0x28
    size = 1


class CheckInventory(Operation):
    opcode = 0x29
    size = 1


class SetStoryFlag(Operation):
    opcode = 0x2A
    size = 1


class ClearStoryFlag(Operation):
    opcode = 0x2B
    size = 1


class CheckStoryFlag(Operation):
    opcode = 0x2C
    size = 1


class RandomCheck(Operation):
    opcode = 0x2D
    size = 1


class CheckProgressBit(Operation):
    opcode = 0x2E
    size = 1


class ConditionalRelativeJump(Operation):
    opcode = 0x2F

    # Jump destination = (opcode_position + 1) + target, where target
    # is the raw `skip_len` byte from the script (i.e. relative to the
    # byte just after the opcode). `value` is the argument passed to the
    # check opcode named by `type` (e.g. inventory/story/random/progress id). Named to
    # avoid colliding with the generic Operation.arg (bytes) used by
    # line_to_op when round-tripping wscript back to .bin.
    def __init__(self, target: int, type: int, value: int):
        self.target = target
        self.type = type
        self.value = value

    def to_object(self):
        return {
            "name": self.__class__.__name__,
            "target": hex(self.target),
            "type": hex(self.type),
            "value": hex(self.value),
        }

    def to_bytes(self):
        return (
            self.opcode.to_bytes(1, "little")
            + self.target.to_bytes(1, "little")
            + self.type.to_bytes(1, "little")
            + self.value.to_bytes(1, "little")
        )

    @classmethod
    def from_io(cls, io):
        target = int.from_bytes(io.read(1), "little")
        type = int.from_bytes(io.read(1), "little")
        value = int.from_bytes(io.read(1), "little")
        if type not in (0x29, 0x2C, 0x2D, 0x2E, 0x30):
            raise ValueError(f"Unknown conditional jump type {hex(type)}")
        return cls(target, type, value)


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
    0x0C: TextBubble,
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
    0x28: GiveItem,
    0x29: CheckInventory,
    0x2A: SetStoryFlag,
    0x2B: ClearStoryFlag,
    0x2C: CheckStoryFlag,
    0x2D: RandomCheck,
    0x2E: CheckProgressBit,
    0x2F: ConditionalRelativeJump,
    0x30: SkipByte,
    0x31: UnconditionalJump,
    0x32: EndScript,
    0xFF: EndBlock,
}


def bin_to_wscript(bin: bytes) -> str:
    """
    Convert a binary script to wscript text.
    """
    bin_io = io.BytesIO(bin)
    wscript_io = io.StringIO()
    script_indices = []
    script_pointers = []

    # Parse through absolute pointer table first
    while True:
        if bin_io.tell() >= 0x800:
            break
        index = int.from_bytes(bin_io.read(0x4), "little")
        pointer = int.from_bytes(bin_io.read(0x4), "little")
        script_indices.append(index)
        script_pointers.append(pointer)

    bin_io.seek(0x800)

    relative_pointers = []
    while True:
        current_pointer = bin_io.tell()

        if (current_pointer - 0x800) in script_pointers:
            i = script_pointers.index(current_pointer - 0x800)
            index = script_indices[i]
            wscript_io.write(f"LABEL_{index:06x}:\n")
        if current_pointer in relative_pointers:
            if (current_pointer - 0x800) in script_pointers:
                sys.exit(
                    "Instruction is both a jump target and a script pointer. Everdred needs to handle this apparently"
                )
            idx = relative_pointers.index(current_pointer)
            wscript_io.write(f"JMP_{idx:06x}\n")

        op_byte = bin_io.read(1)

        if op_byte == b"":
            break
        opcode = int.from_bytes(op_byte, "little")

        if opcode not in opcodes:
            raise ValueError(f"Unknown opcode {hex(opcode)}")
        op = opcodes[opcode].from_io(bin_io)

        if isinstance(op, ConditionalRelativeJump):
            # Destination = (opcode_pos + 1) + skip_len; after from_io reads
            # the 3 inline bytes, bin_io.tell() == opcode_pos + 4, so we subtract 3.
            jump_target = bin_io.tell() - 0x3 + op.target
            # Rewrite target to be an index
            op.target = len(relative_pointers)
            relative_pointers.append(jump_target)

        wscript_io.write(f"  {str(op)}\n")

    return wscript_io.getvalue()


def wscript_to_bin(wscript: str) -> bytes:
    """
    Convert wscript text to a binary script.
    """
    ops = []  # list of (offset_in_opcode_stream, operation)
    labels = []  # list of (script_index, offset) in appearance order
    jump_positions = {}  # jump index -> offset (relative to 0x800)

    current_offset = 0
    for line in wscript.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("LABEL_") and stripped.endswith(":"):
            index = int(stripped[len("LABEL_") : -1], 16)
            labels.append((index, current_offset))
            continue
        if stripped.startswith("JMP_"):
            idx = int(stripped[len("JMP_") :], 16)
            jump_positions[idx] = current_offset
            continue
        op = line_to_op(stripped)
        ops.append((current_offset, op))
        current_offset += len(op.to_bytes())

    # Resolve ConditionalRelativeJump targets: jump index -> skip byte.
    for opcode_pos, op in ops:
        if isinstance(op, ConditionalRelativeJump):
            if op.target not in jump_positions:
                raise ValueError(f"Unknown jump index {hex(op.target)}")
            target_offset = jump_positions[op.target]
            skip_len = target_offset - (opcode_pos + 1)
            if not 0 <= skip_len <= 0xFF:
                raise ValueError(
                    f"Skip length {skip_len} out of byte range at offset {hex(opcode_pos)}"
                )
            op.target = skip_len

    # Build pointer table (0x000..0x800). An index==0 entry terminates the
    # table on read, so we only append our own (0, 0) terminator if no
    # index-0 label was already emitted.
    table = bytearray()
    has_terminator = False
    for index, offset in labels:
        table += index.to_bytes(4, "little")
        table += offset.to_bytes(4, "little")
        if index == 0:
            has_terminator = True
    if not has_terminator:
        table += (0).to_bytes(8, "little")

    if len(table) > 0x800:
        raise ValueError(f"Pointer table too large: {len(table)} > 0x800")
    table += b"\x00" * (0x800 - len(table))

    for _, op in ops:
        table += op.to_bytes()
    return bytes(table)
