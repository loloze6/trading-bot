---
plan: 002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation_1d
idea: 002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast x (5-bar forward return minus coin mean 5-bar return), non-overlapping grid, pooled: 0.0927708; t of the mean: 3.34246 (threshold: confirm: mean > 0 with t >= 2 on >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 on >= 30 cases)
- Supporting check: low-vol mean product minus high-vol mean product (recomputed) > 0: 0.0359131, passed: True
- Counts: non-zero-forecast grid cases pooled across coins: 1806, high-volatility grid cases: 1033
- Decided by: Mean product positive with t >= 2 on at least 30 cases, and low-vol minus high-vol mean product is above 0.
- Reading: The plan's low-volatility situation is read from the recorded regime ('trending' is the config rule volpct <= 0.5, since the 100-bar percentile cannot be recomputed inside ~120-bar windows), the side is the sign of the day's return, the coin mean 5-bar return is the mean over all its grid bars of all windows, and on high-volatility bars the forecast is recomputed as k*sign(z)*z^2 (clipped to +-20) from the price-recomputed standardised scaled move, with k fitted on the active bars against the recorded forecast.
Plan: `steps_cards/03_test_plan/plans/002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation_1d`
Measure: `measure.py`
