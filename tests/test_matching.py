import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from knowledge_base import ANTIGENS, base_facts, forward_chain
from matcher import load_donors, match
from evaluate import perturbed_weight_sets, top1, distance_only_top1

GROUPS = list(ANTIGENS)


def donor(**kw):
    d = dict(donor_id="T1", blood_group="O-", age=30, weight_kg=70, hemoglobin=14.0,
             distance_km=5.0, available="yes", days_since_last_donation=200)
    d.update(kw)
    return d


class TestCompatibility(unittest.TestCase):
    def test_total_compatible_pairs_is_27(self):
        n = sum(ANTIGENS[d] <= ANTIGENS[r] for d in GROUPS for r in GROUPS)
        self.assertEqual(n, 27)

    def test_o_negative_is_universal_donor(self):
        self.assertTrue(all(ANTIGENS["O-"] <= ANTIGENS[r] for r in GROUPS))

    def test_ab_positive_is_universal_recipient(self):
        self.assertTrue(all(ANTIGENS[d] <= ANTIGENS["AB+"] for d in GROUPS))

    def test_rh_positive_cannot_give_rh_negative(self):
        self.assertFalse(ANTIGENS["A+"] <= ANTIGENS["A-"])


class TestEligibility(unittest.TestCase):
    def run_rules(self, d, group="O-"):
        return ("candidate", d["donor_id"]) in forward_chain(base_facts(d, group))

    def test_valid_donor_is_candidate(self):
        self.assertTrue(self.run_rules(donor()))

    def test_underage_rejected(self):
        self.assertFalse(self.run_rules(donor(age=17)))

    def test_low_weight_rejected(self):
        self.assertFalse(self.run_rules(donor(weight_kg=44)))

    def test_low_hemoglobin_rejected(self):
        self.assertFalse(self.run_rules(donor(hemoglobin=12.4)))

    def test_recent_donation_rejected(self):
        self.assertFalse(self.run_rules(donor(days_since_last_donation=89)))

    def test_unavailable_rejected(self):
        self.assertFalse(self.run_rules(donor(available="no")))


class TestRanking(unittest.TestCase):
    def test_closer_donor_ranks_first(self):
        near = donor(donor_id="N", blood_group="A+", distance_km=2)
        far = donor(donor_id="F", blood_group="A+", distance_km=25)
        ranked, _, _ = match([far, near], "A+", "critical", k=2)
        self.assertEqual(ranked[0][0]["donor_id"], "N")

    def test_exact_match_preferred_over_o_negative(self):
        exact = donor(donor_id="E", blood_group="B+", distance_km=10)
        uni = donor(donor_id="U", blood_group="O-", distance_km=10)
        ranked, _, _ = match([uni, exact], "B+", "normal", k=2)
        self.assertEqual(ranked[0][0]["donor_id"], "E")

    def test_no_candidate_returns_empty(self):
        ranked, n, _ = match([donor(available="no")], "O-")
        self.assertEqual((ranked, n), ([], 0))

    def test_dataset_never_returns_ineligible_donor(self):
        donors = load_donors()
        for g in GROUPS:
            ranked, _, _ = match(donors, g, "critical", k=40)
            for d, _h in ranked:
                self.assertTrue(ANTIGENS[d["blood_group"]] <= ANTIGENS[g])
                self.assertEqual(d["available"], "yes")
                self.assertGreaterEqual(d["hemoglobin"], 12.5)


class TestEvaluation(unittest.TestCase):
    def test_perturbed_weights_sum_to_one(self):
        for urg, w in perturbed_weight_sets():
            self.assertAlmostEqual(sum(w[urg].values()), 1.0)

    def test_twelve_weight_variants(self):
        self.assertEqual(len(perturbed_weight_sets()), 12)

    def test_heuristic_avoids_scarce_o_negative_when_other_donor_exists(self):
        donors = load_donors()
        self.assertEqual(distance_only_top1(donors, "A-", "normal"), "D035")
        self.assertNotEqual(top1(donors, "A-", "normal"), "D035")


if __name__ == "__main__":
    unittest.main(verbosity=2)
