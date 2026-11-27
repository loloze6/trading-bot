---
plan: 061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade_1d
idea: 061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 5-bar move (minus (5-bar return - coin's normal 5-bar drift)): 0.0247709; t of the mean, cases of the same day taken together: 2.72771 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, top half minus bottom half at median |forecast|: 0.0181231, passed: True
- Counts: cases: 271, days: 205
- Decided by: Mean unusual move above 0 with t >= 2 and the top |forecast| half at least the bottom half: confirm rule.
- Reading: Situation bars are those the engine labelled mean_reversion, with the close-location, 5-day-return and 60-day-return conditions re-checked from prices where the window's bars allow (the 365-day swing percentile cannot be rebuilt inside a window, so the regime label stands for it); a case is the first short bet in each 5-bar grid cell of a window with its 5-bar return from that bet's close; the top half of the split is |forecast| strictly above the median; the plan's 'fewer than 30 cases' rule is applied as 'not observable' per the workflow.
- Size: unusual move +2.48 % (t 2.73, the cases of one day together: 205 days) per case over 5 bars, 0.226 of the coin's usual move (11.68 %); normal drift in its direction -0.65 %, total +1.83 %; 271 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01096 on the check folds against +0.02477 on every fold
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade_1d`
Measure: `measure.py`
