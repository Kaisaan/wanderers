import csv
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from libwanderers.script import line_to_op
from libwanderers.text import fix_ascii


def from_csv(wscript_file, csv_file, out_wscript_file):
    """
    Apply EN translations from a CSV back into a wscript file. Rows whose
    EN Text column is non-empty replace the original text for that
    instruction; other lines pass through unchanged.
    """
    base_filename = os.path.basename(wscript_file)

    translations = {}
    with open(csv_file, "r", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            id_parts = row["ID"].split("||")
            if len(id_parts) < 2 or id_parts[0] != base_filename:
                continue
            en = row["EN Text"]
            if not en:
                continue
            translations[int(id_parts[1])] = en

    with open(wscript_file, "r", encoding="utf-8") as fp:
        lines = fp.readlines()

    out = []
    i = 0
    for line in lines:
        stripped = line.lstrip().rstrip("\n")
        if "LABEL_" in stripped:
            out.append(line)
            continue
        if "JMP_" in stripped:
            out.append(line)
            continue

        if i in translations:
            op = line_to_op(stripped)
            if op.__class__.__name__ in ("TextBubble", "CutsceneText"):
                op.text = fix_ascii(translations[i]).replace("\n", "\\n")
                out.append(f"  {str(op)}\n")
            else:
                out.append(line)
        else:
            out.append(line)
        i += 1

    with open(out_wscript_file, "w", encoding="utf-8") as fp:
        fp.writelines(out)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python scripts/tasks/from_csv.py <wscript_file> <csv_file> <out_wscript_file>"
        )
        sys.exit(1)
    from_csv(sys.argv[1], sys.argv[2], sys.argv[3])
