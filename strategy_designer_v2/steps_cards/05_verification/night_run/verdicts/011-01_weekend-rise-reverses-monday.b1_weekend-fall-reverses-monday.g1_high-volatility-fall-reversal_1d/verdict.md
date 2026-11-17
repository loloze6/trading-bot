---
plan: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x next-day excess return on bars with forecast > 0, pooled: 0.00553164; t of the mean: 5.09534 (threshold: confirm if t >= 2 with Spearman rho > 0; reject if t <= -2; else inconclusive; at least 100 bars with forecast > 0)
- Supporting check: Spearman rho of forecast vs next-day excess return > 0: 0.0624741, passed: True
- Counts: bars with forecast > 0: 3982
- Decided by: t = 5.10 >= 2 and the rank correlation 0.062 > 0: the confirm rule.
- Reading: The plan's situation (a down day in the high-volatility regime) is taken as regime == 'mean_reversion' (the volatility-percentile regime, which is not recorded and cannot be rebuilt inside ~120-bar windows) and a negative close-to-close return from the prices, falling back to the sign of fall_vol's raw value on a window's first bar; the expected side is long; the coin's mean daily return is the mean of all its next-day returns over all windows; the 'fewer than 100 bars with forecast > 0' rule is applied as a minimum count, counting only bars that have a next-day return.
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal_1d`
Measure: `measure.py`
