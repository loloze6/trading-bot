---
plan: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: ordinary t of the mean of (excess 2-bar return x forecast/10) on 20:00 UTC decision bars: 0.00059806; ordinary t of the mean: 6.17459 (threshold: confirm if t >= 2 and supporting slope > 0; reject if t <= -2; otherwise inconclusive; at least 200 decision bars with forecast > 0)
- Supporting check: OLS slope of excess 2-bar return on forecast, decision bars with forecast > 0: 3.26526e-05, passed: True
- Counts: decision bars with forecast > 0: 8613, decision bars: 17403
- Decided by: The main t is 2 or more and the supporting slope is above 0.
- Reading: Coming hour is taken as the bar's start hour + 1; the fall is the sign of the raw fall24 value (the 24-bar price return where it is not recorded); the main mean pools all 20:00 decision bars, including those with forecast 0 (product 0); the coin mean 2-bar return is pooled over all its windows on a grid at positions 0, 2, 4, ... of each window; a shortfall of the plan's 200-bar minimum is reported as 'not observable'.
Plan: `steps_cards/03_test_plan/d_line_1h_run/plans/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h.md`
Record: `steps_cards/04_backtest/d_line_1h_run/backtests/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h`
Measure: `measure.py`
