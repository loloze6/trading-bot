---
plan: 010-08_rsi-below-streak-reversal_1d
idea: 010-08_rsi-below-streak-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess next-14-bar return on forecast (grid bars, forecast > 0): 0.00185625; OLS t of slope: 1.07762 (threshold: slope t >= +2 to confirm (with top-minus-bottom third > 0), t <= -2 to reject)
- Supporting check: top-third minus bottom-third mean excess 14-bar return: 0.0373083, passed: True
- Counts: independent grid bars with forecast > 0: 185
- Decided by: The slope's t is between -2 and +2 (or undefined), so neither the confirm nor the reject rule is met.
- Reading: Situation taken as the component's raw signed run length below zero, expected side long; each coin's mean 14-bar return is the mean over the same non-overlapping 14-bar grid of all its windows, the slope's t is the OLS t of excess return on forecast, and the thirds are the n//3 lowest and n//3 highest forecasts after a stable sort.
Plan: `steps_cards/03_test_plan/night_rsi_run/plans/010-08_rsi-below-streak-reversal_1d.md`
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-08_rsi-below-streak-reversal_1d`
Measure: `measure.py`
