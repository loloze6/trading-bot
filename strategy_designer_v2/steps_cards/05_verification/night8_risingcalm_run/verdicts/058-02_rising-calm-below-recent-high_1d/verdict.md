---
plan: 058-02_rising-calm-below-recent-high_1d
idea: 058-02_rising-calm-below-recent-high
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: clustered OLS slope t of 5-bar excess return on forecast (in-profile grid bars): -0.00105883; OLS slope t, day-clustered: -1.66833 (threshold: confirm if t >= 2 (with forecast-weighted mean excess > 0); reject if t <= -2)
- Supporting check: forecast-weighted mean excess 5-bar return > 0: -0.00275719, passed: False
- Counts: in-profile grid cases: 607, cases with forecast above 0: 396
- Decided by: slope t between -2 and 2
- Reading: profile = recorded regime 'unknown'; grid = rows 0,5,10,... of each window with a 5-bar return inside it; normal drift = coin's mean 5-bar return on that grid over all its windows; slope t uses a day-clustered (CR1) OLS standard error, timestamps grouped by UTC date.
- Size: unusual move +0.44 % (t 0.77, the cases of one day together: 413 days) per case over 5 bars, 0.044 of the coin's usual move (10.60 %); normal drift in its direction +0.63 %, total +1.08 %; 645 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/058-02_rising-calm-below-recent-high_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/058-02_rising-calm-below-recent-high_1d`
Measure: `measure.py`
