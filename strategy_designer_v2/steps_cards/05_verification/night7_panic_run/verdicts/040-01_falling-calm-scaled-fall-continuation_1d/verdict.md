---
plan: 040-01_falling-calm-scaled-fall-continuation_1d
idea: 040-01_falling-calm-scaled-fall-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean sign-flipped drift-removed 3-bar return after forecast < 0 (grid 0,3,6,...): 0.00914313; t of the mean, day-clustered: 1.93359 (threshold: mean > 0 with day-clustered t >= 2 to confirm; t <= -2 rejects)
- Supporting check: OLS slope of drift-removed 3-bar return on forecast (day-clustered t): 0.000406005, passed: False
- Counts: cases: 632, distinct days: 303
- Decided by: Inconclusive rule: neither the confirm nor the reject rule is met (t between -2 and 2 on a measure, or a failed supporting check).
- Reading: Cases with no close 3 bars later in the same window are left out; the coin's drift is the mean of its non-overlapping 3-bar returns on the 0,3,6,... grid of all its windows; day clustering uses per-day sums of deviations (scores) with a G/(G-1) correction; the slope is fitted on the unflipped drift-removed return with an intercept.
- Size: unusual move +0.58 % (t 1.46, the cases of one day together: 440 days) per case over 3 bars, 0.065 of the coin's usual move (7.96 %); normal drift in its direction -0.39 %, total +0.19 %; 727 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/040-01_falling-calm-scaled-fall-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/040-01_falling-calm-scaled-fall-continuation_1d`
Measure: `measure.py`
