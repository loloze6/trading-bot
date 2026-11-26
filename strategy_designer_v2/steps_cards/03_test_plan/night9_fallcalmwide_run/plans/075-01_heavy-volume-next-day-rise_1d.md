---
idea: 075-01_heavy-volume-next-day-rise
brief: 075_daily-volume-level-leans-next-day
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: a day's volume, heavier or lighter, whatever the day's direction -> kept
- Comparison: the coin's own average daily volume over the past 20 days -> kept
- Outcome: the next day's rise, larger the heavier the volume (lower after light volume) -> kept
- Verdict transfer: yes: the forecast is the day's volume over its prior 20-day mean, so a graded next-day lean confirms or rejects the idea directly.
Forecast: One indicator, VolumeRatioComponent: the day's volume divided by the mean volume of the 20 days before it (period 20, exclude_current 1, short_period 1), in its "centred" form (ratio − 1). It is standardised against its own past 60 values (min_periods 20), which keeps the sign and scales the typical size to about 10. The forecast has no regime condition and is the same at both ends of the scale. It is positive (long) when volume is above its 20-day average, growing with how heavy the day is up to the +20 cap. It is negative (short) when volume is below its average, growing with how light the day is. It is zero at exactly average volume. The day's price direction does not enter.
Config: 075-01_heavy-volume-next-day-rise_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the next-day excess return on the bar's forecast, over every bar of every coin and window. The excess return is close[t+1]/close[t] − 1 minus the coin's mean daily return over all its windows. The slope's t is computed with the cases of one date taken together (clustered by day).
- Supporting check: On bars in the top fifth of the forecast, the mean next-day excess return minus the same mean on bars in the bottom fifth must be above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is −2 or less.
- Inconclusive: A slope t between −2 and 2 is inconclusive. A t of 2 or more with the supporting check failing is also inconclusive. At least 500 distinct days with recorded forecasts are required, else the result is inconclusive.
