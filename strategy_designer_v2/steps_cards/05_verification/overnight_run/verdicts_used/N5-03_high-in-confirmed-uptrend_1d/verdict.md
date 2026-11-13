---
plan: N5-03_high-in-confirmed-uptrend_1d
idea: N5-03_high-in-confirmed-uptrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess forward 10-bar return on bars with forecast >= 10: 0.0312149; t of the mean on non-overlapping 10-bar samples: 2.53071 (threshold: mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects; at least 30 non-overlapping cases)
- Supporting check: Spearman correlation of forecast vs forward 10-bar excess return on trending bars: 0.080073, passed: True
- Counts: non-overlapping cases with forecast >= 10: 251
- Decided by: Confirm rule: mean excess 10-bar return after forecasts >= 10 is above 0 with t >= 2 and at least 30 non-overlapping cases.
- Reading: Situation checked on regime == 'trending' plus near_high raw range position > 0 with a positive forecast; the coin's mean 10-bar return is the mean of all its in-window forward 10-bar returns over all its windows; the mean uses all bars with forecast >= 10 while the t and the case count use the non-overlapping grid (positions 0, 10, 20, ... of each window).
Plan: `steps_cards/03_test_plan/overnight_run/plans/N5-03_high-in-confirmed-uptrend_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N5-03_high-in-confirmed-uptrend_1d`
Measure: `measure.py`
