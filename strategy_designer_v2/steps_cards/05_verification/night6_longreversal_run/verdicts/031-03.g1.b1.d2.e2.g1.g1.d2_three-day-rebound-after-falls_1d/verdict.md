---
plan: 031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls_1d
idea: 031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Pearson correlation of forecast with excess next-3-day return (grid bars): 0.0590885; correlation t: 1.82634 (threshold: t >= 2 (with top-third check and >= 100 grid bars with forecast > 0) to confirm; t <= -2 to reject)
- Supporting check: mean excess 3-day return in top third of forecast > 0 grid bars: 0.0132261, passed: True
- Counts: grid bars with forecast > 0: 436, grid bars: 954
- Decided by: The correlation t is between -2 and 2.
- Reading: The correlation uses all grid bars (positions 0, 3, 6, ... of each window, forecast zero included) with the excess over the mean 3-day grid return of all windows; the top third is the ceil(n/3) positive-forecast grid bars with the largest forecasts; the plan's fewer-than-100 rule is applied as a minimum count, giving 'not observable'.
- Size: unusual move +0.57 % (t 2.08, the cases of one day together: 738 days) per case over 3 bars, 0.075 of the coin's usual move (7.50 %); normal drift in its direction +0.28 %, total +0.84 %; 738 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls_1d`
Measure: `measure.py`
