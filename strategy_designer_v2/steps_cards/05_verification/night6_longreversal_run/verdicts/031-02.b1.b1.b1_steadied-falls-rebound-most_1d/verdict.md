---
plan: 031-02.b1.b1.b1_steadied-falls-rebound-most_1d
idea: 031-02.b1.b1.b1_steadied-falls-rebound-most
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 30-bar forward excess return on forecast, regime mean_reversion, non-overlapping 30-bar grid: -0.00417528; OLS slope t: -1.32522 (threshold: confirm: slope t >= 2 with supporting check positive and >= 40 cases; reject: slope t <= -2)
- Supporting check: mean excess return forecast>0 minus forecast<0: -0.101782, passed: False
- Counts: cases: 89, cases forecast > 0: 19, cases forecast < 0: 70, active bars: 3113
- Decided by: The slope's t is between -2 and 2.
- Reading: The regime detector's r90 component is not recorded and cannot be rebuilt from ~122-bar windows (it needs 90+365 bars), so the situation is read from the detector's own `regime` == mean_reversion and the expected side is the sign of the 30-day return (ret30 last_history_value, else recomputed from closes); the grid is rows 0, 30, 60, ... of each window, all regime bars on it with a forward return are cases (forecast 0 included in the regression), the coin's mean 30-bar return is the mean over the same grid of all its windows and all regimes, and the plan's 40-case minimum is applied as 'not observable'.
- Size: unusual move +0.89 % (t 0.26, the cases of one day together: 110 days) per case over 30 bars, 0.040 of the coin's usual move (29.32 %); normal drift in its direction -2.66 %, total -1.77 %; 180 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-02.b1.b1.b1_steadied-falls-rebound-most_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b1.b1.b1_steadied-falls-rebound-most_1d`
Measure: `measure.py`
