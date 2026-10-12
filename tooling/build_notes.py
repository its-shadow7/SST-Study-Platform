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
from typing import Optional, Set

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

DISALLOWED_SCHEMES_REGEX = re.compile(r"^(javascript|data|vbscript|file):", re.IGNORECASE)
MARKDOWN_LINK_REGEX = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
HTML_LINK_REGEX = re.compile(r"""<a\s+(?:[^>]*?\s+)?href=["']([^"']+)["']""", re.IGNORECASE)
INTERNAL_NOTE_REF_REGEX = re.compile(r"(?:/notes/|/term/[^/]+/[^/]+/|note:)([a-z0-9-]+)", re.IGNORECASE)

def validate_note(note: dict, filepath: Path, all_note_ids: Optional[set] = None) -> None:
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

        # 1. Non-empty citations validation
        if not isinstance(sec["citations"], list) or len(sec["citations"]) == 0:
            raise ValueError(f"[{filepath.name}] Section {i} ('{sec['section_id']}') must have a non-empty list of citations.")

        for c_idx, citation in enumerate(sec["citations"]):
            if not isinstance(citation, str) or not citation.strip():
                raise ValueError(
                    f"[{filepath.name}] Section {i} ('{sec['section_id']}') citation index {c_idx} is empty or whitespace."
                )

        # 2. Markdown & HTML link protocol validation
        body = sec.get("body", "")
        if not isinstance(body, str) or not body.strip():
            raise ValueError(f"[{filepath.name}] Section {i} ('{sec['section_id']}') body must be non-empty text.")

        md_links = [m[1].strip() for m in MARKDOWN_LINK_REGEX.findall(body)]
        html_links = [h.strip() for h in HTML_LINK_REGEX.findall(body)]
        all_links = md_links + html_links

        for link_target in all_links:
            # Strip anchors or query strings for protocol check
            url_no_query = link_target.split("?")[0].split("#")[0].strip()

            if DISALLOWED_SCHEMES_REGEX.match(link_target):
                raise ValueError(
                    f"[{filepath.name}] Section {i} contains forbidden link protocol in '{link_target}'. Unsafe schemes are blocked."
                )

            is_relative = link_target.startswith(("/", "#", "./", "../"))
            is_valid_absolute = link_target.startswith(("https://", "http://", "mailto:"))

            if not (is_relative or is_valid_absolute):
                raise ValueError(
                    f"[{filepath.name}] Section {i} contains invalid link destination '{link_target}'. "
                    f"Links must use https://, http://, mailto:, or relative paths (/ or #)."
                )

            # 3. Inter-note cross-reference validation
            if all_note_ids is not None:
                note_ref_match = INTERNAL_NOTE_REF_REGEX.search(link_target)
                if note_ref_match:
                    target_note_id = note_ref_match.group(1).lower()
                    if target_note_id not in all_note_ids:
                        raise ValueError(
                            f"[{filepath.name}] Broken inter-note reference: '{link_target}' refers to "
                            f"unknown note_id '{target_note_id}'. Must exist in manifest."
                        )

def build():
    print("=== SST Note Pipeline Builder ===")
    NOTES_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (WEB_PUBLIC_DATA_DIR / "notes").mkdir(parents=True, exist_ok=True)

    fixture_files = sorted(FIXTURES_DIR.glob("*.json"))
    if not fixture_files:
        print("Warning: No fixture notes found in content/fixtures!")
        sys.exit(0)

    # Pass 1: Collect and verify all fixture note IDs
    all_fixture_ids = set()
    raw_fixtures = []
    for fp in fixture_files:
        with open(fp, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                raise RuntimeError(f"Failed to parse JSON file {fp.name}: {e}")
            raw_fixtures.append((data, fp))
            nid = data.get("note_id")
            if nid:
                if nid in all_fixture_ids:
                    raise ValueError(f"Duplicate note_id detected: '{nid}' in {fp.name}")
                all_fixture_ids.add(nid)

    # Pass 2: Comprehensive validation & asset generation
    approved_notes = []
    for data, fp in raw_fixtures:
        validate_note(data, fp, all_fixture_ids)
        note_id = data["note_id"]

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
