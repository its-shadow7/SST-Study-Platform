import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

index_path = ROOT / "web" / "public" / "data" / "notes-index.json"
with open(index_path, "r", encoding="utf-8") as f:
    index = json.load(f)

cml_notes = [n for n in index if n["subject_code"] == "CML" and n["term"] == "Term 5"]
print(f"Term 5 CML notes found in public index: {len(cml_notes)}")
for n in cml_notes:
    print(f"  • {n['note_id']}: {n['topic_title']}")

for nid in ["cml-t5-l01", "cml-t5-l02"]:
    note_path = ROOT / "web" / "public" / "data" / "notes" / f"{nid}.json"
    assert note_path.exists(), f"Missing {note_path}"
    with open(note_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"\n[VERIFIED] {nid}:")
    print(f"  Title: {data['topic_title']}")
    print(f"  Sections ({len(data['sections'])}):")
    for s in data["sections"]:
        print(f"    - {s['heading']} ({len(s['body'])} chars)")
    print(f"  Quiz: {len(data['quiz']['questions'])} questions")
    diffs = [q['difficulty'] for q in data['quiz']['questions']]
    print(f"  Difficulty breakdown: {diffs.count('easy')} Easy, {diffs.count('medium')} Medium, {diffs.count('hard')} Hard")
