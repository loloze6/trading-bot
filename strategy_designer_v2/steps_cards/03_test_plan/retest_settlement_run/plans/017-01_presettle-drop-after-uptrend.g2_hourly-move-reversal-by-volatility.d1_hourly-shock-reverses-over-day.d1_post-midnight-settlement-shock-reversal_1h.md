---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the 1-hour return of the first hour after the 00:00 UTC settlement, relative to 24-hour volatility -> adapted: the hour gate is a regime on the coming bar's hour, and the size is graded by the volatility-scaled return.
- Comparison: the hour's move judged against the coin's 24-hour volatility -> kept: the return is divided by the std of the last 24 hourly returns.
- Outcome: the return over the next 24 hours runs opposite to that hour's move, more so for larger moves -> kept: the position is against the move, sized by it, and held 24 bars.
- Verdict transfer: yes: the test measures the same scaled move at the same clock hour against the same 24-hour reversal.
Forecast: On every bar, `VolatilityScaledReturnComponent` computes the bar's one-hour return divided by the std of the last 24 hourly returns (period 1, vol_period 24). `standardise` scales it (window 60, min_periods 20), and `negate` flips it so the position is against the move. The regime detector uses `HourOfDayComponent` and selects `mean_reversion` only when the coming bar starts at 01:00 UTC. That is the close of the 00:00–01:00 bar, the first hour after settlement. Every other bar is `unknown`, which is flat. On that bar the forecast is negative after an up-hour and positive after a down-hour. Its size grows linearly with the move in usual hourly moves, capped at ±20. It is zero on all other bars, and the 24-bar holding period keeps each daily bet for a day.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The cases are the signal bars, where the regime is `mean_reversion` and the forecast is non-zero, one per coin per day. For each case, take the coin's 24-bar forward return minus its normal 24-bar drift over all windows. Measure the pooled least-squares slope of that excess return on the forecast, with its t.
- Supporting check: Take the mean of sign(forecast) × the drift-adjusted 24-bar return over the cases with |forecast| ≥ 10, which are moves at or above the usual size. It must be above 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check's mean is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope with -2 < t < 2 is inconclusive. A slope with t ≥ 2 whose supporting check fails is also inconclusive. At least 500 cases pooled over coins and windows are required, and at least 100 with |forecast| ≥ 10; fewer is inconclusive.
