"""Golden tests: the synthetic cases in data/sample_requests.json plus owner-approved cases (see CLAUDE.md)."""

import pytest

import rules

REQUESTS = {r["id"]: r for r in rules.load_requests()}

# Golden cases added by the test owner (not in sample_requests.json).
OWNER_REQUESTS = [
    {"id": "GT-001", "procedure": "MRI lumbar spine", "diagnosis": "M54.50 Low back pain",
     "therapy_days": 21, "red_flags": [], "trauma_hours": None,
     "gcs_documented": False, "mri_report": False},
]
REQUESTS.update({r["id"]: r for r in OWNER_REQUESTS})

# id -> (expected outcome, rule IDs that must be reported), per SPEC.md
EXPECTED = {
    "PA-001": (rules.APPROVE, {"R1"}),
    "PA-002": (rules.NEEDS_INFO, {"R1"}),
    "PA-003": (rules.CLINICIAN_REVIEW, {"R2"}),
    "PA-004": (rules.APPROVE, {"R3"}),
    "PA-005": (rules.NEEDS_INFO, {"R4"}),
    "PA-006": (rules.CLINICIAN_REVIEW, {"R5"}),
    "GT-001": (rules.NEEDS_INFO, {"R1"}),
}


@pytest.mark.parametrize("request_id", sorted(EXPECTED))
def test_golden_case(request_id):
    outcome, rule_ids = EXPECTED[request_id]
    decision = rules.evaluate(REQUESTS[request_id])
    assert decision.outcome in rules.OUTCOMES
    assert decision.outcome == outcome
    assert rule_ids <= set(decision.rule_ids)
