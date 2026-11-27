---
plan: 072-03.b1.b1_deep-bounce-fades-more-coins_1d
idea: 072-03.b1.b1_deep-bounce-fades-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (10-day return minus coin drift) x forecast/10 on grid cases: 0.0344493; t of the mean, cases of one day summed: 2.11689 (threshold: confirm: above 0 with t >= 2 (and check passes); reject: below 0 with t <= -2)
- Supporting check: deeper-half minus shallower-half mean 10-day return minus drift (Welch t <= -1): -0.0462355, passed: True
- Counts: distinct case days: 128, cases: 306
- Decided by: the main measure is above 0 with t >= 2 and the supporting check passes (confirm rule)
- Reading: Cases are grid bars (0, 10, 20, ... of each window, with 10 bars ahead inside it) whose recorded regime is mean_reversion, whose close is above the prior close and whose forecast is below 0; the coin's drift is the mean 10-day return over all grid bars of all its windows; the deeper half is |forecast| strictly above the median, the rest the shallower half; the plan's 'fewer than 30 distinct case days' is applied as the minimum count giving 'not observable'.
- Size: unusual move +1.40 % (t 2.19, the cases of one day together: 612 days) per case over 10 bars, 0.079 of the coin's usual move (16.82 %); normal drift in its direction -1.50 %, total -0.10 %; 1131 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (86 cases, 86 days)
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-03.b1.b1_deep-bounce-fades-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-03.b1.b1_deep-bounce-fades-more-coins_1d`
Measure: `measure.py`
