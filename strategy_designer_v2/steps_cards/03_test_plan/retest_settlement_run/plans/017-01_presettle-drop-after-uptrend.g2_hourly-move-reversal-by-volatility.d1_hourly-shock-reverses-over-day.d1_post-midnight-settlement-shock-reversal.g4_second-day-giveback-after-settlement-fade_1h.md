---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the coin's 24-hour return after the first post-00:00-settlement hour runs against that hour's move, larger is stronger -> kept: a clock-and-sign regime, with size growing with the size of the 24-hour return.
- Comparison: against the direction of the 00:00–01:00 UTC hour's move -> kept: that hour's one-bar return, lagged 24 bars, sets the sign condition.
- Outcome: the following 24 hours' return runs back toward that hour's direction -> kept: the position takes the hour's side and is held 24 bars.
- Verdict transfer: yes: the test measures the stated reversal size, the stated reference hour and the stated 24-hour follow-through.
Forecast: The forecast is active on one bar a day only: the bar stamped 00:00 UTC, whose close at 01:00 ends the first post-settlement hour. It is active there only when two moves disagree. The first is the 24-bar return ending at that close (`PriceEvolutionComponent`, period 24). The second is the move of the same hour one day earlier (`VolatilityScaledReturnComponent`, period 1, lag 24). On those bars the forecast is minus the standardised 24-bar return. It is long after a falling 24 hours that followed an up hour, and short after a rising 24 hours that followed a down hour. Its size grows continuously with the size of that 24-hour reversal and is 0 as the reversal nears 0. On every other bar the forecast is 0. Each bet is held for 24 bars.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g4_second-day-giveback-after-settlement-fade_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Each case is a bar in the `trending` regime with a non-zero forecast. On those cases, regress the coin's 24-bar forward return from the signal close, minus the coin's normal 24-bar drift over all windows, on the forecast. The result is the slope and its t, pooled over coins and windows.
- Supporting check: The mean unusual 24-bar move in the forecast's direction over the cases is above 0.
- Confirm: The slope is positive with t ≥ 2, and the mean unusual move in the forecast's direction is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive slope with t ≥ 2 but a mean unusual move of 0 or below is also inconclusive. Fewer than 300 cases in total is inconclusive.
