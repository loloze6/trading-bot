---
plan: 036-02_agitated-scaled-fall-delayed-rebound_1d
idea: 036-02_agitated-scaled-fall-delayed-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of 2-bar excess return on forecast, forecast>0 grid cells: 0.000342857; OLS slope t: 1.20579 (threshold: confirm: slope > 0 with t >= 2 and weighted mean excess > 0; reject: slope < 0 with t <= -2)
- Supporting check: forecast-weighted mean excess 2-bar return: 0.00283395, passed: True
- Counts: grid cells with a positive forecast: 1879
- Decided by: The slope's t lies between -2 and 2.
- Reading: Grid cells start at positions 0, 2, 4, ... of each window and need t+2 inside it; the coin's mean 2-bar return is the mean over all its grid cells in all windows; the regression pools all coins; agitated is the recorded regime not being 'chop'.
- Size: unusual move +0.04 % (t 0.18, the cases of one day together: 987 days) per case over 2 bars, 0.005 of the coin's usual move (6.58 %); normal drift in its direction +0.26 %, total +0.30 %; 2287 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/036-02_agitated-scaled-fall-delayed-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/036-02_agitated-scaled-fall-delayed-rebound_1d`
Measure: `measure.py`
