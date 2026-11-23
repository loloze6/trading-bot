---
plan: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation
fit: exact
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-24-bar return minus drift on forecast: -8.12028e-05; OLS slope t: -2.29936 (threshold: slope t >= 2 (with check mean > 0) to confirm, slope t <= -2 to reject)
- Supporting check: mean of sign(forecast) x (24-bar return - drift): -0.000999983, passed: False
- Counts: independent cases: 11744
- Decided by: Slope t <= -2 (moves of quiet hours reverse) with at least 200 independent cases.
- Reading: Volatility ratio recomputed per window from close-to-close hourly returns (rolling std, ddof 1, 24 and 720 returns including the current bar), the expected side is the sign of the hour's move (raw component value, else the 1-bar price return), active bars without a computable ratio are left out of the agreement; the drift is each coin's mean 24-bar return over all grid cells of all its windows, the slope's t is the ordinary OLS t of a pooled regression with intercept, and the independent cases are the active grid cells with a 24-bar return inside their window.
- Size: unusual move -0.06 % per case over 24 bars, -0.013 of the coin's usual move (4.87 %); normal drift in its direction -0.00 %, total -0.07 %; 14921 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h`
Measure: `measure.py`
