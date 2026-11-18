---
plan: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling_1d
idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling
fit: adapted
status: mismatch
---
Situation check: 88 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of active bars are short bars on a new 30-bar closing low with RSI above its reading at the prior low, so the forecast does not follow the plan's divergence situation.
- Reading: Situation recomputed from closes inside each window (prior 30-bar low excluding the current bar; Wilder 14-bar RSI now minus RSI at the lowest close of bars t-30..t-4); active bars where it cannot be computed for lack of in-window history are left out of the agreement; event spacing is greedy per window (an event, then the next one at least 20 bars later), events without a full 20-bar forward return in their window are dropped, the coin mean is the pooled mean of its 20-bar grid returns over all windows, the depth slope is OLS of excess return on |forecast|, and fewer than 20 events is reported as not observable.
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling_1d`
Measure: `measure.py`
