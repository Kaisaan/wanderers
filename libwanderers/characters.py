"""
Character names mapping from the game script format.
Index corresponds to the hexadecimal values used in TextBubble speaker_id.

Source: the speaker nameplate table g_apSpeakerNameplates at vaddr
0x0022d5d0 in SLPM_625.32 -- a 32-entry array of pointers to Shift-JIS
name strings. Speaker IDs >= 0x20 are not in that table; those speakers
only appear in the speaker-relative dialog path (no nameplate drawn).

Per-line comments also include the internal ASCII asset name from the
sprite-asset string table at vaddr 0x0025b0a8 where one exists. Two
notable reveals: Gardner's internal name is "garland" (the original
Japanese romanization), and Adonis's is "pierre".
"""

CHARACTERS = [
    "Adol",                # 0x00 アドル
    "Dogi",                # 0x01 ドギ            / dogi
    "Garland",             # 0x02 ガードナー      / garland
    "Elena",               # 0x03 エレナ          / elena
    "Granny Aida",         # 0x04 アイーダ婆さん
    "Town Girl A",         # 0x05 街娘
    "Town Man A",          # 0x06 街男
    "Town Man B",          # 0x07 街男
    "Cynthia",             # 0x08 シンシア
    "Town Man C",          # 0x09 街男
    "Adonis",              # 0x0A アドニス        / pierre
    "Town Girl B",         # 0x0B 街娘
    "Miner A",             # 0x0C 坑夫           / miner_a
    "Chester",             # 0x0D チェスター      / chester
    "Soldier in Uniform",  # 0x0E 軍服の男        / guardman
    "Dewey",               # 0x0F デューイ        / dewey
    "Edgar",               # 0x10 エドガー        / edgar
    "Priest",              # 0x11 神父
    "Lord",                # 0x12 城主
    "Miner B",             # 0x13 坑夫            / t_miner_a
    "Miner C",             # 0x14 坑夫            / t_miner_b
    "Miner D",             # 0x15 坑夫            / t_miner_c
    "Miner E",             # 0x16 坑夫            / miner_e
    "McGuire",             # 0x17 マクガイア      / mcguire
    "Master",              # 0x18 師匠            / master
    "Bob",                 # 0x19 ボブ            / bob
    "Town Man D",          # 0x1A 街男
    "Town Man E",          # 0x1B 街男
    "Town Man F",          # 0x1C 街男
    "Town Girl C",         # 0x1D 街娘
    "Town Girl D",         # 0x1E 街娘
    "Soldier",             # 0x1F 兵士            / soldier
    "Unknown 1",           # 0x20 (no nameplate)
    "Unknown 2",           # 0x21 (no nameplate)
    "Fortune-teller",      # 0x22
]


def get_character_name(index):
    if isinstance(index, str):
        try:
            index = int(index, 16)
        except ValueError:
            return None

    if 0 <= index < len(CHARACTERS):
        return CHARACTERS[index]
    return None


def get_character_index(name):
    if name.startswith("Speaker_"):
        return int(name[len("Speaker_"):], 16)
    return CHARACTERS.index(name)
