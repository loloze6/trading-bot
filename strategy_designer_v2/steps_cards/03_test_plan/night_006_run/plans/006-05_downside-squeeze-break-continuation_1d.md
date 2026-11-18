---
idea: 006-05_downside-squeeze-break-continuation
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin closes below the low of the prior 20-day band -> kept: a regime rule fires while the close is below the lowest low of bars t-20 to t-1.
- Comparison: how narrow the 20-day band is against the coin's 100-day range -> adapted: "tight" is made graded by the compression of the prior 20-bar range inside the prior 100-bar range.
- Outcome: price keeps falling past the band's bottom over the next 3 days, more for narrower bands -> adapted: the short is held while the close is below the band, and the 3-day holding period is dropped.
- Verdict transfer: yes: the forecast is short only on closes below the band and is larger for narrower bands, so the 3-day falls after it test the idea directly.
Forecast: The forecast is active only on bars whose close is below the lowest low of the previous 20 days. A regime rule makes this check with DistanceFromHigh (extreme "low", 20 bars, bar t excluded) below 0. On those bars the forecast is minus the standardised compression of the prior 20-bar band against the prior 100-bar range (1 minus the range ratio, bar t excluded). Standardise uses a 100-bar window with min_periods 25. The forecast is always zero or negative, and it is about -10 for a band of usual narrowness. It grows towards -20 as the band gets narrower against the 100-day range, and shrinks towards 0 for wide bands. On every other bar it is 0.
Config: 006-05_downside-squeeze-break-continuation_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are the bars of each window's non-overlapping 3-bar grid where the forecast is below 0. For each case, take the 3-bar forward return minus the coin's mean 3-bar return over all windows. The measure is the Welch t of the excess return of the cases with |forecast| at or above the pooled median, minus that of the cases below it.
- Supporting check: The mean excess 3-bar return over all cases is below 0.
- Confirm: The difference has Welch t ≤ -2 and the supporting check passes.
- Reject: The difference has Welch t ≥ +2.
- Inconclusive: A t between -2 and +2 is inconclusive. So is a t of -2 or less when the mean excess return of all cases is 0 or above. The test also needs at least 60 cases, with at least 30 in each half; fewer is inconclusive.
