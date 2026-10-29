# Intelligent Blood Donation Matching System

Rule-based screening + heuristic Best First Search · AI project · demo on synthetic data

Recipient blood group Urgency Show top

Decision-support prototype using synthetic data. Final donor selection and cross-matching must be confirmed by qualified medical staff.

## Add a donor

Blood groupAge Weight (kg)Hemoglobin (g/dL) Distance (km)Days since last donation Available

Donors you add are kept in this browser only. A value of 999 days means no recent donation on record.

Filter by blood group

## Red-cell compatibility (donor → recipient)

A ✓ means the donor’s antigens are a subset of the recipient’s. The column of the selected recipient group is outlined.

## Evaluation of the heuristic

Each weight is changed by ±0.10 (12 variants) for all 16 requests (8 blood groups × 2 urgency levels), and the result is compared with a distance-only ranking. It runs live on the current donor list.

## How it works

**Pipeline:** Blood request → donor facts → forward chaining (rules R1–R3) → eligible donors → heuristic score h → Best First Search (priority queue) → ranked list with reasons.

### Knowledge base (Unit 3)

`R1` compatible(d) → blood_ok(d)\
`R2` age_ok ∧ weight_ok ∧ hb_ok ∧ gap_ok → medically_eligible(d)\
`R3` blood_ok ∧ medically_eligible ∧ available → candidate(d)

Thresholds (NBTC donor-selection guidance): age 18–65, weight ≥ 45 kg (350 ml collection), hemoglobin ≥ 12.5 g/dL, at least 90 days since the last donation.

### Heuristic and search (Units 1–2)

`h = wd·(km/30) + wm·match + wr·max(0, 1 − days/180)` — lower is better.\
Weights (distance / match / rest): normal 0.40 / 0.35 / 0.25; critical 0.65 / 0.20 / 0.15. Match = 0 for the same group, 0.5 for another compatible group, 1 when scarce O− would be used for a different group.