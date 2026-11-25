---
idea: 037-01_wide-day-fall-next-day-rebound
brief: 037_wide-range-separates-forced-falls
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 00d5d6f5c07b
---
Fidelity:
- Situation: a one-day fall, together with that day's high-low range against its average range over the past 14 days -> kept: `RiseTimesRangeMultipleComponent` multiplies the day's percent fall by the day's range over the mean range of the prior 14 days.
- Comparison: the day's range against its own 14-day average range -> kept: the range multiple, with the base excluding the current bar.
- Outcome: a larger rise over the next day, growing with fall and width -> kept: a 1-bar horizon, long only, with a graded position.
- Verdict transfer: yes: the forecast is the idea's product itself, so a positive timing gain that grows with size confirms it, and a negative one rejects it.
Forecast: The forecast is the day's fall in percent times the day's high-low range divided by the mean range of the 14 prior days. It uses `RiseTimesRangeMultipleComponent` with rise_period 1, range_period 14, side "down" and exclude_current 1. The value is standardised against its own past 60 values (window 60, min_periods 20). It is 0 on up or flat days, so the book is flat then. It is positive after a falling day and grows continuously with both the fall's depth and the day's width. It is never negative (long only). The detector is ungated.
Config: 037-01_wide-day-fall-next-day-rebound_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Criterion:
- Horizon: 1 bar
- Main measure: The timing gain before costs, on every bar of every window. It is the position held after bar t's trade × (next-day return − the coin's mean daily return over all windows). It is averaged per day across coins, and its t is taken over days.
- Supporting check: Split the bars with forecast > 0 at the median `post_pipeline_value` of wide_fall. The upper half's mean next-day excess return (coin's return minus its mean daily return) minus the lower half's must be above 0, with Welch t ≥ 1.
- Confirm: The main measure's t is ≥ 2 and its mean is above 0, and the supporting check passes.
- Reject: The main measure's t is ≤ -2, meaning large wide-range falls are followed by declines relative to holding the coin.
- Inconclusive: Any main-measure t between -2 and 2 is inconclusive. A confirm-level main measure whose supporting check fails is also inconclusive. At least 200 bars with forecast > 0, spread over at least 100 distinct days, are needed; fewer is inconclusive.
