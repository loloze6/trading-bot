---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 48-bar excess return on forecast, 20:00-close cases: 0.000279914; OLS slope t: 1.69761 (threshold: confirm if slope t >= 2 (with top-third mean excess > 0); reject if t <= -2)
- Supporting check: mean excess 48-bar return, top third of forecast: 0.00344678, passed: True
- Counts: non-overlapping cases: 4236, top-third cases: 1412
- Decided by: The slope's t lies between -2 and 2.
- Reading: Non-overlap is taken as every other calendar day of 20:00-close bars per window, counted from the window's first one; the coin's mean is over its non-overlapping 48-bar grid across all windows; the top third is the pooled cases with forecast at or above the pooled 2/3 quantile; fewer than 100 cases is reported as not observable.
- Size: unusual move +0.10 % per case over 48 bars, 0.016 of the coin's usual move (6.56 %); normal drift in its direction +0.27 %, total +0.37 %; 5853 cases
Plan: `steps_cards/03_test_plan/step7ab_bp_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound_1h.md`
Record: `steps_cards/04_backtest/step7ab_bp_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound_1h`
Measure: `measure.py`
