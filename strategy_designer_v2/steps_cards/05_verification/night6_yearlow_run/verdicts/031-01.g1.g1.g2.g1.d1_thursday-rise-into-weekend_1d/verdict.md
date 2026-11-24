---
plan: 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d
idea: 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 2-bar return on forecast, Thursday-close bars with forecast > 0: 0.00127004; OLS slope t: 4.69346 (threshold: slope t >= 2 with positive forecast-weighted mean excess confirms; t <= -2 rejects; at least 200 cases)
- Supporting check: forecast-weighted mean excess 2-bar return > 0: 0.0157884, passed: True
- Counts: cases: 1230
- Decided by: The slope has t >= 2 and the forecast-weighted mean excess return is above 0 (confirm rule).
- Reading: Thursday-close bars are those whose next bar (timestamp + 1 day, UTC) is a Friday; the coin's normal 2-bar drift is the mean of non-overlapping 2-bar returns on a grid from each window's first row, pooled over all its windows; cases need close[t+2] inside the same window; the 14-day return is the recorded raw value or, where missing, recomputed from closes; the plan's 200-case minimum is applied as 'not observable'.
- Size: unusual move +1.14 % (t 3.43, the cases of one day together: 290 days) per case over 2 bars, 0.165 of the coin's usual move (6.58 %); normal drift in its direction +0.24 %, total +1.37 %; 1053 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d`
Measure: `measure.py`
