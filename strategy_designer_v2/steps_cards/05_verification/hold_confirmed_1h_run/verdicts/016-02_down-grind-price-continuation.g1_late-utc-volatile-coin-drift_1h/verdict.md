---
plan: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h
idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of vol-sized excess slot return (excess 2-bar return x forecast/10): 0.000961003; t of the mean: 7.67712 (threshold: mean > 0 with t >= 2 to confirm; t <= -2 rejects)
- Supporting check: OLS slope t of excess slot return on forecast at 20:00 bar: 3.74308, passed: True
- Counts: slot cases: 17257
- Decided by: Main mean > 0 with t = 7.68 >= 2 and supporting slope t = 3.74 >= 2.
- Reading: Cases are every bar stamped 20:00 UTC whose 22:00 bar exists in the same window, including cases with forecast 0; the coin mean 2-bar return uses non-overlapping positions 0,2,4,... of each window pooled over all windows; all coins are pooled into one set of cases for the mean and the regression.
Plan: `steps_cards/03_test_plan/hold_confirmed_1h_run/plans/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h.md`
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h`
Measure: `measure.py`
