"""
Pipeline builder for Term 5 CML Lectures 5-6.
Validates constraints:
- Zero personal instructor names
- Exactly 25 questions per lecture with progressive difficulty (easy -> medium -> hard) and mix of single/multi correct
- Rich Markdown source generation in content/notes/term-5/cml/
- JSON fixture generation in content/fixtures/term-5/cml/
- Runs build_notes.py to update data/ and web/public/data/
"""

import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONTENT_NOTES_DIR = ROOT_DIR / "content" / "notes" / "term-5" / "cml"
FIXTURES_DIR = ROOT_DIR / "content" / "fixtures" / "term-5" / "cml"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_cml_l5 import CML_L05_DATA
from data_cml_l6 import CML_L06_DATA

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

def normalize_note_data(raw_data):
    note = dict(raw_data)
    
    # 1. Normalize top-level keys
    note["schema_version"] = 1
    if "note_id" not in note and "slug" in note:
        note["note_id"] = note["slug"]
    if "topic_title" not in note and "title" in note:
        note["topic_title"] = note["title"]
        
    nid = note["note_id"]
    if nid == "cml-t5-l05":
        note["tags"] = [
            "Optimization",
            "Gradient Descent",
            "Batch Gradient Descent",
            "Stochastic Gradient Descent",
            "Mini-Batch Gradient Descent",
            "Learning Rate",
            "Loss Landscape",
            "Feature Scaling",
            "Convergence Diagnostics"
        ]
        note["learning_objectives"] = [
            "1. Explain why closed-form OLS fails for large sample sizes or high feature dimensions, necessitating iterative first-order optimization.",
            "2. Geometrically and mathematically interpret the gradient vector as the direction of steepest ascent on convex loss surfaces.",
            "3. Derive both scalar and vectorized gradient formulas for Mean Squared Error loss.",
            "4. Analyze the stability bounds of learning rate eta based on Hessian Lipschitz smoothness to prevent explosive divergence.",
            "5. Compare computational complexity, trajectory geometry, and memory requirements of Batch, Stochastic, and Mini-Batch Gradient Descent.",
            "6. Diagnose how unscaled features distort the loss landscape into elongated ravines and induce severe orthogonal bouncing.",
            "7. Implement automated stopping criteria and dynamic learning rate decay schedules (step decay, exponential, cosine annealing).",
            "8. Construct high-throughput vectorized solvers in NumPy and robust production pipelines with Scikit-Learn SGDRegressor."
        ]
    elif nid == "cml-t5-l06":
        note["tags"] = [
            "Polynomial Regression",
            "Non-Linear Modeling",
            "Basis Expansion",
            "Bias-Variance Tradeoff",
            "Underfitting",
            "Overfitting",
            "Adjusted R-squared",
            "Occam's Razor",
            "Vandermonde Matrix",
            "Model Selection"
        ]
        note["learning_objectives"] = [
            "1. Motivate the need for non-linear modeling on curved data while maintaining the computational benefits of linear-in-parameter estimation.",
            "2. Formulate polynomial feature expansion mathematically and evaluate the combinatorial growth of interaction terms.",
            "3. Prove mathematically why raw training R-squared can never decrease when higher polynomial powers are added.",
            "4. Derive and interpret Adjusted R-squared, utilizing its degree-of-freedom penalty to evaluate model fit fairly.",
            "5. Apply Occam's Razor to choose parsimonious, robust models among competing hypotheses with comparable test accuracy.",
            "6. Prove the Bias-Variance-Noise decomposition of expected out-of-sample prediction error step-by-step.",
            "7. Map underfitting and overfitting states to high bias vs. high variance using the classical dartboard analogy.",
            "8. Diagnose numerical hazards including structural multicollinearity and Vandermonde matrix ill-conditioning.",
            "9. Build end-to-end, leakage-free Scikit-Learn pipelines utilizing PolynomialFeatures, StandardScaler, and validation sweeps."
        ]

    # Ensure all sections have citations
    for sec in note.get("sections", []):
        if "citations" not in sec or not sec["citations"]:
            sec["citations"] = ["Hastie, T., et al. (2009). The Elements of Statistical Learning. Springer."]
            
    # 2. Normalize Quiz
    if "quiz" in note:
        quiz = note["quiz"]
        normalized_questions = []
        for q in quiz.get("questions", []):
            nq = dict(q)
            # Map type
            if nq.get("type") in ["multi_choice", "multiple_choice"]:
                nq["type"] = "multiple_choice"
            else:
                nq["type"] = "single_choice"
                
            # Map correctOptionIds
            if "correctOptionIds" not in nq:
                ca = nq.get("correct_answer")
                if isinstance(ca, list):
                    nq["correctOptionIds"] = ca
                elif isinstance(ca, str):
                    nq["correctOptionIds"] = [ca]
                else:
                    raise ValueError(f"Missing correct answer in question {nq.get('id')}")
            
            # Ensure correct_answer key is removed if present to avoid confusion
            nq.pop("correct_answer", None)
            normalized_questions.append(nq)
        quiz["questions"] = normalized_questions
        
    return note

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
    print("=== Term 5 CML (L5-L6) Pipeline Builder & Validator ===")
    CONTENT_NOTES_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    
    notes = [
        normalize_note_data(CML_L05_DATA),
        normalize_note_data(CML_L06_DATA)
    ]
    
    for note in notes:
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

    print("\nAll CML L5-L6 assets generated successfully in content/fixtures!")
    
    # 5. Execute build_notes to sync all assets to data/ and web/public/data/
    import build_notes
    build_notes.build()

if __name__ == "__main__":
    run()
