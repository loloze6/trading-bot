---
plan: 032-02.g1.e2.e2_overextended-high-reverses_1d
idea: 032-02.g1.e2.e2_overextended-high-reverses
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of next-5-bar excess return on abs(post_pipeline_value of runup), trending grid bars: -1.27432; OLS slope t: -1.27432 (threshold: confirm if slope t <= -2 with supporting check passing; reject if slope t >= +2; at least 30 independent cases)
- Supporting check: mean excess 5-bar return in the short direction > 0: -0.0167279, passed: False
- Counts: independent cases: 323
- Decided by: The slope t lies between -2 and +2 (inconclusive rule).
- Reading: Situation computed from closes as close >= rolling 28-bar max close of the window (bar t included), using the detector's regime only for the first 27 bars of a window where 28 closes are not available; cases are regime=='trending' bars at grid positions 0,5,10,... of each window with t+5 inside the window, strength = abs(post_pipeline_value) including zeros from the clip, drift = coin's mean non-overlapping 5-bar return over all its windows, slope t from pooled OLS across coins and windows; below 30 cases is reported as 'not observable'.
- Size: unusual move -1.67 % (t -3.05, the cases of one day together: 491 days) per case over 5 bars, -0.149 of the coin's usual move (10.60 %); normal drift in its direction -0.67 %, total -2.34 %; 710 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e2.e2_overextended-high-reverses_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e2.e2_overextended-high-reverses_1d`
Measure: `measure.py`
