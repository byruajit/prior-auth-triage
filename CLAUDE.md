# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A prior-authorisation triage demo that applies **synthetic** payer rules to synthetic requests. Its sources of truth:

- `SPEC.md`: the approved spec. It is stored with Markdown escapes (`\#`, `\*\*`, `\_`), so read it as raw text.
- `data/payer_rules.md`: rules R1–R6.
- `data/sample_requests.json`: the input format and the six demo requests (PA-001…PA-006).

## Project rules

- **Stack:** Python 3, Streamlit for the UI, pytest for tests. Keep the code simple.
- **Architecture:** put the rule logic in a pure-Python module (`rules.py`) that never imports Streamlit. Keep it separate from the Streamlit app (`app.py`). Write the rules as plain, ordered checks, not a policy engine.
- **Business rules come ONLY from `data/payer_rules.md` and `SPEC.md`.** Never invent rules or add behaviour beyond R1–R6.
- **Input format:** `data/sample_requests.json`, exactly as SPEC.md describes it.
- **Synthetic data only.** Never ask for or paste real patient information.
- **Never output "Deny".** The only outcomes are Approve, Needs info and Clinician review. Missing information → Needs info.
- **Every decision must include the rule IDs (R1–R6) that produced it.**
- **Tests:** humans own the golden test set. Write tests ONLY for the cases in `data/sample_requests.json`, with the expected outcomes taken from SPEC.md. Do not invent extra test cases unless explicitly asked.
- **Git:** in this demo, commit directly to `main` unless asked for a branch.
- **Workflow:** work on one task at a time and run the tests after every change.

## Commands

- Run the tests: `python -m pytest -q`
- Run one test: `python -m pytest -q path/to/test_file.py::test_name`
- Run the app: `streamlit run app.py`

## Decision logic

Precedence is strict and applied in this order:
1. Any affirmative red flag (history of cancer, new neurological deficit, suspected infection) → **Clinician review** (R2).
2. Otherwise, red-flag data that is missing, blank or unknown → **Needs info** (R2). Only a known empty list `[]` means "no red flags".
3. Otherwise, a procedure name that is not listed → **Clinician review** (R5). The names must match exactly: `MRI lumbar spine`, `CT head`, `Knee arthroscopy`.
4. Otherwise, apply that procedure's own rule:
   - **R1 MRI lumbar spine:** `therapy_days >= 42` → Approve. Anything else → Needs info.
   - **R3 CT head:** valid `trauma_hours` within 0–48 and `gcs_documented` true → Approve. Anything else → Needs info.
   - **R4 Knee arthroscopy:** `therapy_days >= 84` and `mri_report` attached → Approve. Anything else → Needs info.

Field validation:
- `therapy_days` must be an `int`, not a `bool`. A value above 0 counts as documented therapy, but each rule's day threshold still applies.
- `trauma_hours` must be an `int` or `float`, not a `bool`. The range `0 <= trauma_hours <= 48` is inclusive. Negative, NaN, infinite or non-numeric values are invalid → Needs info.

## Lessons learned

- Every numeric threshold needs owner-approved boundary golden tests: one below, exactly at, and one above. Examples: 41/42/43 days for R1, 83/84/85 days for R4; for R3, 0, 47 and 48 hours → Approve, and 48.5 and -1 → Needs info.
- AI code review must be given SPEC.md, not just the function, to avoid false alarms.

## Presentation

- Show the single outcome prominently, together with the rule IDs and a short explanation.
- Under Needs info, list the missing items without wording that implies denial.
- For Clinician review, say whether a red flag or an unlisted procedure caused the routing.
- Show the synthetic-rules safety notice in the UI and next to any exported results.
- Do not persist case data beyond the active session. No EHR, payer or claims integrations.
