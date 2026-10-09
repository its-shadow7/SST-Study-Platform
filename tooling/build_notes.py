"""
Build-time script to validate and build approved course notes into protected JSON assets.
Reference: Section 6 & 7 of Antigravity Study Platform TDD v1.1
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
FIXTURES_DIR = ROOT_DIR / "content" / "fixtures"
DATA_DIR = ROOT_DIR / "data"
NOTES_OUTPUT_DIR = DATA_DIR / "notes"
WEB_PUBLIC_DATA_DIR = ROOT_DIR / "web" / "public" / "data"

REQUIRED_FIELDS = [
    "schema_version",
    "note_id",
    "term",
    "subject_code",
    "topic_title",
    "tags",
    "learning_objectives",
    "summary",
    "key_takeaways",
    "sections",
    "last_updated",
    "approval_status"
]

def validate_note(note: dict, filepath: Path) -> None:
    for field in REQUIRED_FIELDS:
        if field not in note:
            raise ValueError(f"[{filepath.name}] Missing required field: '{field}'")

    if note["schema_version"] != 1:
        raise ValueError(f"[{filepath.name}] Invalid schema_version: {note['schema_version']}. Expected 1.")

    if not re.match(r"^[a-z0-9-]+$", note["note_id"]):
        raise ValueError(f"[{filepath.name}] Invalid note_id: '{note['note_id']}'. Must be lowercase alphanumeric with hyphens.")

    if note["approval_status"] != "approved":
        raise ValueError(f"[{filepath.name}] Note is not approved (status: '{note['approval_status']}'). Only approved notes can be published.")

    if not isinstance(note["sections"], list) or len(note["sections"]) == 0:
        raise ValueError(f"[{filepath.name}] 'sections' must be a non-empty list.")

    for i, sec in enumerate(note["sections"]):
        for sf in ["section_id", "heading", "body", "citations"]:
            if sf not in sec:
                raise ValueError(f"[{filepath.name}] Section {i} missing field '{sf}'")

def build():
    print("=== Antigravity Note Pipeline Builder ===")
    NOTES_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (WEB_PUBLIC_DATA_DIR / "notes").mkdir(parents=True, exist_ok=True)

    approved_notes = []
    seen_ids = set()

    # Search for json files in fixtures
    fixture_files = sorted(FIXTURES_DIR.glob("*.json"))
    if not fixture_files:
        print("Warning: No fixture notes found in content/fixtures!")
        sys.exit(0)

    for fp in fixture_files:
        with open(fp, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                raise RuntimeError(f"Failed to parse JSON file {fp.name}: {e}")

        validate_note(data, fp)

        note_id = data["note_id"]
        if note_id in seen_ids:
            raise ValueError(f"Duplicate note_id detected: '{note_id}' in {fp.name}")
        seen_ids.add(note_id)

        # Write to protected data/notes/ and web/public/data/notes/
        out_path = NOTES_OUTPUT_DIR / f"{note_id}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        web_out_path = WEB_PUBLIC_DATA_DIR / "notes" / f"{note_id}.json"
        with open(web_out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[OK] Validated and built: {note_id} ({data['subject_code']} - {data['topic_title']})")

        # Build index entry
        approved_notes.append({
            "note_id": data["note_id"],
            "term": data["term"],
            "subject_code": data["subject_code"],
            "topic_title": data["topic_title"],
            "tags": data["tags"],
            "summary": data["summary"],
            "learning_objectives": data["learning_objectives"],
            "last_updated": data["last_updated"]
        })

    # Sort index by subject and topic
    approved_notes.sort(key=lambda x: (x["subject_code"], x["note_id"]))

    # Write notes-index.json to both locations
    index_path = DATA_DIR / "notes-index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(approved_notes, f, indent=2, ensure_ascii=False)

    web_index_path = WEB_PUBLIC_DATA_DIR / "notes-index.json"
    with open(web_index_path, "w", encoding="utf-8") as f:
        json.dump(approved_notes, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Generated search index with {len(approved_notes)} notes at {index_path.name}")
    print("Build completed successfully!")

if __name__ == "__main__":
    build()
