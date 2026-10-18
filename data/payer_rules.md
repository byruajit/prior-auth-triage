# Synthetic payer rules - prior authorisation (demo only)

R1  MRI lumbar spine: approve only if >= 6 weeks (42 days) of documented
    conservative therapy (physiotherapy or medication). Missing -> Needs info.
R2  Any red flag (history of cancer, new neurological deficit, suspected
    infection) -> Clinician review, regardless of other rules.
R3  CT head: approve if trauma within 48 hours AND GCS documented. Else Needs info.
    "Within 48 hours" is inclusive (0 <= trauma_hours <= 48); negative hours are
    invalid -> Needs info.
R4  Knee arthroscopy: approve only if >= 12 weeks (84 days) of conservative
    therapy AND an MRI report is attached. Else Needs info.
R5  Any procedure not listed above -> Clinician review.
R6  The system NEVER denies. Only a clinician can deny.
