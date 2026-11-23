---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the 1-hour return of the first hour after the 00:00 UTC settlement on Saturday or Sunday, relative to 24-hour volatility -> kept
- Comparison: the weekend reversal against the weekday one -> kept (measured in the criterion; weekday cases are recomputed from prices)
- Outcome: the next 24 hours' return runs opposite to that hour's move, more so the larger the move -> kept
- Verdict transfer: yes: the config fades exactly the weekend post-settlement hour, scaled by 24-hour volatility, and holds it for 24 hours.
Forecast: The regime detector selects only the bar stamped 00:00 UTC on Saturday or Sunday. It does this by requiring the coming bar to be the 01:00 bar (HourOfDay 1) on weekday 5 or 6. On that bar the forecast is minus the bar's own 1-hour return divided by the standard deviation of the last 24 one-bar returns (VolatilityScaledReturnComponent, period 1, vol_period 24). It is standardised over the 60 values before it (min 20) and then negated. It is short after an up hour and long after a down hour, and its size grows linearly with the move in usual moves, capped at ±20. On every other bar the regime is null and the forecast is 0. The 24-bar holding period carries the bet through the next 24 hours.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: On each weekend 00:00-bar case, take the coin's 24-bar return from that bar's close minus the coin's mean 24-bar return over all windows. Regress it on the recorded forecast, pooled over coins and windows. The cases are 24 bars apart, so they do not overlap. The measure is the slope's t.
- Supporting check: Recompute the same faded, volatility-scaled 00:00-hour move from prices for weekday cases (Monday to Friday) and run the same regression. The weekend slope minus the weekday slope must be above 0.
- Confirm: The weekend slope is positive with t ≥ 2 over at least 1000 weekend cases, and the weekend slope exceeds the weekday slope.
- Reject: The weekend slope is negative with t ≤ -2 over at least 1000 cases, meaning the hour's move continues rather than reverses.
- Inconclusive: Any of these is inconclusive: - a weekend t between -2 and 2; - a weekend t ≥ 2 while the weekend slope does not exceed the weekday slope; - fewer than 1000 weekend cases.
