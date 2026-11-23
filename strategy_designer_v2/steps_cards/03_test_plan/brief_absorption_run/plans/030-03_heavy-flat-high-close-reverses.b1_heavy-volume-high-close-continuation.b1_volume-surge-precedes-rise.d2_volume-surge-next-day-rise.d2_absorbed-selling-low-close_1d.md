---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2035953e3f95
---
Fidelity:
- Situation: a day's volume heavy relative to its own prior 20-day average, with the close low within its high-low range -> kept: the close's distance from the high as a share of the range, times volume over the prior 20-day mean, graded.
- Comparison: the prior 20-day average volume, and the day's own high-low range -> kept
- Outcome: the coin rises more over the next day, the heavier the volume and the lower the close -> kept
- Verdict transfer: yes: the forecast is the idea's own product of the volume surge and the low close, held for its one-day horizon.
Forecast: The forecast is one component, `VolumeWeightedCloseLocationComponent`, with `volume_period` 20, `exclude_current` 1 and `reference` "high". It computes (high - close) / (high - low) of the day, times the day's volume over the mean volume of the 20 prior days. It is standardised over its past 60 values, with min_periods 20. It is never negative, so the book is long only. It is near 0 when the day closed at its high, whatever the volume. It grows as the close sits nearer the low and as the volume is heavier than usual. It is largest on a heavy-volume day that closed at its low, up to the cap of 20.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On every bar of each window (the 1-bar grid), regress the coin's next-day return minus the coin's mean daily return over all windows on the bar's forecast, pooled over coins and windows. Report the slope's t.
- Supporting check: The mean next-day excess return on the top fifth of forecast bars, minus that on the bottom fifth, must be above 0.
- Confirm: The slope is positive with t >= 2, and the supporting check passes.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any slope with -2 < t < 2 is inconclusive, as is t >= 2 with the supporting check failing. At least 1000 bars with a forecast above 0 are required, else the result is inconclusive.
