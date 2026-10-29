import csv
import os
from knowledge_base import base_facts, forward_chain, explain
from search import best_first_search

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "donors.csv")


def load_donors(path=DEFAULT_PATH):
    donors = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            r["age"] = int(r["age"]); r["weight_kg"] = int(r["weight_kg"])
            r["hemoglobin"] = float(r["hemoglobin"])
            r["distance_km"] = float(r["distance_km"])
            r["days_since_last_donation"] = int(r["days_since_last_donation"])
            donors.append(r)
    return donors


def match(donors, recipient_group, urgency="normal", k=5, weights=None):
    facts = set()
    for d in donors:
        facts |= base_facts(d, recipient_group)
    derived = forward_chain(facts)
    candidates = [d for d in donors if ("candidate", d["donor_id"]) in derived]
    rejected = {d["donor_id"]: explain(d, derived)
                for d in donors if ("candidate", d["donor_id"]) not in derived}
    ranked = best_first_search(candidates, recipient_group, urgency, k, weights)
    return ranked, len(candidates), rejected
