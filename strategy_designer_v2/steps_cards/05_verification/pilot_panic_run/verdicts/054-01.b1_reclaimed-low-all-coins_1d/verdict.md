---
plan: 054-01.b1_reclaimed-low-all-coins_1d
idea: 054-01.b1_reclaimed-low-all-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-day return of long bets over the coin's mean 5-day return: 0.0243447; t of the mean, deviations summed per day: 1.28668 (threshold: confirm: mean > 0 with t >= 2 and deeper-minus-shallower > 0; reject: mean < 0 with t <= -2)
- Supporting check: deeper-half minus shallower-half mean excess 5-day return (split at median forecast) (Welch t 1.530): 0.0312832, passed: True
- Counts: cases: 148, distinct days: 67, cases in deeper half: 74
- Decided by: The t of the mean excess 5-day return lies between -2 and 2 (or its sign disagrees with the mean), meeting neither rule.
- Reading: Situation = a reclaimed pierce of the prior 30-day low (recorded pierce_depth raw value > 0, recomputed from prices where not recorded) on a bar the detector sent to mean_reversion (the regime column carries the falling-agitated profile vetoes, whose 60-bar trend and 365-bar volatility percentile cannot be rebuilt inside a window), expected side long; a case is a forecast rise of at least 2 points from its lowest positive level since the last bet (from 0 after a flat), the first in each 5-bar grid cell of its window; the coin's mean 5-day return is taken on the non-overlapping grid of all its windows; the day-clustered t uses per-day sums of deviations with a G/(G-1) correction; the deeper half is forecast above the median, the shallower half at or below it; the plan's 'fewer than 30 cases or 25 days' rule is reported as 'not observable'.
- Size: unusual move +2.43 % (t 1.30, the cases of one day together: 67 days) per case over 5 bars, 0.208 of the coin's usual move (11.68 %); normal drift in its direction +0.72 %, total +3.16 %; 148 cases
Plan: `steps_cards/03_test_plan/pilot_panic_run/plans/054-01.b1_reclaimed-low-all-coins_1d.md`
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-01.b1_reclaimed-low-all-coins_1d`
Measure: `measure.py`
