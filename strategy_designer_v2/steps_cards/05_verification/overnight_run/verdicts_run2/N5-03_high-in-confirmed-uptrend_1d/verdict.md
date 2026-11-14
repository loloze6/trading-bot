---
plan: N5-03_high-in-confirmed-uptrend_1d
idea: N5-03_high-in-confirmed-uptrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess forward 10-bar return after forecast >= 10 (non-overlapping): 0.0366019; t of the mean (non-overlapping samples): 2.53071 (threshold: mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects; at least 30 non-overlapping cases)
- Supporting check: Spearman rank correlation of forecast vs forward 10-bar excess return on trending bars: 0.080073, passed: True
- Counts: non-overlapping cases with forecast >= 10: 251
- Decided by: Mean excess 10-bar return after forecasts >= 10 is above 0 with t >= 2, on at least 30 non-overlapping cases.
- Reading: The situation is regime == 'trending' with the raw near_high range position above 0 on the long side. The coin mean is taken over all bars with a valid in-window 10-bar return across all its windows. The mean and t are computed on the non-overlapping grid (positions 0, 10, 20, ... of each window) of bars with forecast >= 10; the all-bar mean is 0.0312148517582747. The supporting check is reported but does not enter the decision, because the confirm and reject rules do not name it.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N5-03_high-in-confirmed-uptrend_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N5-03_high-in-confirmed-uptrend_1d`
Measure: `measure.py`
