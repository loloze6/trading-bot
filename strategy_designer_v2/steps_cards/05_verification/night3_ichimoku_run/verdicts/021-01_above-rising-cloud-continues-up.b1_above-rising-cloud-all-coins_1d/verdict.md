---
plan: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins_1d
idea: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 26-bar excess return over the coin's mean: 0.0943107; t of the mean of forecast-weighted excess returns: 1.74727 (threshold: t >= 2 (confirm, with positive mean) or t <= -2 (reject, with negative mean), at least 50 independent cases)
- Supporting check: Spearman rank correlation forecast vs excess return > 0: -0.0266729, passed: False
- Counts: independent cases: 277
- Decided by: t between -2 and 2 (or not computable), which the plan calls inconclusive.
- Reading: Situation checked on active bars where the cloud top (recomputed from the window's prices, 9/26/52 spans displaced 26) and the 26-day slope (recorded cloud_slope raw value, else recomputed from the cloud midpoint) are both computable; cases are grid bars 0,26,52,... of each window with forecast > 0 and a 26-bar forward return inside the window; the coin's mean is the mean of its non-overlapping 26-bar grid returns over all its windows; the t-statistic is the ordinary t of the mean of the per-case forecast x excess-return products.
- Size: unusual move +1.00 % per case over 26 bars, 0.018 of the coin's usual move (32.35 %); normal drift in its direction +5.35 %, total +6.34 %; 420 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins_1d`
Measure: `measure.py`
