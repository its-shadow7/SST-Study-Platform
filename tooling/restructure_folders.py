import os
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
notes_dir = ROOT / "content" / "notes"
fixtures_dir = ROOT / "content" / "fixtures"

# Mapping of note_id to (term_folder, subject_folder)
structure = {
    "cml-lecture-01-linear-regression": ("term-3", "cml"),
    "cn-lecture-01-introduction": ("term-3", "cn"),
    "cn-lecture-02-packet-switching": ("term-3", "cn"),
    "cn-t5-l01": ("term-5", "computer-networks"),
    "cn-t5-l02": ("term-5", "computer-networks"),
    "cn-t5-l03": ("term-5", "computer-networks"),
}

for nid, (term, sub) in structure.items():
    target_note_dir = notes_dir / term / sub
    target_fix_dir = fixtures_dir / term / sub
    target_note_dir.mkdir(parents=True, exist_ok=True)
    target_fix_dir.mkdir(parents=True, exist_ok=True)

    # 1. Move or copy fixture
    old_fix = fixtures_dir / f"{nid}.json"
    new_fix = target_fix_dir / f"{nid}.json"
    if old_fix.exists():
        shutil.copy2(old_fix, new_fix)
        old_fix.unlink()
        print(f"Moved fixture: {old_fix.name} -> {term}/{sub}/{nid}.json")

    # 2. Move existing markdown or generate markdown from fixture
    old_md = notes_dir / f"{nid}.md"
    new_md = target_note_dir / f"{nid}.md"
    if old_md.exists():
        shutil.copy2(old_md, new_md)
        old_md.unlink()
        print(f"Moved markdown: {old_md.name} -> {term}/{sub}/{nid}.md")
    elif new_fix.exists():
        with open(new_fix, "r", encoding="utf-8") as f:
            data = json.load(f)
        lines = []
        lines.append(f"# {data['topic_title']}")
        lines.append(f"**Term:** {data['term']} | **Subject:** {data['subject_code']} | **Note ID:** `{data['note_id']}`")
        lines.append(f"**Last Updated:** {data['last_updated']}\n")
        lines.append("## Abstract & Summary")
        lines.append(data.get("summary", ""))
        lines.append("\n## Learning Objectives")
        for lo in data.get("learning_objectives", []):
            lines.append(f"- {lo}")
        lines.append("\n## Key Takeaways")
        for kt in data.get("key_takeaways", []):
            lines.append(f"- {kt}")
        lines.append("\n---")
        for sec in data.get("sections", []):
            lines.append(f"\n## {sec.get('heading', '')}")
            lines.append(sec.get("body", ""))
            if sec.get("citations"):
                lines.append("\n**Citations & References:**")
                for c in sec["citations"]:
                    lines.append(f"- {c}")
            lines.append("\n---")
        with open(new_md, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Generated markdown: {term}/{sub}/{nid}.md")

print("Restructure complete!")
