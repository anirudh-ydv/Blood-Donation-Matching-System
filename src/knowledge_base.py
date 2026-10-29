"""
Unit 3 - Knowledge Representation & Reasoning
Facts, rules and a forward-chaining inference engine for donor screening.

Knowledge is stored as:
  * Facts      : ("predicate", donor_id)
  * Horn rules : IF all premises are known facts THEN conclusion is a new fact
"""

# ---- Domain knowledge: antigens present on red cells of each blood group ----
ANTIGENS = {
    "O-": set(),
    "O+": {"Rh"},
    "A-": {"A"},
    "A+": {"A", "Rh"},
    "B-": {"B"},
    "B+": {"B", "Rh"},
    "AB-": {"A", "B"},
    "AB+": {"A", "B", "Rh"},
}

# ---- Eligibility thresholds (configurable; based on common Indian whole-blood
# donation criteria - must always be confirmed by a medical officer) ----
MIN_AGE, MAX_AGE = 18, 65
MIN_WEIGHT_KG = 45
MIN_HEMOGLOBIN = 12.5
MIN_GAP_DAYS = 90


class Rule:
    def __init__(self, name, premises, conclusion):
        self.name = name
        self.premises = premises        # predicate names (same donor)
        self.conclusion = conclusion    # predicate name to derive


# Horn-clause style rules (all variables refer to the same donor d)
RULES = [
    Rule("R1", ["compatible"], "blood_ok"),
    Rule("R2", ["age_ok", "weight_ok", "hb_ok", "gap_ok"], "medically_eligible"),
    Rule("R3", ["blood_ok", "medically_eligible", "available"], "candidate"),
]


def base_facts(donor, recipient_group):
    """Convert one donor record + request into atomic facts."""
    d = donor["donor_id"]
    facts = set()
    # compatibility: donor antigens must be a subset of the recipient's antigens
    if ANTIGENS[donor["blood_group"]] <= ANTIGENS[recipient_group]:
        facts.add(("compatible", d))
    if MIN_AGE <= donor["age"] <= MAX_AGE:
        facts.add(("age_ok", d))
    if donor["weight_kg"] >= MIN_WEIGHT_KG:
        facts.add(("weight_ok", d))
    if donor["hemoglobin"] >= MIN_HEMOGLOBIN:
        facts.add(("hb_ok", d))
    if donor["days_since_last_donation"] >= MIN_GAP_DAYS:
        facts.add(("gap_ok", d))
    if donor["available"] == "yes":
        facts.add(("available", d))
    return facts


def forward_chain(facts):
    """Repeatedly fire rules until no new fact can be derived."""
    facts = set(facts)
    donors = {f[1] for f in facts}
    changed = True
    while changed:
        changed = False
        for rule in RULES:
            for d in donors:
                if (rule.conclusion, d) in facts:
                    continue
                if all((p, d) in facts for p in rule.premises):
                    facts.add((rule.conclusion, d))
                    changed = True
    return facts


def explain(donor, derived_facts):
    """Return the reasons a donor was rejected (explainable reasoning)."""
    d = donor["donor_id"]
    checks = [("compatible", "blood group incompatible"),
              ("age_ok", f"age outside {MIN_AGE}-{MAX_AGE}"),
              ("weight_ok", f"weight below {MIN_WEIGHT_KG} kg"),
              ("hb_ok", f"hemoglobin below {MIN_HEMOGLOBIN} g/dL"),
              ("gap_ok", f"last donation less than {MIN_GAP_DAYS} days ago"),
              ("available", "donor not available")]
    return [msg for pred, msg in checks if (pred, d) not in derived_facts]
