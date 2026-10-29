# Intelligent Blood Donation Matching System

AI project (Course: Artificial Intelligence, CCSAI0301) - B.Tech CSE, NIET Greater Noida.
Supports **SDG 3 - Good Health and Well-Being**.

The system finds and ranks suitable blood donors for a blood request using rule-based
reasoning and heuristic search.

| Course concept | Where it is used |
|---|---|
| Problem formulation / state space (Unit 1) | Donor records form the search space (`src/matcher.py`) |
| Constraint filtering, heuristic, Best First Search (Unit 2) | `src/search.py` |
| Knowledge representation, rules, forward chaining (Unit 3) | `src/knowledge_base.py` |

## Project structure
```
data/donors.csv          synthetic sample dataset (40 donors, random seed 42)
src/knowledge_base.py    antigen knowledge, rules R1-R3, forward chaining, rejection reasons
src/search.py            heuristic function + Best First Search
src/matcher.py           data loading + end-to-end matching pipeline
src/main.py              runs 6 sample blood-request scenarios
src/app.py               command-line interface (group, urgency, top-k, rejection reasons)
src/evaluate.py          weight-sensitivity analysis + distance-only baseline comparison
web/index.html           working website (single file, same logic as the Python code)
tests/test_matching.py   17 unit tests
```

## Website
Open `web/index.html` in any browser (no install, no server). Tabs: Find donors, Donor database,
Compatibility, Evaluation, How it works. To host it free, enable GitHub Pages for the `web/` folder.

## Run (Python)
```
python src/main.py
python src/app.py --group A+ --urgency critical --top 3 --why
python src/evaluate.py
python -m unittest discover -s tests -v
```
Requires Python 3.8+ (standard library only).

## Workflow
Blood Request -> Facts -> Forward Chaining (rules R1-R3) -> Candidate Donors ->
Heuristic Evaluation -> Best First Search -> Ranked Donor List

## Important notes
* The dataset is **synthetic** (randomly generated); it contains no real donor data.
* Eligibility thresholds (age 18-65, weight >= 45 kg, Hb >= 12.5 g/dL, gap >= 90 days)
  are configurable in `knowledge_base.py`; heuristic weights are configurable in `search.py`.
* Decision-support prototype only. Final donor selection and cross-matching must be done
  by qualified medical staff.

## Team (Group 2)
Anjali, Anirudh Yadav, Anil Singh, Ankit Singh, Ankur Chaudhari - Faculty: Dr. Mohd Nazim
