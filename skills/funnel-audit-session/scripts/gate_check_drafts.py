#!/usr/bin/env python3
"""
Gate-check email drafts against Haytham's voice rules.

Run with: python3 scripts/gate_check_drafts.py
Or invoke from execute_code with a list of (subject, body) tuples.

Checks (in order, fail fast on any):
  1. Em-dash (U+2014) anywhere — absolute rule
  2. Kill list (lowercase substring match)
  3. Operator vocabulary (word boundary, allow "email" for leak description)
  4. Sentence-start capitalization (allow numbers, quotes, em-dash)
  5. Word count <= 100 (configurable)
  6. Subject: <= 8 words, no end punctuation, not all caps
  7. "clients" / "leads" (use parents/moms/families)
  8. Multiple questions (should be exactly 1)

Returns a dict per variant: {"words": N, "issues": [...], "pass": bool}.

False positives to ignore:
  - "CAPS" warning when a sentence starts with a digit (e.g. "11,500 followers")
  - The script's capitalization check is overly strict on numeric openers
"""

import re
import sys

KILL_LIST = [
    "stuck with me", "sitting with me", "sat with me", "stayed with me",
    "that's real", "love that energy", "love that", "love this",
    "i noticed", "i wanted to reach out", "hope this finds you well",
    "no strings attached", "no worries if not", "no pressure",
    "just checking in", "quick question", "i came across your profile",
    "love what you're doing", "i noticed something",
    "free audit", "audit for coaches",
]

OPERATOR_VOCAB = [
    "funnel", "email sequence", "email capture", "opt-in",
    "conversion", "optimize", "audit",
    # "email" alone is allowed — needed to describe the leak
    # "sequence" alone is too generic; keep it scoped to "email sequence"
]

REPLACED_WORDS = ["clients", "leads"]  # use parents/moms/families

MAX_BODY_WORDS = 100
MAX_SUBJECT_WORDS = 8


def gate_check(subject: str, body: str) -> dict:
    issues = []

    # 1. Em-dash
    if "\u2014" in subject or "\u2014" in body:
        issues.append("EM-DASH present")

    # 2. Kill list
    body_lower = body.lower()
    for k in KILL_LIST:
        if k in body_lower:
            issues.append(f"KILL LIST: '{k}'")

    # 3. Operator vocabulary
    for v in OPERATOR_VOCAB:
        if re.search(r"\b" + re.escape(v) + r"\b", body_lower):
            issues.append(f"OPERATOR VOCAL: '{v}'")

    # 4. Capitalization (with false-positive guard for digits/quotes)
    sentences = re.split(r'(?<=[.!?])\s+', body.strip())
    for s in sentences:
        if not s:
            continue
        first = s[0]
        if first.isupper() or first in "0123456789\"'\u2014\n":
            continue
        issues.append(f"NOT CAPITALIZED: '{s[:60]}'")

    # 5. Word count
    words = len(body.split())
    if words > MAX_BODY_WORDS:
        issues.append(f"WORD COUNT: {words} > {MAX_BODY_WORDS}")

    # 6. Subject
    subj_words = len(subject.split())
    if subj_words > MAX_SUBJECT_WORDS:
        issues.append(f"SUBJECT WORDS: {subj_words} > {MAX_SUBJECT_WORDS}")
    if subject.endswith((".", "!", "?")):
        issues.append("SUBJECT ENDS WITH PUNCTUATION")
    if subject.isupper():
        issues.append("SUBJECT ALL CAPS")

    # 7. Replaced words
    for w in REPLACED_WORDS:
        if re.search(r"\b" + w + r"\b", body_lower):
            issues.append(f"REPLACED: '{w}' (use parents/moms/families)")

    # 8. Multiple questions
    questions = [s for s in sentences if "?" in s]
    if len(questions) > 1:
        issues.append(f"MULTIPLE QUESTIONS: {len(questions)}")

    return {"words": words, "subject_words": subj_words, "issues": issues, "pass": not issues}


def main():
    """Read (subject, body) pairs from stdin, one per line: SUBJECT\\nBODY\\n---\\n"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(__doc__)
        return
    print("Use from execute_code or import gate_check() directly.")
    print("Example:")
    print("  from gate_check_drafts import gate_check")
    print('  result = gate_check("the regulated parent", "Hi Roisin,\\n\\n...")')


if __name__ == "__main__":
    main()
