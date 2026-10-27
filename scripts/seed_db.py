"""
CLI utility to sync or reseed all JSON note fixtures from content/fixtures/
into MongoDB Atlas.
"""
import json
import logging
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from api.core.database import get_mongo_db, in_memory_store, seed_initial_notes
from api.schemas.note import NoteDocument, extract_term_number

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("seed_db")


def seed_database(force_overwrite: bool = False):
    db = get_mongo_db()
    fixtures_dir = project_root / "content" / "fixtures"

    if not fixtures_dir.exists():
        logger.error("Fixtures directory not found: %s", fixtures_dir)
        sys.exit(1)

    json_files = sorted(list(fixtures_dir.rglob("*.json")))
    if not json_files:
        logger.warning("No JSON fixtures found in %s", fixtures_dir)
        return

    logger.info("Found %d fixture files in %s", len(json_files), fixtures_dir)

    synced_count = 0
    errors = 0

    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict) or "note_id" not in data:
                continue

            # Ensure term_number
            if not data.get("term_number"):
                data["term_number"] = extract_term_number(data.get("term", "Term 1"))

            # Validate against schema
            note_obj = NoteDocument(**data)
            note_dict = note_obj.model_dump(by_alias=True)
            clean_id = note_dict["note_id"].lower().strip()

            # Seed in-memory
            in_memory_store.save_note(note_dict)

            # Seed MongoDB Atlas if connected
            if db is not None:
                if force_overwrite:
                    db.notes.update_one(
                        {"note_id": clean_id},
                        {"$set": note_dict},
                        upsert=True
                    )
                else:
                    db.notes.update_one(
                        {"note_id": clean_id},
                        {"$setOnInsert": note_dict},
                        upsert=True
                    )

            synced_count += 1
            logger.info("Synced note: %s (%s - %s)", clean_id, note_dict.get("subject_code"), note_dict.get("title"))
        except Exception as e:
            logger.error("Failed to seed %s: %s", file_path.name, e)
            errors += 1

    target = f"MongoDB Atlas ('{db.name}') & InMemoryStore" if db is not None else "InMemoryStore (offline dev mode)"
    logger.info("Seeding completed! Successfully processed %d notes into %s with %d errors.", synced_count, target, errors)


if __name__ == "__main__":
    force = "--force" in sys.argv or "-f" in sys.argv
    seed_database(force_overwrite=force)
