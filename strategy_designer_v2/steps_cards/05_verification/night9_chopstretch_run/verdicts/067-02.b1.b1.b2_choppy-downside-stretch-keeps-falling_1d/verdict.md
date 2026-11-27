---
plan: 067-02.b1.b1.b2_choppy-downside-stretch-keeps-falling_1d
idea: 067-02.b1.b1.b2_choppy-downside-stretch-keeps-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 5-bar move on grid cases with forecast < 0: 0.0103086; t of the mean, cases of each day taken together: 1.702 (threshold: confirm: mean > 0 with t >= 2 and deeper half > shallower half; reject: mean < 0 with t <= -2)
- Supporting check: deeper-half mean minus shallower-half mean (split at median forecast): 0.000208906, passed: True
- Counts: cases: 405, distinct days: 228
- Decided by: The t is between -2 and 2, which the plan calls inconclusive.
- Reading: Choppy is read as the regime 'unknown' (the only regime with a strategy, the choppy profile) and below-average as the raw stretch < 0 (close < SMA20 from prices where it is missing); the day-clustered t sums per-day deviations from the overall mean with a G/(G-1) correction; drift is the coin's mean of 5-bar returns on the same non-overlapping grid over all its windows; the deeper half is forecast <= the median of all cases.
- Size: unusual move +0.60 % (t 1.50, the cases of one day together: 449 days) per case over 5 bars, 0.071 of the coin's usual move (10.60 %); normal drift in its direction -0.57 %, total +0.03 %; 605 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-02.b1.b1.b2_choppy-downside-stretch-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-02.b1.b1.b2_choppy-downside-stretch-keeps-falling_1d`
Measure: `measure.py`
