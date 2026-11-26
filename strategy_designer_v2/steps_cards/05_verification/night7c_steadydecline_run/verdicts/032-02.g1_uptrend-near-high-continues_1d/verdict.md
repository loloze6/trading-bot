---
plan: 032-02.g1_uptrend-near-high-continues_1d
idea: 032-02.g1_uptrend-near-high-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope t of 5-bar forward excess return on forecast, in-regime non-overlapping grid: 0.000675807; OLS slope t: 1.65271 (threshold: confirm: slope t >= 2 and supporting check passes; reject: slope t <= -2)
- Supporting check: top third minus bottom third of forecast, mean 5-bar excess return, Welch t > 0: 1.54916, passed: True
- Counts: in-regime grid cases: 1700, top third cases: 566, bottom third cases: 566
- Decided by: Slope t lies between -2 and 2.
- Reading: Grid = positions 0,5,10,... of each window with a 5-bar return inside the window; in-regime = recorded regime 'trending'; coin mean = mean of that coin's grid 5-bar returns over all windows; thirds = the n//3 lowest and n//3 highest forecasts by stable rank; the plan's 150-case minimum is applied as 'not observable'.
- Size: unusual move +0.78 % (t 1.88, the cases of one day together: 836 days) per case over 5 bars, 0.064 of the coin's usual move (10.60 %); normal drift in its direction +0.58 %, total +1.36 %; 1449 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1_uptrend-near-high-continues_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1_uptrend-near-high-continues_1d`
Measure: `measure.py`
