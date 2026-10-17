"""
Pipeline builder for Term 5 CML Lecture 1.
Validates constraints:
- Zero personal instructor names
- Exactly 25 questions with progressive difficulty (easy -> medium -> hard) and mix of single/multi correct
- Rich Markdown source generation in content/notes/term-5/cml/cml-t5-l01.md
- JSON fixture generation in content/fixtures/term-5/cml/cml-t5-l01.json
- Runs build_notes.py to update data/ and web/public/data/
"""

import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONTENT_NOTES_DIR = ROOT_DIR / "content" / "notes" / "term-5" / "cml"
FIXTURES_DIR = ROOT_DIR / "content" / "fixtures" / "term-5" / "cml"

from data_cml_l1 import L1_DATA

FORBIDDEN_NAMES = [
    re.compile(r"\bayush\b", re.IGNORECASE),
    re.compile(r"\bkshitij\b", re.IGNORECASE),
    re.compile(r"\bchitwan\b", re.IGNORECASE)
]

def assert_zero_forbidden_names(obj, context=""):
    if isinstance(obj, str):
        for pattern in FORBIDDEN_NAMES:
            if pattern.search(obj):
                raise ValueError(f"FORBIDDEN NAME DETECTED in {context}: '{pattern.pattern}' found in text: {obj[:120]}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            assert_zero_forbidden_names(v, f"{context}->{k}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            assert_zero_forbidden_names(item, f"{context}[{idx}]")

def validate_quiz(quiz_data, note_id):
    questions = quiz_data.get("questions", [])
    if len(questions) != 25:
        raise ValueError(f"[{note_id}] Expected exactly 25 questions, got {len(questions)}")
    
    diff_order = {"easy": 1, "medium": 2, "hard": 3}
    last_val = 1
    single_count = 0
    multi_count = 0
    
    for q in questions:
        q_id = q["id"]
        q_diff = q["difficulty"]
        q_type = q["type"]
        val = diff_order.get(q_diff, 0)
        if val < last_val:
            raise ValueError(f"[{note_id}] Difficulty regression at question {q_id}: went from {last_val} to {val}")
        last_val = val
        
        if q_type == "single_choice":
            single_count += 1
            if len(q["correctOptionIds"]) != 1:
                raise ValueError(f"[{note_id}] {q_id}: single_choice must have exactly 1 correct option, got {len(q['correctOptionIds'])}")
        elif q_type == "multiple_choice":
            multi_count += 1
            if len(q["correctOptionIds"]) < 1:
                raise ValueError(f"[{note_id}] {q_id}: multiple_choice must have at least 1 correct option")
        else:
            raise ValueError(f"[{note_id}] {q_id}: Invalid question type '{q_type}'")
            
        opt_ids = {opt["id"] for opt in q["options"]}
        for cid in q["correctOptionIds"]:
            if cid not in opt_ids:
                raise ValueError(f"[{note_id}] {q_id}: correctOptionId '{cid}' not found in options {opt_ids}")
                
    print(f"[{note_id}] Quiz verified: {len(questions)} questions ({single_count} single-choice, {multi_count} multi-choice). Strict progressive difficulty satisfied.")

def json_to_markdown(note):
    md = []
    md.append(f"# {note['topic_title']}")
    md.append(f"**Term:** {note['term']} | **Subject:** {note['subject_code']} | **Note ID:** `{note['note_id']}`")
    md.append(f"**Last Updated:** {note['last_updated']}\n")
    
    md.append("## Abstract & Summary")
    md.append(note["summary"])
    md.append("")
    
    md.append("## Learning Objectives")
    for obj in note["learning_objectives"]:
        md.append(f"- {obj}")
    md.append("")
    
    md.append("## Key Takeaways")
    for kt in note["key_takeaways"]:
        md.append(f"- {kt}")
    md.append("")
    
    md.append("---")
    md.append("")
    
    for sec in note["sections"]:
        md.append(f"## {sec['heading']}")
        md.append(sec["body"])
        md.append("")
        if sec.get("citations"):
            md.append("**Citations & References:**")
            for c in sec["citations"]:
                md.append(f"- {c}")
            md.append("")
        md.append("---")
        md.append("")
        
    return "\n".join(md)

def run():
    print("=== Term 5 CML (L1) Pipeline Builder & Validator ===")
    CONTENT_NOTES_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    
    note = L1_DATA
    nid = note["note_id"]
    print(f"\n--- Processing {nid} ---")
    
    # 1. Strict zero forbidden names check
    assert_zero_forbidden_names(note, context=nid)
    print(f"[{nid}] Constraint PASSED: 0 occurrences of forbidden instructor names.")
    
    # 2. Validate Quiz structure and progressive difficulty
    validate_quiz(note["quiz"], nid)
    
    # 3. Write Markdown representation
    md_content = json_to_markdown(note)
    md_path = CONTENT_NOTES_DIR / f"{nid}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[{nid}] Generated Markdown source at content/notes/term-5/cml/{nid}.md ({len(md_content)} chars)")
    
    # 4. Write JSON fixture
    json_path = FIXTURES_DIR / f"{nid}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(note, f, indent=2, ensure_ascii=False)
    print(f"[{nid}] Generated JSON fixture at content/fixtures/term-5/cml/{nid}.json")

    print("\nAll CML L1 assets generated successfully in content/fixtures!")
    
    # 5. Execute build_notes to sync all assets to data/ and web/public/data/
    import build_notes
    build_notes.build()

if __name__ == "__main__":
    run()
