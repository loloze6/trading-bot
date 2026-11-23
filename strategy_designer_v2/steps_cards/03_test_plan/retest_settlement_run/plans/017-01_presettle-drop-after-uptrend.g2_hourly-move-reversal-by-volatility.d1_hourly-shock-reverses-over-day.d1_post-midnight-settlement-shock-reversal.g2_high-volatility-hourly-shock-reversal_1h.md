---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the 1-hour return relative to the 24-hour volatility, larger the sharper the move -> kept: the 1-bar return divided by the std of the last 24 one-bar returns.
- Comparison: only while the 24-hour volatility is high relative to the 30-day volatility -> kept: a regime rule on the 24-bar return std over the 720-bar return std, above 1.
- Outcome: the return over the next 24 hours runs the opposite way, at any hour of the day -> kept: a fade held 24 bars, on every hour.
- Verdict transfer: yes: the test measures the idea's own move, volatility condition and horizon, so its result is the idea's result.
Forecast: The forecast is computed only while the 24-bar return volatility is above the 720-bar return volatility (RecentToPriorVolatilityRatioComponent with vol_period 24, base_period 720, base_lag 0, ratio above 1.0). It is flat on all other bars. In that regime the forecast is minus the current 1-hour return divided by its 24-bar return std (VolatilityScaledReturnComponent with period 1 and vol_period 24). It is standardised over the 60 values before it, then negated. So it is short after a sharp up-hour and long after a sharp down-hour. Its size grows with the move measured in usual hourly moves, and it is capped at ±20.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Cases are the bars on a non-overlapping 24-bar grid per window where the regime is mean_reversion and the forecast is not 0, pooled over coins and windows. For each case, take the coin's 24-bar return minus the coin's mean 24-bar return over all windows. Regress that excess return on the forecast, before costs, and read the slope's t.
- Supporting check: The mean of the excess 24-bar return times the forecast's sign, over the same cases, is above 0.
- Confirm: The slope is positive with t ≥ 2 (a larger fade forecast is followed by a larger opposite move), and the supporting check passes.
- Reject: The slope is negative with t ≤ -2 (sharp hourly moves continue rather than reverse).
- Inconclusive: A slope t between -2 and 2, or a confirming slope whose supporting check fails. Fewer than 300 grid cases is also inconclusive.
