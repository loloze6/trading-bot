# Exercises 9, 10 and 11: "not observable" (the same file is in exercise_9)

**Change** (approved). A plan's minimum counts are applied first: if any minimum count of cases the plan states is not reached, the status is **not observable** (the data could not show the idea), whatever the other numbers. **Inconclusive** is kept for results with enough cases that meet neither the confirm nor the reject rule. It is a count against a number fixed before the data, so the two can be told apart without any judgement after the data.

**Exercises 9 and 10: the fixed inputs, run twice side by side.** The 29 daily plans of `03_test_plan/plans/` (13 with a record). Cost 1.11 and 1.12 USD. No code refusal.
- The same status for all 13 plans in both runs: inconclusive.
- **Right:** every plan reached its minimum counts (for example 001-01: 60 cases, 30 needed; 002-05: 5 up-cross stretches, 3 needed), so none is "not observable".
- The 14 refusals give "no verdict", as before.

**Exercise 11: the new path, on purpose.** Two real records cut to one window of one coin (`exercise_11/records/`, not market evidence), two runs:
- 001-01: 3 extreme cases, 30 needed: **not observable**, both runs.
- 002-05: 13 in-stretch bars, 100 needed: **not observable**, both runs.

**Status.** "Done when" is met (exercises 9 and 10), and the new status is reached when it should be (exercise 11).
