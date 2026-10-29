"""
Evaluation: (a) weight sensitivity of the heuristic ranking and
(b) comparison with a distance-only baseline, over 8 blood groups x 2 urgency levels.
"""
import copy
from knowledge_base import ANTIGENS
from search import WEIGHTS
from matcher import load_donors, match


def perturbed_weight_sets():
    """+/-0.10 on each weight of each profile, renormalised to sum to 1."""
    sets = []
    for urg in WEIGHTS:
        for key in WEIGHTS[urg]:
            for delta in (+0.10, -0.10):
                w = copy.deepcopy(WEIGHTS)
                w[urg][key] = max(0.0, w[urg][key] + delta)
                total = sum(w[urg].values())
                w[urg] = {k: v / total for k, v in w[urg].items()}
                sets.append((urg, w))
    return sets


def top1(donors, group, urgency, weights=None):
    ranked, _, _ = match(donors, group, urgency, 1, weights)
    return ranked[0][0]["donor_id"] if ranked else None


def distance_only_top1(donors, group, urgency):
    ranked, _, _ = match(donors, group, urgency, 100)
    return min(ranked, key=lambda x: x[0]["distance_km"])[0]["donor_id"] if ranked else None


if __name__ == "__main__":
    donors = load_donors()
    variants = perturbed_weight_sets()
    requests = [(g, u) for g in ANTIGENS for u in WEIGHTS]
    stable = same_base = solved = 0
    print(f"{'request':<14}{'cands':>6}  {'top-1':<6}{'stable':>8}  {'dist-only':<10}")
    for g, u in requests:
        _, n, _ = match(donors, g, u, 1)
        base = top1(donors, g, u)
        if base is None:
            print(f"{g+' '+u:<14}{n:>6}  {'none':<6}"); continue
        solved += 1
        runs = [top1(donors, g, u, w) for urg, w in variants if urg == u]
        frac = sum(r == base for r in runs) / len(runs)
        dist = distance_only_top1(donors, g, u)
        stable += frac; same_base += (dist == base)
        print(f"{g+' '+u:<14}{n:>6}  {base:<6}{frac:>8.0%}  {dist:<10}")
    print(f"\nRequests with at least one eligible donor: {solved} of {len(requests)}")
    print(f"Mean top-1 stability under +/-0.10 weight changes: {stable/solved:.0%}")
    print(f"Heuristic top-1 equals distance-only top-1 in {same_base} of {solved} requests")
