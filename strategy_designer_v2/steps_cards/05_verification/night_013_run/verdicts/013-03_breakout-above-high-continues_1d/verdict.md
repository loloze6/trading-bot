---
plan: 013-03_breakout-above-high-continues_1d
idea: 013-03_breakout-above-high-continues
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 30-bar excess return on forecast (forecast > 0 grid bars): 0.205492; OLS slope t: 5.17955 (threshold: slope t >= 2 with mean excess > 0 confirms; t <= -2 rejects; at least 30 cases)
- Supporting check: mean excess 30-bar return on break bars (minus coin's mean 30-bar return) > 0: 0.229245, passed: True
- Counts: grid bars where the forecast is above 0: 10
- Decided by: Only 10 grid bars with forecast above 0, fewer than the plan's minimum of 30 cases.
- Reading: The coin's mean 30-bar return is the mean over all its windows' non-overlapping 30-bar grid returns (positions 0, 30, 60, ... with a full 30 bars ahead), and the plan's fewer-than-30-cases rule is reported as 'not observable' per the workflow's minimum-count rule.
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-03_breakout-above-high-continues_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-03_breakout-above-high-continues_1d`
Measure: `measure.py`
