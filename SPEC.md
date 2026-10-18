\# Prior-Authorisation Triage Assistant — Demo Specification



> \*\*Demo safety notice:\*\* This specification uses synthetic payer rules supplied for a software demo. The rules are not clinical guidance, are not validated for care decisions, and must not be used to make real patient decisions.



\## Goal



Build a small Python + Streamlit demonstration that applies the supplied synthetic rules to a request and returns exactly one of three outcomes: \*\*Approve\*\*, \*\*Needs info\*\*, or \*\*Clinician review\*\*. The assistant reports which rule conditions were met or which information is missing. It never denies a request.



\## Users



\- \*\*Demo operator / reviewer:\*\* enters or reviews synthetic request details and the rule result.

\- \*\*Clinician reviewer (represented in the demo):\*\* receives cases routed for clinician review; the demo does not make a denial decision.



This demo is not intended for patients, operational payer workflows, or clinical use.



\## Input data



The demo reads requests from `data/sample\_requests.json`. Each request has these fields:



\- `id`

\- `procedure`

\- `diagnosis`

\- `therapy\_days`

\- `red\_flags` (a list of strings; an empty list means no red flags)

\- `trauma\_hours`

\- `gcs\_documented`

\- `mri\_report`



Procedure names must match the rule names exactly: `MRI lumbar spine`, `CT head`, or `Knee arthroscopy`. Any other procedure name is unlisted under R5. A `therapy\_days` value greater than 0 counts as documented conservative therapy; the supplied procedure rule's duration threshold still applies. Requests and results must be clearly marked as synthetic demo data. Do not include identifying or real patient information.



Red-flag data must distinguish a known empty list from missing, blank, or unknown data. An empty `red\_flags` list means no red flags. Missing, blank, or unknown red-flag data results in \*\*Needs info\*\*, unless another red flag is present, in which case R2 requires \*\*Clinician review\*\*.



\## Outcomes



The application returns exactly one of:



1\. \*\*Clinician review\*\* — A red flag is present, or, when red-flag data is known, the procedure is not listed by the rules.

2\. \*\*Needs info\*\* — A required condition or documentation item is missing, unknown, or not established by the supplied inputs.

3\. \*\*Approve\*\* — The listed procedure’s complete approval conditions are met and `red\_flags` is a known empty list.



There is no Deny outcome or denial action. Apply precedence in this order: \*\*any affirmative red flag → Clinician review; otherwise missing, blank, or unknown red-flag data → Needs info; otherwise unlisted procedure → Clinician review; otherwise evaluate the listed procedure’s approval conditions.\*\*



\## Rule acceptance criteria



\### R1 — MRI lumbar spine



\- Given conservative therapy for \*\*42 days or more\*\*, and no red flag and no unresolved red-flag data, return \*\*Approve\*\*.

\- Given therapy duration under 42 days, return \*\*Needs info\*\*.

\- Given missing or unknown therapy information, return \*\*Needs info\*\*.

\- If a red flag is present, return \*\*Clinician review\*\* regardless of therapy details (R2 takes precedence).



\### R2 — Red flags



\- If any of history of cancer, new neurological deficit, or suspected infection is present, return \*\*Clinician review\*\*, regardless of procedure or other rule conditions.

\- If red-flag data is missing, blank, or unknown, return \*\*Needs info\*\*, unless another red flag is affirmative, in which case return \*\*Clinician review\*\*.

\- Only a known empty `red\_flags` list establishes that there are no red flags and permits evaluation for approval.



\### R3 — CT head



\- Given `trauma\_hours` in the inclusive range \*\*0 <= trauma\_hours <= 48\*\* (an integer or float), documented GCS, and no red flag or unresolved red-flag data, return \*\*Approve\*\*.

\- A negative, NaN, infinite, non-numeric, missing, or otherwise invalid `trauma\_hours` value returns \*\*Needs info\*\*.

\- If valid trauma timing is outside the 48-hour window, or GCS is missing/undocumented, return \*\*Needs info\*\*.

\- If a red flag is present, return \*\*Clinician review\*\* (R2 takes precedence).



\### R4 — Knee arthroscopy



