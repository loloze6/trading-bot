---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 2035953e3f95
---
Fidelity:
- Situation: a day's volume heavy relative to the coin's prior 20-day average, the heavier the stronger -> adapted: a "heavy-volume day" becomes graded; the long grows with the volume ratio above 1 and is zero at or below it.
- Comparison: the coin's own prior 20-day average volume, the current day excluded -> kept
- Outcome: the coin rises over the next day, more so the larger the surge -> kept
- Verdict transfer: yes: the forecast is the idea's own volume ratio against its prior 20 days, held long for one day, so a confirmation or a rejection here is one of the idea.
Forecast: The forecast uses one indicator, the volume ratio: today's volume divided by the mean volume of the 20 days before it (VolumeRatioComponent, period 20, exclude_current 1, centred form, so the reading is the ratio minus 1). It is standardised against its own past 60 values (min_periods 20). Its short side is then clipped at 0, so the idea stays long only. The forecast is zero when today's volume is at or below its prior 20-day average. It is positive when volume is above that average, and the long grows in proportion to the size of the surge, up to the +20 cap. It is never negative. Each long is held for one day.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The slope of a pooled least-squares fit, over every bar of every coin and window. The quantity fitted is the next-day excess return: close[t+1]/close[t] − 1 minus that coin's mean daily return over all its windows. It is fitted on the bar's forecast, including the zero-forecast bars. The measure is the slope's t-statistic, before costs.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2. The fit needs at least 300 bars with a forecast above 0.
- Reject: The slope is negative with t ≤ −2. The fit needs at least 300 bars with a forecast above 0.
- Inconclusive: A slope with −2 < t < 2 is inconclusive, and so is any result from fewer than 300 bars with a forecast above 0.
