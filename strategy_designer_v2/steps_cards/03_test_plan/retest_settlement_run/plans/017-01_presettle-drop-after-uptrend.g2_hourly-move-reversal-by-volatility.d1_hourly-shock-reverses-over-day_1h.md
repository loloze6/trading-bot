---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the last 1-hour return is large -> kept: the current bar's one-bar return.
- Comparison: relative to its 24-hour volatility -> kept: divided by the std of the last 24 one-bar returns.
- Outcome: the return over the next 24 hours runs the opposite way, more so as the ratio grows -> kept: a negated graded forecast whose bets are held for 24 bars.
- Verdict transfer: yes: the forecast is the idea's own ratio, held against the move for its stated 24-hour horizon.
Forecast: The forecast is built from VolatilityScaledReturnComponent with period 1, vol_period 24, lag 0 and vol_lookback 1. Its raw value is the last hourly return divided by the standard deviation of the last 24 hourly returns. That value is standardised against its own past 60 values (min_periods 20) and then negated. The forecast is short after an up hour and long after a down hour. Its size is linear in the move counted in usual hourly moves, it is near 0 after a quiet hour, and it is capped at ±20. It is active on every bar, with no regime.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Use the bars at positions 0, 24, 48, … of each window. On those bars, regress the coin's 24-bar forward return minus its normal drift (its mean 24-bar return over all windows) on the forecast, pooled across coins and windows. The measure is the slope's t, with returns before costs.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2: the excess return after a bar grows in the forecast's direction as the forecast grows.
- Reject: The slope is negative with t ≤ -2: larger moves are followed by continuation, not reversal.
- Inconclusive: A t strictly between -2 and 2 is inconclusive. Fewer than 500 grid cases with a non-zero forecast is also inconclusive.
