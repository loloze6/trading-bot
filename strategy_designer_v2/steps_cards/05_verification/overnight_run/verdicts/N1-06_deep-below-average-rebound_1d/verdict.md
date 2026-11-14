---
plan: N1-06_deep-below-average-rebound_1d
idea: N1-06_deep-below-average-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 10-bar forward return after forecast >= 5 minus the coin's mean 10-bar return: 0.00988948; ordinary t of the mean (non-overlapping 10-bar blocks): 0.883225 (threshold: confirm if the mean is > 0 with t >= 2; reject if the mean is < 0 with t <= -2; otherwise inconclusive; at least 30 non-overlapping cases are needed)
- Supporting check: OLS slope of the 10-bar excess return on the forecast, forecast > 0: 0.00175331, passed: True
- Counts: non-overlapping 10-bar cases at forecast >= 5: 201
- Decided by: -2 < t < 2 for the mean excess 10-bar return after forecast >= 5.
- Reading: Overlap is handled with the non-overlapping grid (positions 0, 10, 20, ... of each window) and the ordinary t of the mean. The coin's holding mean is its mean grid 10-bar return over all its windows. The supporting slope uses the same grid bars with forecast > 0 and is reported but does not enter the decision, since the confirm and reject rules do not name it.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N1-06_deep-below-average-rebound_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-06_deep-below-average-rebound_1d`
Measure: `measure.py`
