---
plan: 060-01.d1_wide-day-high-close-next-day-fade_1d
idea: 060-01.d1_wide-day-high-close-next-day-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual next-day move in the short's direction: -0.00800085; t of the mean, cases of one day summed: -1.78099 (threshold: above 0 with t >= 2 (and supporting check) to confirm; below 0 with t <= -2 to reject)
- Supporting check: top third minus bottom third of close_loc, mean next-day excess return: -0.028127, passed: True
- Counts: days with cases: 329, cases: 572
- Decided by: The t lies between -2 and 2.
- Reading: Wide is recomputed as (high-low)/close over the std of 20 daily returns (accepting inclusive or exclusive-of-today windows), falling as the 60-bar % change below -10, the agitated percentile (365-day lookback, not rebuildable in the windows) and any part not computable on a window's first bars are taken from the recorded regime not being 'chop'; the per-day t uses deviations summed per day (clustered standard error); thirds are equal splits of the cases sorted by close_loc raw value and the excess return there is unsigned (next-day return minus the coin's mean).
- Size: unusual move -0.52 % (t -1.14, the cases of one day together: 268 days) per case over 1 bars, -0.093 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total -0.65 %; 428 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01.d1_wide-day-high-close-next-day-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.d1_wide-day-high-close-next-day-fade_1d`
Measure: `measure.py`
