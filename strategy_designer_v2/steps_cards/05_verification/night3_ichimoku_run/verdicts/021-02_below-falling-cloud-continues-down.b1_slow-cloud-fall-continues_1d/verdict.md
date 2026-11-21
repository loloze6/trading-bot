---
plan: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d
idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 26-bar unusual move (return minus drift, short direction), before costs: 0.015116; t of the mean: 0.689244 (threshold: confirm: mean > 0 with t >= 2; reject: t <= -2)
- Supporting check: slow-fall half minus fast-fall half excess return (26-bar return minus drift): -0.116214, passed: True
- Counts: cases over all coins and windows: 156, slow-fall half: 78, fast-fall half: 78
- Decided by: Inconclusive: the main t lies between -2 and 2 and no reject rule is met.
- Reading: Cases are grid bars (positions 0, 26, 52, ... of each window with a close 26 bars later in the same window) with regime 'trending' and forecast < 0, drift is each coin's mean non-overlapping 26-bar return over all its windows, the slow-fall half is slow_fall raw value strictly above the cases' median (ties go to the fast half), and the plan's 'fewer than 30 cases' is applied as the minimum count.
- Size: unusual move +2.49 % per case over 26 bars, 0.095 of the coin's usual move (25.48 %); normal drift in its direction -4.01 %, total -1.52 %; 191 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d`
Measure: `measure.py`
