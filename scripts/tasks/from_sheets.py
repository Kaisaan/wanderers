# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-api-python-client",
#     "google-auth",
# ]
# ///

"""
Pull latest translations from Google Sheets and apply them to wscript files.
"""

import csv
import os
import sys
import tempfile
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tasks.from_csv import from_csv
from tasks.update_asm import generate_asm

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/spreadsheets",
]

SPREADSHEET_ID = "10h_j4RCCrUQtMjdgoMcrJcWS6CIDrvKm5Dv0k0JE2iY"
TL_SHEET = "TL"
SECRET_FILE = "wanderers_secret.json"
EXPECTED_HEADER = ["ID", "Block", "Speaker", "JP Text", "EN Text"]


def get_rows(service, sheet):
    range_name = f"{sheet}!A:Z"
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, range=range_name)
        .execute()
    )
    return result.get("values", [])


def from_sheets(wscript_dir: str = "decompiled"):
    if not os.path.exists(SECRET_FILE):
        sys.exit(
            f"{SECRET_FILE} not found. Make sure it's in the wanderers folder."
        )

    if not os.path.isdir(wscript_dir):
        sys.exit(f"Directory {wscript_dir} does not exist")

    credentials = service_account.Credentials.from_service_account_file(
        SECRET_FILE, scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=credentials)

    rows = get_rows(service, TL_SHEET)
    if not rows:
        sys.exit(f"No rows fetched from '{TL_SHEET}' sheet")

    header = rows[0]
    if header[: len(EXPECTED_HEADER)] != EXPECTED_HEADER:
        print(header)
        sys.exit(
            "Header does not match expected: " + ",".join(EXPECTED_HEADER)
        )

    rows_by_file: dict[str, list[list[str]]] = {}
    for row in rows[1:]:
        if not row or not row[0]:
            continue
        id_parts = row[0].split("||")
        if len(id_parts) < 2:
            continue
        rows_by_file.setdefault(id_parts[0], []).append(row)

    with tempfile.TemporaryDirectory() as tmp:
        for wscript_filename, stage_rows in sorted(rows_by_file.items()):
            wscript_path = Path(wscript_dir) / wscript_filename
            if not wscript_path.exists():
                print(f"  {wscript_path} missing; skipping")
                continue

            csv_path = Path(tmp) / f"{Path(wscript_filename).stem}.csv"
            with csv_path.open("w", newline="", encoding="utf-8") as fp:
                writer = csv.writer(fp)
                writer.writerow(header)
                writer.writerows(stage_rows)

            print(f"Applying sheet translations to {wscript_path}")
            from_csv(str(wscript_path), str(csv_path), str(wscript_path))
    
    print("Generating strings.asm...")
    asm_rows = get_rows(service, "SLPM")
    generate_asm(Path("asm/strings.asm"), asm_rows)


if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "decompiled"
    from_sheets(target_dir)
