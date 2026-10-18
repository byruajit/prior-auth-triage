---
name: add-payer-rule
description: Add a new payer rule to the prior-auth triage assistant, spec-first, with golden tests
---
1. Add the rule with the next free ID to data/payer_rules.md and SPEC.md first.
2. Implement it in the rule module (see CLAUDE.md). Never output "Deny"; keep the evaluation order (R2 first).
3. Add golden test cases (owner-approved) for every outcome the rule can produce, inline in tests/test_golden.py.
4. Run python -m pytest -q and report a one-line result.
5. Update the Streamlit app only if a new field is needed.
