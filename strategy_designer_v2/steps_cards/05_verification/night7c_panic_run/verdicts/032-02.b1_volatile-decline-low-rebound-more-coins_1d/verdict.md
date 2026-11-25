---
plan: 032-02.b1_volatile-decline-low-rebound-more-coins_1d
idea: 032-02.b1_volatile-decline-low-rebound-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar unusual move of long cases (return minus normal 5-bar drift): -0.0059838; t of the mean, cases summed per day: -0.212479 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: least-squares slope of per-case unusual move on forecast: 0.00861822, passed: True
- Counts: cases: 64, distinct days: 31
- Decided by: t lies between -2 and 2.
- Reading: Situation = regime 'mean_reversion' cross-checked with price-based 30-bar return and recorded depth; a case is a forecast rise of at least 2 above its lowest long level since the last bet (from 0 after a flat), the first per 5-bar grid cell from each window's first row, dropped if its 5-bar return leaves the window; the drift is each coin's mean grid 5-bar return over all its windows; t uses per-day summed deviations with a D/(D-1) factor; the plan's 'fewer is inconclusive' minimum is reported as 'not observable'.
- Size: unusual move -0.60 % (t -0.22, the cases of one day together: 31 days) per case over 5 bars, -0.036 of the coin's usual move (11.68 %); normal drift in its direction +0.82 %, total +0.22 %; 64 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b1_volatile-decline-low-rebound-more-coins_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b1_volatile-decline-low-rebound-more-coins_1d`
Measure: `measure.py`
