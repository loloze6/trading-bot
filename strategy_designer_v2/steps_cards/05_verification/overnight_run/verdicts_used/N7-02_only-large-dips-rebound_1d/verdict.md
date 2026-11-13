---
plan: N7-02_only-large-dips-rebound_1d
idea: N7-02_only-large-dips-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 3-bar forward return after forecast >= 5 bars: 0.00346006; t of the mean: 1.03143 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 30 de-overlapped cases)
- Supporting check: mean excess 3-bar return on mild down days (0 < forecast < 2), 95% CI includes 0: 0.00154275, passed: True
- Counts: de-overlapped cases (forecast >= 5): 746, forecast >= 5 bars: 1191, de-overlapped mild cases (0 < forecast < 2): 935
- Decided by: t is between -2 and 2 (inconclusive rule).
- Reading: The coin's mean 3-bar return is over all bars of all its windows; events within 3 bars of the previous event in the same window are chained into one case valued at its first event; the mild group is de-overlapped the same way, and the supporting check is reported but does not change the plan's t rule.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N7-02_only-large-dips-rebound_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N7-02_only-large-dips-rebound_1d`
Measure: `measure.py`
