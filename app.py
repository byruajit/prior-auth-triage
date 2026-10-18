"""Streamlit UI for the prior-authorisation triage demo. All rule logic lives in rules.py."""

import streamlit as st

import rules

SAFETY_NOTICE = (
    "**Synthetic demo only.** These payer rules are synthetic, are not clinical guidance, "
    "are not validated for care decisions and must not be used for real patient decisions. "
    "This demo never denies a request; only a clinician can deny."
)

st.set_page_config(page_title="Prior-Auth Triage Demo")
st.title("Prior-Authorisation Triage (synthetic demo)")
st.warning(SAFETY_NOTICE)

requests = {r["id"]: r for r in rules.load_requests()}
request_id = st.selectbox("Synthetic request", list(requests))
request = requests[request_id]

st.subheader("Request details (synthetic data)")
st.json(request)

decision = rules.evaluate(request)

st.subheader("Result (synthetic data)")
show = {
    rules.APPROVE: st.success,
    rules.NEEDS_INFO: st.info,
    rules.CLINICIAN_REVIEW: st.info,
}[decision.outcome]
show(f"## {decision.outcome}")
st.markdown(f"**Rule IDs:** {', '.join(decision.rule_ids)}")
st.markdown(f"**Explanation:** {decision.explanation}")
st.caption(SAFETY_NOTICE)
