---
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 3d6ac1c822df
---
Fidelity:
- Situation: a 4h close above the highest high of the preceding two days, only while the 7-day return is positive -> kept: the break is measured over 12 prior bars with bar t excluded, and the 7-day (42-bar) return above 0 is a regime rule.
- Comparison: how far the close sits above the two-day high, in the 30-day average 4h range -> kept: the break size is divided by the mean bar range over 180 bars.
- Outcome: the coin rises over the next three days, more for larger breaks -> kept: the 18-bar forward return is judged against the coin's drift and grows with the forecast.
- Verdict transfer: yes: the forecast is the idea's own break measure, active only in the idea's own condition, and it is judged on the idea's own horizon.
Forecast: The forecast is computed only on bars where the 42-bar (7-day) return is above 0; on all other bars it is 0 (flat). On those bars it is BreakoutInMeanRangesComponent with period 12 and base_period 180: max(0, close − highest high of the prior 12 bars) divided by the mean high-low range of the last 180 bars. This is standardised over its past 180 values (min_periods 45). The forecast is 0 when the close is at or below the 2-day high. It is positive when the close breaks above that high, and it grows linearly with the size of the break, up to the cap of 20. It is long only by construction.
Config: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The cases are rises of the forecast of at least 2 points, read once per non-overlapping 18-bar grid cell of each window. For each case, take the coin's 18-bar return from the signal bar's close, minus the coin's normal 18-bar drift (holding the coin, over all windows). The measure is the mean of these unusual moves over all coins and windows, with the ordinary t of that mean. It is judged before costs.
- Supporting check: Split the cases at the median forecast. The cases above the median must have a larger mean unusual move than the cases below it (difference, top minus bottom, above 0).
- Confirm: The mean unusual move is positive with t >= 2, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 when the supporting check fails, and so is any result with fewer than 100 independent cases in total (pooled over the 6 coins and 24 windows).
