---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the coin's 1-hour return in the first hour after the 00:00 UTC settlement, relative to its 24-hour volatility -> kept: a 1-bar return over the std of the last 24 hourly returns, taken only at the close of the 00:00-stamped bar (a regime on the hour of day).
- Comparison: the reversal grows faster than the move, so large moves of several usual hourly moves reverse more per unit than small ones -> kept: the fade is sized convexly (signed_power exponent 2), and the criterion compares the reversal per unit of move across move sizes.
- Outcome: the return over the next 24 hours runs opposite to that move -> kept: each bet is held 24 bars, short after a rise and long after a fall.
- Verdict transfer: yes: the test measures that hour's move in usual moves, fades it convexly and judges the next 24 hours, so a confirm or a reject carries over to the idea.
Forecast: The forecast is computed at the close of the bar stamped 00:00 UTC, which is the first hour after the 00:00 settlement. At that close the coming bar starts at 01:00, so HourOfDayComponent reads 1, and a rule between 0.5 and 1.5 selects the mean_reversion regime. Every other hour is flat (null). The indicator is VolatilityScaledReturnComponent with period 1 and vol_period 24: the hour's return divided by the standard deviation of the last 24 hourly returns. The steps are: 1. Standardise it over its past 60 hourly values (min_periods 20), so a usual hour reads about ±10. 2. Negate it, so the forecast fades the move. 3. Apply signed_power with exponent 2 and pivot 10, which makes the forecast convex in the move. A usual move stays near ±10, half a usual move gives ±2.5 (the position barely changes), and 1.5 usual moves give ±22.5 (capped at ±20). The forecast is negative after an up hour, positive after a down hour, and 0 on a flat hour and on every other bar. The book holds each bet for 24 bars.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The cases are the bars stamped 00:00 with |forecast| >= 2: one per day, 24 bars apart, so they do not overlap. For each case, compute y = forecast × (close[t+24]/close[t] − 1 − d). Here d is the coin's mean 24-hour return over all windows, the drift of simply holding it. The measure is the mean of y over all coins and cases, with its one-sample t.
- Supporting check: Rank the cases by the size of the move (the raw value). Compare the faded return per unit of move, sum(sign(forecast) × (r24 − d)) / sum(|raw|), in the top third against the bottom two thirds. The check passes if the top third's value is larger.
- Confirm: The mean of y is above 0 with t >= 2, and the supporting check passes.
- Reject: The mean of y is below 0 with t <= −2.
- Inconclusive: Any t between −2 and 2, or t >= 2 with a failed supporting check. At least 100 cases with |forecast| >= 2 are required, over all coins and windows; with fewer the result is inconclusive.
