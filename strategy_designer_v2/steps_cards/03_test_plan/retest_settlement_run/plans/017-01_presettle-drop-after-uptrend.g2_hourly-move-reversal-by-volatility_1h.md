---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the last 1-hour return, relative to 24-hour volatility -> kept
- Comparison: the move's size against its 24-hour volatility, larger means stronger -> kept
- Outcome: the next 1-hour return runs opposite to that move -> kept
- Verdict transfer: yes: the forecast is the negated volatility-scaled 1-hour return, so its next-hour gain is the idea's claim.
Forecast: The forecast uses VolatilityScaledReturnComponent with period 1, vol_period 24, lag 0 and vol_lookback 1. Its raw value is the last 1-hour return divided by the standard deviation of the last 24 one-hour returns. It is standardised against its own past 60 values (min_periods 20) and then negated. The forecast is negative after an up hour and positive after a down hour. It is near 0 after a small move and grows linearly with the move's size in usual moves, up to the ±20 cap. There is no regime and no dead zone: the idea claims a steady relation, and it is applied on every bar.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility_1h_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The pooled least-squares slope of the next 1-hour return on the forecast at bar t, using every bar of every coin and window. The return is close[t+1]/close[t]-1 inside its window, minus the coin's mean hourly return over all its windows. The measure is the slope's t-statistic, before costs.
- Supporting check: The book's mean daily return before costs, minus its gain from the market's own rise, is above 0.
- Confirm: The slope's t is at least 2 and the supporting check passes.
- Reject: The slope's t is -2 or less: the next hour follows the move instead of reversing it.
- Inconclusive: A t between -2 and 2, or a t of 2 or more while the check fails, is inconclusive. A test with fewer than 10,000 bars of nonzero forecast is also inconclusive, whatever its t.
