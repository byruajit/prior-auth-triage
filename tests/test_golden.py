"""Golden tests: only the synthetic cases in data/sample_requests.json (see CLAUDE.md)."""

import pytest

import rules

REQUESTS = {r["id"]: r for r in rules.load_requests()}

# id -> (expected outcome, rule IDs that must be reported), per SPEC.md
EXPECTED = {
    "PA-003": (rules.CLINICIAN_REVIEW, {"R2"}),
}


@pytest.mark.parametrize("request_id", sorted(EXPECTED))
def test_golden_case(request_id):
    outcome, rule_ids = EXPECTED[request_id]
    decision = rules.evaluate(REQUESTS[request_id])
    assert decision.outcome in rules.OUTCOMES
    assert decision.outcome == outcome
    assert rule_ids <= set(decision.rule_ids)
