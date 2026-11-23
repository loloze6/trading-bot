---
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: last hour's move, relative to the coin's usual hourly volatility -> kept
- Comparison: stronger when the coin's 24-hour volatility is high -> adapted: an on/off condition made graded, as a multiplier of the current 24h volatility over its 30-day average
- Outcome: next hour, the price moves against last hour's move, more so the larger that move -> kept
- Verdict transfer: yes: the forecast is the faded last-hour move in usual hourly moves, times the 24h-volatility ratio, held for one hour.
Forecast: The forecast uses VolatilityScaledReturnComponent with period 1, vol_period 24 and vol_lookback 720. Its raw value is the last hour's return divided by the usual hourly volatility. That usual volatility is the 30-day mean of the 24-hour standard deviation of hourly returns. The raw value therefore equals the move in current 24h-volatility units times the current 24h volatility over its 30-day mean, so it grows with the move's size and with how high the 24h volatility is. The value is standardised over its past 500 values (min_periods 120) and negated. The forecast is negative after an up hour and positive after a down hour. Its size grows linearly with the scaled move and the volatility ratio, and it is near zero after a flat hour. There is no regime and no dead zone.
Config: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Pool the bars of all coins and windows. Regress the next-hour return, minus the coin's mean hourly return over all windows, on the bar's forecast (post_pipeline_value of fade_1h). Report the slope's t.
- Supporting check: Recompute from closes whether the 24h volatility is at or above its 720-bar mean. The same slope on bars where it is must exceed the slope on the other bars (difference above 0).
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with the supporting check failing is also inconclusive. The test needs at least 5000 bars in total and at least 1000 in each volatility group.
