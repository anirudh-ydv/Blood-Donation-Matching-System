"""
Unit 2 + Unit 3 - Best First Search over screened candidate donors.
Lower heuristic value h(n) = better donor.
"""
import heapq

# Heuristic weights for normal and critical requests
WEIGHTS = {
    "normal":   {"distance": 0.40, "match": 0.35, "rest": 0.25},
    "critical": {"distance": 0.65, "match": 0.20, "rest": 0.15},
}
MAX_DISTANCE_KM = 30.0
REST_TARGET_DAYS = 180   # donors rested >= this get zero rest-penalty


def heuristic(donor, recipient_group, urgency, weights=None):
    w = (weights or WEIGHTS)[urgency]
    dist = min(donor["distance_km"] / MAX_DISTANCE_KM, 1.0)
    # exact group match preferred; universal donor O- given to other groups is
    # penalised more so scarce O- stock is conserved
    if donor["blood_group"] == recipient_group:
        match = 0.0
    elif donor["blood_group"] == "O-":
        match = 1.0
    else:
        match = 0.5
    rest = max(0.0, 1 - donor["days_since_last_donation"] / REST_TARGET_DAYS)
    return round(w["distance"] * dist + w["match"] * match + w["rest"] * rest, 4)


def best_first_search(candidates, recipient_group, urgency="normal", k=5, weights=None):
    """Greedy Best First Search: frontier is a priority queue ordered by h(n)."""
    frontier = []
    for i, d in enumerate(candidates):
        heapq.heappush(frontier, (heuristic(d, recipient_group, urgency, weights), i, d))
    ranked = []
    while frontier and len(ranked) < k:
        h, _, d = heapq.heappop(frontier)   # expand most promising node
        ranked.append((d, h))
    return ranked
