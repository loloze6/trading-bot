---
plan: 031-03_uprun-size-scales-wide-flat-reversal_1d
idea: 031-03_uprun-size-scales-wide-flat-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move in the short direction after a bet: -0.0134535; t of the mean, cases of one day taken together: -1.00259 (threshold: confirm: mean > 0 with day-clustered t >= 2 (and check passes); reject: t <= -2)
- Supporting check: mean unusual move above-median |forecast| minus below-median: -0.0337037, passed: False
- Counts: cases: 78, distinct days: 68
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: A bet is a fall of the forecast at least 2 points below its lowest short level since the last bet (from 0 after a flat), the first bet of each 5-bar grid cell per window is the case; the drift is each coin's mean non-overlapping 5-bar return over all its windows; the t uses day-clustered errors with a G/(G-1) correction; above-median means |forecast| strictly above the median, below-median the rest; the plan's 30-case and 30-day minimums are applied as 'not observable'.
- Size: unusual move -1.35 % (t -1.01, the cases of one day together: 68 days) per case over 5 bars, -0.124 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total -1.94 %; 78 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-03_uprun-size-scales-wide-flat-reversal_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-03_uprun-size-scales-wide-flat-reversal_1d`
Measure: `measure.py`
