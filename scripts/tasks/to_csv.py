import csv
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libwanderers.script import line_to_op


def to_csv(wscript_file, csv_file):
    """
    Pull out just the textual operations from a wscript file and save to CSV
    """
    base_filename = os.path.basename(wscript_file)
    wscript_fp = open(wscript_file, "r", encoding="utf-8")
    csv_fp = open(csv_file, "w", newline="", encoding="utf-8")
    writer = csv.writer(csv_fp)
    writer.writerow(
        ["ID", "Block", "Speaker", "JP Text", "EN Text", "Comments", "Text Type"]
    )

    i = 0
    block_index = 0

    for line in wscript_fp.readlines():
        line = line.lstrip().rstrip("\n")
        # Using labels, we can roughly split script files into "blocks"
        # which may make it easier for translators to logically break the
        # script up.
        if "LABEL_" in line:
            block_index += 1
            continue
        if "JMP_" in line:
            continue

        op = line_to_op(line)
        op_type = op.__class__.__name__

        if op_type in [
            "TextBubble",
            "CutsceneText",
        ]:
            text = op.to_object()["text"]
            text = text.replace("\\n", "\n")
            speaker = op.to_object().get("character_name", "").replace("*", "")
            writer.writerow(
                [
                    f"{base_filename}||{i}",
                    block_index,
                    speaker,
                    text,
                    "",
                    "",
                    op_type,
                ]
            )
        i += 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/tasks/to_csv.py <wscript_file> <csv_file>")
        sys.exit(1)
    to_csv(sys.argv[1], sys.argv[2])
