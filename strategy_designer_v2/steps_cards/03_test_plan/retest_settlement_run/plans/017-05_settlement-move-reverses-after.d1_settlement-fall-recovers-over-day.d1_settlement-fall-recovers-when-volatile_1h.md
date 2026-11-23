---
idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a fall over the 2 hours before a 00:00 or 16:00 UTC settlement, sized against the usual 2-hour move -> adapted: the condition "at a 00:00/16:00 settlement" is a regime on the bar closing at that hour, and the fall is graded in usual 2h moves.
- Comparison: the size of the fall grows more with the 7-day hourly volatility against the 30-day volatility -> kept: the 7-day volatility over its mean across the last 30 days, multiplied into the fall.
- Outcome: the price rises over the next 24 hours, long -> kept: each bet is held 24 bars.
- Verdict transfer: yes: the forecast is the fall times the volatility ratio, placed only at the two settlements and held for the idea's day.
Forecast: The regime is active only on the bar whose close is 00:00 or 16:00 UTC: the coming bar's hour is 0 or 16, so 08:00 is excluded. On every other bar the forecast is 0. On the active bar there is one component, `VolatilityScaledReturnComponent` (period 2, vol_period 168, vol_lookback 720). Its value is the 2-hour return in usual moves, using the 7-day hourly volatility, times that 7-day volatility over its mean across the last 30 days. The component is standardised (window 500, min_periods 120), negated, then clipped at 0. The forecast is therefore positive only after a fall into settlement and 0 after a rise. It grows with the depth of the fall and with how volatile the coin has recently become, and it is never short. Each bet is held 24 bars.
Config: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Use the settlement bars with forecast ≥ 2, taking the first case in each non-overlapping 24-bar grid cell of each window. Regress each case's 24-bar return from the signal close, minus the coin's normal 24-bar drift over all windows, on its forecast; the measure is the slope's t.
- Supporting check: The forecast-weighted mean of those excess 24-bar returns is above 0.
- Confirm: The slope's t is 2 or more and the forecast-weighted mean excess return is above 0.
- Reject: The slope's t is -2 or less and the forecast-weighted mean excess return is below 0.
- Inconclusive: Any slope t between -2 and 2, or a slope and weighted mean whose signs disagree. Fewer than 200 independent cases across all coins is also inconclusive.
