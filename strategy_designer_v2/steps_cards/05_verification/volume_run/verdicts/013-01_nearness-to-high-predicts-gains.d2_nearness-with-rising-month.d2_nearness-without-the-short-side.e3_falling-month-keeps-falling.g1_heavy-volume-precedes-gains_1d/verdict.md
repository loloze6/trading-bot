---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of coin-demeaned 3-bar forward return on forecast (non-overlapping grid, pooled): 0.00174125; OLS slope t: 4.13504 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive; at least 300 non-overlapping cases)
- Supporting check: none
- Counts: non-overlapping cases: 5723, active bars: 17524
- Decided by: The slope is positive with t = 4.14 >= 2 over 5723 cases (confirm rule).
- Reading: The coin's mean 3-bar return is taken over that coin's non-overlapping grid samples pooled over all its windows, the regression is OLS with an intercept, the 300-case minimum counts the pooled grid cases with a forecast and a return, and the situation check rebuilds standardise from raw values where the full 60-bar history is inside the window and uses the recorded post-pipeline values before that.
Plan: `steps_cards/03_test_plan/volume_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d`
Measure: `measure.py`
