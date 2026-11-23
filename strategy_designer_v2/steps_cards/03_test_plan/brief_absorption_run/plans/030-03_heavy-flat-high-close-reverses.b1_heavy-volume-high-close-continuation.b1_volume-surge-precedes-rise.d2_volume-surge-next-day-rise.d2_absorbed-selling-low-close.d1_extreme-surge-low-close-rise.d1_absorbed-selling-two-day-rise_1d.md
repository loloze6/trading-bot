---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d1_absorbed-selling-two-day-rise
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 17ade308c2e6
---
Fidelity:
- Situation: a day's volume heavy against its own prior 20-day average, with the close near the day's low -> kept
- Comparison: volume against the prior 20-day average, bar t excluded -> kept
- Outcome: the coin rises over the next two days, and the rise grows faster than the volume surge -> kept
- Verdict transfer: yes: the forecast is the idea's own product of close-near-low and the volume multiple, convexly sized, held two days.
Forecast: The forecast is built from `VolumeWeightedCloseLocationComponent` with `volume_period` 20, `exclude_current` 1 and `reference` "high". Its raw value is (high − close)/(high − low) × volume[t]/mean(volume of the prior 20 days). It is never negative: 0 when the close is at the high, larger as the close nears the low and as volume rises above its prior average. `standardise` (60/20) puts it on the forecast scale, about +10 on an average day. `signed_power` (exponent 2, pivot 10) then damps ordinary days towards 0 and amplifies heavy-volume, low-close days, so the position grows faster than the surge. The forecast is long only and graded. It is near 0 when the close is near the high or volume is light, and it grows with both factors.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d1_absorbed-selling-two-day-rise_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The sample is the cells of a non-overlapping 2-bar grid in each window. In each cell, take the coin's 2-day return from the close minus the coin's mean 2-day return over all windows. Regress that excess return on the bar's forecast (`post_pipeline_value`), pooling all coins, and read the slope's t.
- Supporting check: Rank the cells by forecast and take the top fifth. Their mean excess 2-day return must be above 0.
- Confirm: The slope is positive with t ≥ 2, and the top-fifth mean excess return is above 0. Before costs.
- Reject: The slope is negative with t ≤ −2.
- Inconclusive: Any slope with −2 < t < 2 is inconclusive, and so is a confirming slope whose top fifth fails the check. The test needs at least 1000 grid cells pooled and at least 200 in the top fifth; with fewer, the result is inconclusive.
