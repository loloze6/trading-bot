---
plan: 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d
idea: 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 2-bar return on forecast, Thursday-close bars with forecast > 0: -0.00108804; OLS slope t: -1.1434 (threshold: slope t >= 2 with positive forecast-weighted mean excess confirms; t <= -2 rejects; at least 200 cases)
- Supporting check: forecast-weighted mean excess 2-bar return > 0: -0.00599393, passed: False
- Counts: cases: 260
- Decided by: The slope has -2 < t < 2 (inconclusive rule).
- Reading: Thursday-close bars are those whose next bar (timestamp + 1 day, UTC) is a Friday; the coin's normal 2-bar drift is the mean of non-overlapping 2-bar returns on a grid from each window's first row, pooled over all its windows; cases need close[t+2] inside the same window; the 14-day return is the recorded raw value or, where missing, recomputed from closes; the plan's 200-case minimum is applied as 'not observable'.
- Size: unusual move -0.45 % (t -0.57, the cases of one day together: 92 days) per case over 2 bars, -0.032 of the coin's usual move (11.41 %); normal drift in its direction +1.92 %, total +1.48 %; 231 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2016_2017/backtests/031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d`
Measure: `measure.py`
