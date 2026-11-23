---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2035953e3f95
---
Fidelity:
- Situation: a day with volume far above its 20-day average, and the close near the day's low -> kept: a regime rule (volume over the prior 20-day mean at 2 or more, by convention) plus a graded close location measured from the high.
- Comparison: none -> kept
- Outcome: the coin rises over the next 1 day, more the nearer the close is to the low -> kept: a long-only position held 1 bar, sized by the close location.
- Verdict transfer: yes: the test measures exactly whether, on heavy-volume days, a close nearer the low is followed by a larger next-day rise.
Forecast: A regime rule fires only on days when today's volume is at least 2 times the mean volume of the prior 20 days (`VolumeRatioComponent`, period 20, exclude_current 1). On every other day the forecast is 0, so the book is flat. On heavy-volume days the forecast is the close location measured from the high (`CloseLocationInRangeComponent`, reference "high"), standardised over its past 60 values. That location is 0 when the close is at the day's high and 1 when it is at the low. The forecast is therefore 0 or positive, never short. It is near 0 for a close at the high, about +10 for a close at a typical location, and up to +20 for a close at the low. It grows continuously as the close nears the low.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take the cases, which are the bars with forecast > 0 (heavy-volume days). Regress each case's next-day return, minus the coin's mean daily return over all windows, on the forecast, and read the t of the slope.
- Supporting check: The forecast-weighted mean of those excess next-day returns over the cases is above 0.
- Confirm: The slope's t is 2 or more and the forecast-weighted mean excess return is above 0, with at least 100 cases.
- Reject: The slope's t is -2 or less, with at least 100 cases.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is a t of 2 or more with a weighted mean excess return at or below 0. Fewer than 100 cases, pooled over coins and windows, is also inconclusive.
