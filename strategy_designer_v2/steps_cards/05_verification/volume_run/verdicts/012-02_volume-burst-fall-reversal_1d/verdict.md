---
plan: 012-02_volume-burst-fall-reversal_1d
idea: 012-02_volume-burst-fall-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 3-bar return on raw volume ratio, sharp-fall bars: 0.00431798; OLS t of slope: 1.58575 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 3-bar return of top third by volume ratio > 0: -0.00245463, passed: False
- Counts: kept sharp-fall cases: 440
- Decided by: The slope's t lies between -2 and 2.
- Reading: Kept bars are thinned greedily per window on regime bars before dropping those without a 3-bar forward return inside the window, the coin's mean 3-bar return uses the non-overlapping grid 0,3,6,... pooled over all windows, and the top third is the floor(n/3) cases with the largest volume ratio.
Plan: `steps_cards/03_test_plan/volume_run/plans/012-02_volume-burst-fall-reversal_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/012-02_volume-burst-fall-reversal_1d`
Measure: `measure.py`
