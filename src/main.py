from matcher import load_donors, match

SCENARIOS = [
    ("S1", "O-",  "critical"),
    ("S2", "A+",  "normal"),
    ("S3", "B+",  "critical"),
    ("S4", "AB+", "normal"),
    ("S5", "AB-", "critical"),
    ("S6", "B-",  "normal"),
]

if __name__ == "__main__":
    donors = load_donors()
    print(f"Loaded {len(donors)} donor records\n")
    for sid, group, urgency in SCENARIOS:
        ranked, n_cand, rejected = match(donors, group, urgency, k=3)
        print(f"{sid}: request={group}, urgency={urgency}, "
              f"eligible candidates={n_cand}, rejected={len(rejected)}")
        if not ranked:
            print("   No eligible donor found - escalate to blood bank.")
        for pos, (d, h) in enumerate(ranked, 1):
            print(f"   #{pos} {d['donor_id']}  group={d['blood_group']:<3} "
                  f"dist={d['distance_km']:>4} km  last_don={d['days_since_last_donation']:>3} d  h={h}")
        print()
