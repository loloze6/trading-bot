---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of 48-bar excess forward return on forecast (non-overlapping grid, pooled): 0.906918; OLS slope t: 0.906918 (threshold: confirm if slope t >= 2 (with >= 300 positive-forecast grid cases and supporting difference > 0); reject if slope t <= -2)
- Supporting check: grind (upper-median) minus jump (lower-median) mean excess 48-bar return among forecast > 0 grid bars: 0.00292927, passed: True
- Counts: positive-forecast grid cases: 4191, grid cases: 8579, upper (grind) half cases: 2095, lower (jump) half cases: 2096
- Decided by: Slope t lies between -2 and 2.
- Reading: Net 24-hour fall is read from the sign of the raw component (prices' 24h return where it is missing); the grid is positions 0, 48, 96, ... of each window; the coin's normal drift is the mean of its non-overlapping 48-bar grid returns over all windows; the upper half is forecast > median and the lower half forecast <= median; the supporting check passes when the difference is > 0; fewer than 300 positive-forecast grid cases is 'not observable'.
- Size: unusual move +0.08 % per case over 48 bars, 0.011 of the coin's usual move (6.56 %); normal drift in its direction +0.27 %, total +0.35 %; 7924 cases
Plan: `steps_cards/03_test_plan/step7ab_bp_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h.md`
Record: `steps_cards/04_backtest/step7ab_bp_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h`
Measure: `measure.py`
