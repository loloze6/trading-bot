---
plan: 031-01.b1.b2_wide-day-extends-strong-run_1d
idea: 031-01.b1.b2_wide-day-extends-strong-run
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move of long cases (forecast rises >= 2 points, one per 3-bar cell): 0.00171923; t of the mean, cases of one day taken together: 0.759228 (threshold: confirm: mean > 0 with day-clustered t >= 2 and upper-minus-lower half > 0; reject: mean < 0 with t <= -2)
- Supporting check: upper-half minus lower-half mean unusual move (split at median forecast): 0.00463102, passed: True
- Counts: distinct case days: 1164, cases: 2538
- Decided by: The t lies between -2 and 2 (or is not computable): neither confirm nor reject is met.
- Reading: Situation = 5-bar close return > 0 recomputed from prices inside each window (component raw value > 0 on a window's first 5 bars), side long; a case is the first bar in each 3-bar grid cell (from each window's first row) where the positive forecast has risen >= 2 points above its lowest level since the last bet (from 0 after flat); drift is the coin's mean 3-bar return on the same grid over all its windows; t sums case deviations per UTC day; the median split puts cases with forecast above the median in the upper half and the rest in the lower half; fewer than 30 case days gives 'not observable'.
- Size: unusual move +0.17 % (t 0.76, the cases of one day together: 1164 days) per case over 3 bars, 0.019 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.53 %; 2538 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.b2_wide-day-extends-strong-run_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b1.b2_wide-day-extends-strong-run_1d`
Measure: `measure.py`
