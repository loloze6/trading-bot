---
plan: 061-01.b1.b1.b1.d1.d1.d1.d3_moderate-fall-high-close-fades_1d
idea: 061-01.b1.b1.b1.d1.d1.d1.d3_moderate-fall-high-close-fades
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 5-bar move per case: 0.0326046; t of the mean, cases of one day taken together: 2.7497 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2)
- Supporting check: larger-|forecast| half minus smaller half, mean unusual move: 0.0312569, passed: True
- Counts: cases: 77, distinct days: 72
- Decided by: Mean short-direction unusual move above 0 with t >= 2 and the supporting check above 0.
- Reading: Profile taken from the recorded regime (its volatility percentile cannot be rebuilt from the recorded bars) with ret5, ret20, ret60 and close location recomputed from prices where the window has the history; a case is the first short bet (rise of |forecast| >= 2) in each 5-bar grid cell of a window with a full 5-bar return in that window; 'fewer than 30 cases on fewer than 20 distinct days' read as not observable if either count is short; the median split puts |forecast| above the median in the larger half and the rest in the smaller half.
- Size: unusual move +3.26 % (t 2.77, the cases of one day together: 72 days) per case over 5 bars, 0.275 of the coin's usual move (11.68 %); normal drift in its direction -0.70 %, total +2.56 %; 77 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (61 cases, 56 days)
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d1.d1.d3_moderate-fall-high-close-fades_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d1.d1.d3_moderate-fall-high-close-fades_1d`
Measure: `measure.py`
