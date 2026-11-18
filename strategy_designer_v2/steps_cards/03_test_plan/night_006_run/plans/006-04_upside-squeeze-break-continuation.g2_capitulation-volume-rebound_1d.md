---
idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: the coin has fallen over the last 5 days, with its 5-day average volume high against its 30-day average -> kept: the fall is the regime condition (5-bar return below 0), and the volume ratio (5-bar mean over 30-bar mean) sizes the position.
- Comparison: higher 5-day/30-day volume ratio against lower, among falling coins -> kept: the position grows with the ratio, and thin-volume declines get small positions.
- Outcome: a larger rebound (price rises) over the next 3 days -> kept: a long position measured over 3 bars.
- Verdict transfer: yes: the test buys falls in proportion to the volume ratio and checks whether the 3-day rebound grows with that size.
Forecast: When the 5-bar price change is negative (the regime rule), the forecast is the 5-bar mean volume divided by the 30-bar mean volume, standardised against its own last 60 values. It is always positive, about +10 at the usual ratio and up to +20 when volume is about twice its usual ratio. It is long and grows with the ratio. On bars where the coin has not fallen over the last 5 days, the forecast is 0 (flat).
Config: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Use regime `mean_reversion` bars on a non-overlapping 3-bar grid in each window. Take the forward return close[t+3]/close[t]-1, minus the coin's mean 3-bar return over all its windows. Regress this excess return on the forecast and read the slope's t, pooled over coins and windows.
- Supporting check: The mean excess 3-bar return of the top-third forecast cases minus that of the bottom-third cases is above 0.
- Confirm: The slope's t is at least 2 and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2, or a t of 2 or more with a failed supporting check, is inconclusive. Any result from fewer than 100 independent grid cases in the falling regime is also inconclusive.
