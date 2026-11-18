---
plan: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast[t] x next-day excess return over coin mean, pooled: 0.00811037; t of the mean: 2.28164 (threshold: confirm t >= 2 with positive check; reject t <= -2)
- Supporting check: mean next-day excess return, forecast>0 minus forecast<0: 0.00224191, passed: True
- Counts: bars_measured: 5794, bars_nonzero_forecast: 5794, bars_forecast_positive: 2832, bars_forecast_negative: 2962
- Decided by: The main measure has t >= 2 and the supporting check is positive.
- Reading: Down/up day is taken from the sign of the raw vol-scaled 1-day return (price return if missing), the long situation also requires a non-zero raw fall_low value; the main mean includes every bar with a next bar in its window (zero forecasts included), and the minimum counts are the bars with a non-zero forecast and a next-day return, by forecast sign.
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d`
Measure: `measure.py`
