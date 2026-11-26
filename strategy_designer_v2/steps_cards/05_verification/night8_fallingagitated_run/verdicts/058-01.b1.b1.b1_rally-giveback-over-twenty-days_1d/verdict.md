---
plan: 058-01.b1.b1.b1_rally-giveback-over-twenty-days_1d
idea: 058-01.b1.b1.b1_rally-giveback-over-twenty-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 20-bar forward return on abs(forecast), forecast<0 grid cells: -0.00834939; OLS slope t: -2.91956 (threshold: slope t <= -2 confirms (with supporting check); slope t >= +2 rejects)
- Supporting check: mean drift-adjusted 20-bar return over cases < 0 with day-clustered t <= -2: -1.9567, passed: False
- Counts: non-overlapping cases: 112, days: 36, active bars: 2361
- Decided by: Neither the confirm rule (slope t <= -2 with supporting check passed) nor the reject rule (slope t >= +2 or mean t >= +2) is met.
- Reading: Cases are grid cells at positions 0,20,40,... of each window with forecast < 0 and a full 20-bar forward return inside the window, drift is the coin's mean over that grid in all windows, the supporting t clusters deviations by UTC day, the same t is used for the reject rule's mean, and the plan's 30-case minimum gives 'not observable' when unmet.
- Size: unusual move +3.74 % (t 2.01, the cases of one day together: 185 days) per case over 20 bars, 0.132 of the coin's usual move (24.73 %); normal drift in its direction -3.09 %, total +0.66 %; 354 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.b1.b1.b1_rally-giveback-over-twenty-days_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.b1.b1.b1_rally-giveback-over-twenty-days_1d`
Measure: `measure.py`
