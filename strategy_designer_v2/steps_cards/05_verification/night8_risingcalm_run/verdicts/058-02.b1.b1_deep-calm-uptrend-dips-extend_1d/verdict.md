---
plan: 058-02.b1.b1_deep-calm-uptrend-dips-extend_1d
idea: 058-02.b1.b1_deep-calm-uptrend-dips-extend
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x (5-bar forward return minus coin's mean 5-bar return), forecast<0, non-overlapping grid: 0.00520952; t of the mean, cases of one day summed as one piece of evidence: 0.612557 (threshold: confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: mean excess 5-bar return, deepest third minus shallowest third (must be < 0): -0.000601519, passed: True
- Counts: cases: 715, distinct days: 239
- Decided by: t of the mean product lies between -2 and 2
- Reading: the rising calm profile is the recorded regime 'unknown'; grid cells need a full 5-bar forward return inside the window; the coin's mean is over all its grid returns in all windows; thirds are n//3 cases at each end sorted by forecast; the t uses a day-clustered standard error.
- Size: unusual move +0.04 % (t 0.09, the cases of one day together: 594 days) per case over 5 bars, 0.000 of the coin's usual move (11.68 %); normal drift in its direction -0.73 %, total -0.69 %; 1159 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/058-02.b1.b1_deep-calm-uptrend-dips-extend_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/058-02.b1.b1_deep-calm-uptrend-dips-extend_1d`
Measure: `measure.py`
