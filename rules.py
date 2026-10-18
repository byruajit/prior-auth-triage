"""Rule evaluator for the prior-authorisation triage demo.

SYNTHETIC DEMO ONLY: the rules come from data/payer_rules.md and SPEC.md, are not
clinical guidance and must not be used for real patient decisions.
The evaluator never denies (R6): the only outcomes are the three constants below.
"""

import json
from dataclasses import dataclass
from pathlib import Path

APPROVE = "Approve"
NEEDS_INFO = "Needs info"
CLINICIAN_REVIEW = "Clinician review"
OUTCOMES = (APPROVE, NEEDS_INFO, CLINICIAN_REVIEW)

RED_FLAGS = ("history of cancer", "new neurological deficit", "suspected infection")

MRI_LUMBAR_SPINE = "MRI lumbar spine"
CT_HEAD = "CT head"
KNEE_ARTHROSCOPY = "Knee arthroscopy"
LISTED_PROCEDURES = (MRI_LUMBAR_SPINE, CT_HEAD, KNEE_ARTHROSCOPY)

REQUESTS_PATH = Path(__file__).parent / "data" / "sample_requests.json"


@dataclass(frozen=True)
class Decision:
    outcome: str
    rule_ids: tuple[str, ...]
    explanation: str


def load_requests(path=REQUESTS_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _check_red_flags(red_flags):
    """Split red-flag data into (affirmative flags, unresolved entries).

    Only a known empty list means "no red flags". Missing data, a non-list value,
    or any blank/unrecognised entry is unresolved.
    """
    if not isinstance(red_flags, list):
        return [], ["red_flags data is missing or unknown"]
    affirmative, unresolved = [], []
    for entry in red_flags:
        name = entry.strip().lower() if isinstance(entry, str) else None
        if name in RED_FLAGS:
            affirmative.append(name)
        else:
            unresolved.append(f"red-flag entry {entry!r} is blank or unknown")
    return affirmative, unresolved


def evaluate(request):
    affirmative, unresolved = _check_red_flags(request.get("red_flags"))
    if affirmative:
        return Decision(
            CLINICIAN_REVIEW,
            ("R2",),
            "Routed to clinician review: red flag present (" + ", ".join(affirmative) + ").",
        )
    if unresolved:
        return Decision(
            NEEDS_INFO,
            ("R2",),
            "Needs info: " + "; ".join(unresolved) + ".",
        )
    procedure = request.get("procedure")
    if procedure not in LISTED_PROCEDURES:
        return Decision(
            CLINICIAN_REVIEW,
            ("R5",),
            f"Routed to clinician review: unlisted procedure ({procedure!r}).",
        )
    raise NotImplementedError("procedure rules (R1, R3, R4) are not implemented yet")