\- Given documented conservative therapy for \*\*84 days or more\*\* and an attached MRI report, and no red flag or unresolved red-flag data, return \*\*Approve\*\*.

\- If therapy duration is under 84 days, therapy information is missing, or the MRI report is not attached/unknown, return \*\*Needs info\*\*.

\- If a red flag is present, return \*\*Clinician review\*\* (R2 takes precedence).



\### R5 — Procedures not listed above



\- For any procedure other than MRI lumbar spine, CT head, or knee arthroscopy, return \*\*Clinician review\*\* when red-flag data is known and no red flag is present.

\- If a red flag is present, return \*\*Clinician review\*\* under R2.

\- If red-flag data is missing, blank, or unknown and no red flag is affirmative, return \*\*Needs info\*\* under the outcome precedence.



\### R6 — No denial



\- The application must never produce a \*\*Deny\*\* result, denial recommendation, or denial action.

\- The only result values available to the interface and rule evaluator are \*\*Approve\*\*, \*\*Needs info\*\*, and \*\*Clinician review\*\*.

\- Missing information must route to \*\*Needs info\*\*, not denial. Only a clinician may deny outside this demo; the demo itself does not support that action.



\## Architecture options



\### Option A — Streamlit UI with a separate pure-Python rule module (chosen)



Keep the Streamlit interface in `app.py` and place explicit rule evaluation in a separate pure-Python module such as `rules.py`. The app reads `data/sample\_requests.json`, passes each request to the evaluator, and displays the outcome and a concise explanation.



\*\*Trade-offs:\*\* The separation makes rules easier to inspect and change independently and supports focused verification of precedence and thresholds. It has modestly more structure than a single-file demo.



\### Option B — Single-file Streamlit demo



Keep JSON loading, Streamlit UI, and rule evaluation together in one Python application file, using explicit ordered condition checks.



\*\*Trade-offs:\*\* Fastest to assemble and easiest to run for a short demo. UI and decision logic are coupled, making later rule changes and focused verification less convenient.



Option A is the selected architecture. Keep rules explicit rather than introducing a general policy engine. Do not add rule behavior beyond R1–R6.



\## Edge cases to handle



1\. A request has both a red flag and a full therapy history; return \*\*Clinician review\*\*, not \*\*Approve\*\*.

2\. A red flag is present while all procedure approval criteria are met; return \*\*Clinician review\*\*.

3\. Red-flag data is missing, blank, or unknown and no affirmative red flag is listed; return \*\*Needs info\*\*, never \*\*Approve\*\*.

4\. Therapy duration is below the applicable threshold; return \*\*Needs info\*\*.

5\. Therapy information is missing or unknown; return \*\*Needs info\*\* for rules requiring that evidence.

6\. CT head `trauma\_hours` is negative, NaN, infinite, non-numeric, missing, or otherwise invalid; return \*\*Needs info\*\*.

7\. CT head trauma timing is valid and within the inclusive 48-hour window, with GCS documented and no red flag or unresolved red-flag data; evaluate for \*\*Approve\*\*.

8\. Knee arthroscopy meets the therapy duration but has no MRI report, or the request is for an unlisted procedure; respectively return \*\*Needs info\*\* or \*\*Clinician review\*\*, never denial.



\## Non-goals



\- \*\*No auto-denial:\*\* the system does not deny, recommend denial, or initiate a denial workflow.

\- \*\*No real patient data:\*\* use synthetic demo inputs only; do not collect or store real patient identifiers or records.

\- \*\*No EHR integration:\*\* no connection to electronic health records, payer systems, claims systems, or external clinical data sources.

\- No clinical guidance, diagnosis, medical necessity determination, or validation of the synthetic rules.

\- No rules beyond R1–R6, and no autonomous clinician decision-making.



\## Demo behavior and presentation



\- Show the single outcome prominently and provide a brief, rule-linked explanation.

\- Identify missing information under \*\*Needs info\*\* without implying denial.

\- For \*\*Clinician review\*\*, indicate whether routing was caused by a red flag or an unlisted procedure, when the available data establishes the reason.

\- Display the synthetic-rules safety notice in the UI and alongside exported/demo results.

\- Do not persist submitted case data beyond what is necessary for the active demo session.

