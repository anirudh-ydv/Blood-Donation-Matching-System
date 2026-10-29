"""
Command-line interface for the Intelligent Blood Donation Matching System.
Examples:
  python src/app.py --group A+ --urgency critical --top 3
  python src/app.py --group B- --why          # also show why donors were rejected
  python src/app.py                           # interactive prompt
"""
import argparse
from knowledge_base import ANTIGENS
from matcher import load_donors, match


def main():
    ap = argparse.ArgumentParser(description="Blood donor matching")
    ap.add_argument("--group", help="recipient blood group, e.g. O-")
    ap.add_argument("--urgency", choices=["normal", "critical"], default="normal")
    ap.add_argument("--top", type=int, default=3, help="number of donors to show")
    ap.add_argument("--why", action="store_true", help="show rejection reasons summary")
    args = ap.parse_args()
    if not args.group:
        args.group = input("Recipient blood group (e.g. A+): ").strip().upper()
    if args.group not in ANTIGENS:
        raise SystemExit(f"Unknown blood group '{args.group}'. Use one of: {', '.join(ANTIGENS)}")

    donors = load_donors()
    ranked, n_cand, rejected = match(donors, args.group, args.urgency, args.top)
    print(f"\nRequest: {args.group} | urgency: {args.urgency} | "
          f"eligible donors: {n_cand} of {len(donors)}")
    if not ranked:
        print("No eligible donor found. Escalate to the blood bank.")
    for pos, (d, h) in enumerate(ranked, 1):
        print(f"  #{pos}  {d['donor_id']}  {d['blood_group']:<3}  {d['distance_km']:>5} km  "
              f"last donation {d['days_since_last_donation']:>3} d ago  score h={h}")
    if args.why:
        counts = {}
        for reasons in rejected.values():
            for r in reasons:
                counts[r] = counts.get(r, 0) + 1
        print("\nRejection reasons (a donor can fail more than one check):")
        for r, c in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"  {c:>2} donors: {r}")
    print("\nNote: decision support only - final selection needs medical verification.")


if __name__ == "__main__":
    main()
