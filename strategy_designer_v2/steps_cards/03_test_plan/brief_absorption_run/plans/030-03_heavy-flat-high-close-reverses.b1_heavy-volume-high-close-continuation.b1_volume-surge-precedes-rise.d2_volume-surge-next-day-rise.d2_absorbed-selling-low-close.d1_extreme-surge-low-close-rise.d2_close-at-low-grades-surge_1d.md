---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d2_close-at-low-grades-surge
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 17ade308c2e6
---
Fidelity:
- Situation: a day of heavy volume against the prior 20-day average, with the close near the day's low -> adapted: "heavy" is graded as volume over the prior 20-day mean, multiplied by the close's distance from the high, (high-close)/(high-low).
- Comparison: volume against the coin's prior 20-day average, today excluded -> kept
- Outcome: the coin rises over the next day, more so the nearer the close is to the low, and steeply so at the very low -> kept: a long-only forecast with a convex graded dead zone, held for 1 bar.
- Verdict transfer: yes: the forecast is the idea's surge times close-near-low reading, made steep near the extreme, so its next-day result answers the idea.
Forecast: One component, VolumeWeightedCloseLocationComponent (volume_period 20, exclude_current 1, reference "high"). It is today's volume over the mean of the prior 20 days' volumes, times (high - close) / (high - low). It is near 0 when the close sits at the day's high or volume is thin. It grows with the volume surge and as the close nears the low. It is standardised over its past 60 values (about 10 at its usual size). It then passes through signed_power with exponent 3 and pivot 20, the strongest graded dead zone. Faint readings and upper-half closes give almost nothing, and only heavy days closing near the low reach a large long. The raw value is never negative, so the forecast is long or flat, never short.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d2_close-at-low-grades-surge_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The cases are bars where the forecast rose by at least 2 points on its long side (the holding period's bets), one per daily grid cell, pooled over coins and windows. For each case, take the coin's next-day return minus the coin's mean daily return over all its windows. Measure the mean of these excess returns and its t (ordinary t of the mean), before costs.
- Supporting check: The book's mean daily return minus its gain from the market's own rise (the timing part) is above 0.
- Confirm: The mean excess next-day return over the cases is positive with t >= 2, and the timing part of the book's mean daily return is above 0.
- Reject: The mean excess next-day return over the cases is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive t >= 2 with a timing part at or below 0 is also inconclusive. Fewer than 100 cases over all coins and windows is inconclusive, whatever the t.
