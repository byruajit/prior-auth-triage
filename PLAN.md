# Build plan: Prior-Authorisation Triage Demo

The sources of truth are `SPEC.md`, `data/payer_rules.md` and `CLAUDE.md`. The demo uses synthetic data only. It has three outcomes, Approve, Needs info and Clinician review, and never a Deny.

## Golden cases and expected outcomes

These are the only test cases, as `CLAUDE.md` requires. The expected outcomes come from SPEC.md.

| ID | Procedure | Key inputs | Expected outcome | Rule IDs |
|---|---|---|---|---|
| PA-001 | MRI lumbar spine | therapy_days 56, red_flags [] | Approve | R1 |
| PA-002 | MRI lumbar spine | therapy_days 0, red_flags [] | Needs info | R1 |
| PA-003 | MRI lumbar spine | red_flags ["history of cancer"] | Clinician review | R2 |
| PA-004 | CT head | trauma_hours 12, gcs_documented true, red_flags [] | Approve | R3 |
| PA-005 | Knee arthroscopy | therapy_days 90, mri_report false, red_flags [] | Needs info | R4 |
| PA-006 | Cardiac PET scan | unlisted, red_flags [] | Clinician review | R5 |

For every golden case, the tests check three things:
1. the outcome matches the table;
2. the result includes the rule IDs listed in the table;
3. the outcome is one of the three allowed values. This is how R6 is checked.

Each task below adds its rows to a single parametrised test in `tests/test_golden.py`. The rows are read from `data/sample_requests.json` by ID. No case is invented.

## Task 1: Scaffold and R2 red-flag precedence

- **Create:**
  - `requirements.txt` (streamlit, pytest);
  - `rules.py`, which holds:
    - the three outcome constants;
    - an `evaluate(request)` function that returns the outcome, the rule IDs and a short explanation;
    - the R2 checks: an affirmative red flag → Clinician review; red-flag data that is missing, blank or unknown → Needs info;
    - a request loader for `data/sample_requests.json`;
  - `tests/test_golden.py`, with the shared assertions and the PA-003 row.
- **Change:** none.
- **Acceptance:** `python -m pytest -q` passes, with PA-003 → Clinician review [R2].

## Task 2: R5 unlisted procedures

- **Change:**
  - `rules.py`: after R2, a procedure name that doesn't exactly match a listed one → Clinician review, with the reason "unlisted procedure";
  - `tests/test_golden.py`: add the PA-006 row.
- **Create:** none.
- **Acceptance:** `python -m pytest -q` passes, with PA-003 and PA-006 → Clinician review [R5].

## Task 3: R1 MRI lumbar spine

- **Change:**
  - `rules.py`: `therapy_days` must be an int and not a bool, and must be ≥ 42 → Approve. Otherwise Needs info, with the missing or insufficient therapy named;
  - `tests/test_golden.py`: add the PA-001 and PA-002 rows.
- **Create:** none.
- **Acceptance:** `python -m pytest -q` passes, with PA-001 → Approve [R1] and PA-002 → Needs info [R1], and the earlier rows still green.

## Task 4: R3 CT head and R4 knee arthroscopy

- **Change:**
  - `rules.py`, R3: `trauma_hours` must be an int or float, not a bool, and finite, with 0 ≤ h ≤ 48 inclusive, and `gcs_documented` must be true → Approve. Otherwise Needs info, naming what is missing or invalid;
  - `rules.py`, R4: `therapy_days` (an int) must be ≥ 84 and `mri_report` must be attached → Approve. Otherwise Needs info, naming what is missing;
  - `tests/test_golden.py`: add the PA-004 and PA-005 rows.
- **Create:** none.
- **Acceptance:** `python -m pytest -q` passes with all 6 golden cases green.

## Task 5: Streamlit UI

- **Create:** `app.py`. It:
  - shows the safety notice;
  - loads the requests through `rules.py`;
  - lets the user pick a request;
  - shows its synthetic details;
  - shows the outcome prominently, with the rule IDs and an explanation. That explanation names the missing items for Needs info, and says whether a red flag or an unlisted procedure caused a Clinician review.

  `app.py` contains no rule logic and does not persist anything.
- **Change:** none. `rules.py` stays untouched unless a display need shows a gap, and any such change gets its own re-run of the tests.
- **Acceptance:**
  - `python -m pytest -q` still passes all 6 golden cases;
  - a manual smoke test with `streamlit run app.py` shows each of the 6 requests with the expected outcome and the safety notice, and no Deny appears anywhere.

## Notes

- Run `python -m pytest -q` from the repo root so that `rules.py` can be imported without extra configuration.
- `rules.py` must follow every validation rule in SPEC.md, including NaN, infinite and bool inputs and unknown red-flag entries. Only the golden cases above are tested, unless a human asks for more.
- Commit to `main` after each task once its acceptance check passes.
