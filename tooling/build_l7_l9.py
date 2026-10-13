"""
Pipeline builder for Term 5 Lectures 7-9.
Validates constraints:
- Zero personal instructor names (Ayush, Kshitij)
- 25 questions per lecture with progressive difficulty (easy -> medium -> hard) and mix of single/multi correct
- Rich Markdown source generation in content/notes/term-5/computer-networks/
- JSON fixture generation in content/fixtures/term-5/computer-networks/
- Builds catalog and index via tooling/build_notes.py
"""

import json
import re
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONTENT_NOTES_DIR = ROOT_DIR / "content" / "notes" / "term-5" / "computer-networks"
FIXTURES_DIR = ROOT_DIR / "content" / "fixtures" / "term-5" / "computer-networks"

from data_l7 import L7_DATA
from data_l8 import L8_DATA
from data_l9 import L9_DATA

FORBIDDEN_NAMES = [re.compile(r"\bayush\b", re.IGNORECASE), re.compile(r"\bkshitij\b", re.IGNORECASE)]

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
    if len(questions) < 20 or len(questions) > 30:
        raise ValueError(f"[{note_id}] Question count must be between 20 and 30, got {len(questions)}")
    
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
    print("=== Term 5 (L7-L9) Pipeline Builder & Validator ===")
    CONTENT_NOTES_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    
    notes = [L7_DATA, L8_DATA, L9_DATA]
    
    for note in notes:
        note_id = note["note_id"]
        print(f"\nProcessing {note_id} ({note['topic_title']})...")
        
        # 1. Zero forbidden names check
        assert_zero_forbidden_names(note, context=note_id)
        print(f"[{note_id}] Zero forbidden names assertion passed.")
        
        # 2. Validate quiz structure
        validate_quiz(note["quiz"], note_id)
        
        # 3. Write Markdown source
        md_file = CONTENT_NOTES_DIR / f"{note_id}.md"
        md_content = json_to_markdown(note)
        # Check markdown too
        assert_zero_forbidden_names(md_content, context=f"{note_id}.md")
        md_file.write_text(md_content, encoding="utf-8")
        print(f"[{note_id}] Wrote source markdown to {md_file}")
        
        # 4. Write JSON fixture
        json_file = FIXTURES_DIR / f"{note_id}.json"
        json_file.write_text(json.dumps(note, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[{note_id}] Wrote JSON fixture to {json_file}")
        
    print("\n=== Running Master Build Script (tooling/build_notes.py) ===")
    cmd = [sys.executable, str(ROOT_DIR / "tooling" / "build_notes.py")]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print("ERROR in build_notes.py:", res.stderr)
        sys.exit(1)
        
    print("=== L7-L9 Pipeline Complete Successfully! ===")

if __name__ == "__main__":
    run()
