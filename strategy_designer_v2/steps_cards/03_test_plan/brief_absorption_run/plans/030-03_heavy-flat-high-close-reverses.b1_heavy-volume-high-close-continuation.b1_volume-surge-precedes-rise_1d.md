---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2035953e3f95
---
Fidelity:
- Situation: a day's volume, heavier the larger the surge -> kept: the log of the day's volume over its average, graded and clipped to the heavy side.
- Comparison: the coin's own prior 20-day average volume -> kept: the base is the 20 days before the day, with the day itself excluded.
- Outcome: the coin rises over the next 10 days, more so after a larger surge, with no shorts -> kept: long only, held for 10 bars.
- Verdict transfer: yes: the forecast is the idea's own graded volume surge against the same base, long only, judged over the same 10 days.
Forecast: The forecast starts from the natural log of one ratio: the day's volume over the mean volume of the 20 prior days (`VolumeRatioComponent`, period 20, exclude_current 1, form "log"). The log is positive on heavier-than-usual days and negative on lighter ones. It is standardised against its own last 60 values (min_periods 20), which keeps its sign. It is then clipped at 0, so it never goes short. The forecast is 0 on days at or below the prior average. It is positive on heavier days and grows continuously with the surge, up to the cap of 20.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use the non-overlapping 10-bar grid of each window. On each grid bar, take the coin's 10-bar forward return minus the coin's mean 10-bar return over all its windows. Measure the slope of that excess return on the forecast, before costs, pooled over all coins and windows, with its t.
- Supporting check: Take the grid bars with forecast > 0. Their mean excess 10-bar return (as above) must be above 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope with t between -2 and 2 is inconclusive. So is a positive slope with t ≥ 2 when the mean excess on bars with forecast > 0 is not above 0. The test needs at least 100 independent grid cases with forecast > 0; with fewer, it is inconclusive.
