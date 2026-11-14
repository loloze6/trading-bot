---
plan: N2-02_capitulation-rebound_1d
idea: N2-02_capitulation-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 10-bar excess forward return after forecast >= 10, pooled, non-overlapping: 0.0206189; t of the mean: 0.89693 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 non-overlapping cases)
- Supporting check: mean excess rises across in-regime forecast buckets [0,5), [5,10), >=10 (value: top minus bottom bucket mean): 0.0278941, passed: True
- Counts: non-overlapping cases with forecast >= 10: 69, in-regime cases forecast 0 to 5: 683, in-regime cases forecast 5 to 10: 43, in-regime cases forecast 10 and above: 69
- Decided by: The t-statistic lies between -2 and 2 with at least 30 cases, so it neither confirms nor rejects.
- Reading: Cases are the bars at positions 0, 10, 20, ... of each window, and the coin's mean 10-bar return is taken over that same grid pooled across all its windows; the buckets are half-open [0,5), [5,10), >=10 on mean_reversion-regime bars including zero forecasts; and the supporting check passes when the three bucket means strictly increase and does not enter the decision.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N2-02_capitulation-rebound_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N2-02_capitulation-rebound_1d`
Measure: `measure.py`
