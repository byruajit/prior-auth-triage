"""Golden tests: only the synthetic cases in data/sample_requests.json (see CLAUDE.md)."""

import pytest

import rules

REQUESTS = {r["id"]: r for r in rules.load_requests()}

# id -> (expected outcome, rule IDs that must be reported), per SPEC.md
EXPECTED = {
    "PA-001": (rules.APPROVE, {"R1"}),
    "PA-002": (rules.NEEDS_INFO, {"R1"}),
    "PA-003": (rules.CLINICIAN_REVIEW, {"R2"}),
    "PA-004": (rules.APPROVE, {"R3"}),
    "PA-005": (rules.NEEDS_INFO, {"R4"}),
    "PA-006": (rules.CLINICIAN_REVIEW, {"R5"}),
}


@pytest.mark.parametrize("request_id", sorted(EXPECTED))
def test_golden_case(request_id):
    outcome, rule_ids = EXPECTED[request_id]
    decision = rules.evaluate(REQUESTS[request_id])
    assert decision.outcome in rules.OUTCOMES
    assert decision.outcome == outcome
    assert rule_ids <= set(decision.rule_ids)
