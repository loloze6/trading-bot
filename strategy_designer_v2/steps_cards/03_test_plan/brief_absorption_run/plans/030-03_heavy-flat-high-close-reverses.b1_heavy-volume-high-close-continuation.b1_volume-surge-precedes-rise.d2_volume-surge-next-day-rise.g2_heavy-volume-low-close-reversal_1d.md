---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 17ade308c2e6
---
Fidelity:
- Situation: a day with heavy volume against its prior 20-day average, closing low in its high-low range -> adapted: the heavy-volume threshold is made graded, as the close's nearness to the low times volume over the prior 20-day mean.
- Comparison: the heavier the volume, the stronger the link -> kept: the volume ratio multiplies the close location, so heavier volume gives a larger position.
- Outcome: the coin rises over the next day, more the lower the close -> kept: the long position is held one day, sized by the product.
- Verdict transfer: yes: the forecast is the idea's own product of close location and volume ratio, long only as the consequence says, and it is judged on next-day returns.
Forecast: One component, VolumeWeightedCloseLocationComponent (volume_period 20, exclude_current 1, reference "high"). It computes (high − close)/(high − low) x volume[t] / mean(volume of the prior 20 days). This is 0 when the close is at the high and grows as the close nears the low and as the day's volume rises above its prior 20-day average. It is standardised over its past 60 values, so a typical day is about +10. A signed_power with exponent 2 then damps ordinary days toward 0 and enlarges heavy-volume closes near the low. The forecast is never negative: it is long when the situation is present and close to 0 otherwise. A close near the high, or light volume, gives near-zero, so no long position.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Pooled regression over all bars of all coins and windows. The dependent variable is the next-day return in excess of the coin's mean daily return over all windows. The regressor is the bar's forecast (post_pipeline_value of "absorb"). The measure is the t of the slope.
- Supporting check: Recompute close location (high−close)/(high−low) and the volume ratio from the bars. The slope of excess next-day return on close location, on days with volume ratio ≥ 1, minus the same slope on days with ratio < 1, must be > 0.
- Confirm: The slope t is ≥ 2 and the supporting check's difference is > 0.
- Reject: The slope t is ≤ −2.
- Inconclusive: A slope t between −2 and 2 is inconclusive. So is a slope t ≥ 2 with the check's difference ≤ 0. The test needs at least 1,000 bars with forecast > 2 across the coins; fewer is inconclusive.
