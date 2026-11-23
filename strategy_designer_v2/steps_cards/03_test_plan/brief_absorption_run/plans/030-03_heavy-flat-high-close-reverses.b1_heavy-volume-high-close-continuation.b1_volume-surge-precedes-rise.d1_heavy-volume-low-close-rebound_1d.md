---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2035953e3f95
---
Fidelity:
- Situation: a day's volume heavy against its prior 20-day average, with the close near the day's low, graded -> kept
- Comparison: the prior 20-day average volume, with the day itself left out -> kept
- Outcome: the coin rises over the next 10 days, more so the stronger the situation -> kept
- Verdict transfer: yes: the forecast is the idea's own product of the volume ratio and the close's nearness to the low, held for 10 days.
Forecast: The forecast is built from one component, VolumeWeightedCloseLocationComponent, with volume_period 20, exclude_current 1 and reference "high". Its raw value is (high − close) / (high − low), multiplied by the day's volume over the mean volume of the 20 prior days. - It is 0 when the close sits at the day's high. - It grows as the close nears the low and as the volume gets heavier than usual. - It is never negative, so the forecast is long or flat only. Steps: - It is standardised against its past 60 values (min_periods 20), so an average day reads about 10, capped at 20. - signed_power with exponent 3 and pivot 20 then damps ordinary days hard: 10 becomes 2.5 and 5 becomes about 0.3. - Heavy-volume days that closed near their low stay near 20. The position therefore grows smoothly with volume and close depth, and is near zero after ordinary days.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The slope of the next-10-bar return on the forecast, in pooled least squares. - Cases: the non-overlapping 10-bar grid of each window (bars 0, 10, 20, …). - The return is close[t+10]/close[t] − 1, minus the coin's mean 10-bar return over all its windows (holding the coin). - The t of the slope is reported with its case count.
- Supporting check: The mean excess 10-bar return on grid bars with a forecast of 10 or more is above 0, over at least 30 such cases.
- Confirm: The slope's t is 2.0 or more, and the supporting check passes.
- Reject: The slope's t is −2.0 or less, that is, a lower return the heavier the volume and the lower the close.
- Inconclusive: Any of these results is inconclusive: - the slope's t lies between −2.0 and 2.0; - the slope confirms but the check fails; - there are fewer than 300 grid cases in total, or fewer than 30 cases with a forecast of 10 or more.
