---
plan: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h
idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction
fit: adapted
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-adjusted 48-bar move signed by forecast (Monday bets): 0.00365823; t of the mean: 1.95155 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move above minus below median |forecast|: 0.00315257, passed: True
- Counts: cases: 1686
- Decided by: t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Cases are the Monday 00:00 bars (stamped Sunday 23:00) with |forecast| >= the 2-point band, i.e. the workflow's bets; returns are positional close[t+48]/close[t]-1 inside the window; the normal drift is the coin's mean 48-bar return on the 0,48,96,... grid of all its windows; cases at exactly the median |forecast| are left out of both halves; the plan's 'fewer than 100 cases' minimum is treated as 'not observable'.
- Size: unusual move +0.37 % per case over 48 bars, 0.052 of the coin's usual move (6.56 %); normal drift in its direction +0.03 %, total +0.40 %; 1687 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h`
Measure: `measure.py`
