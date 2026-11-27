---
idea: 064-02_rising-agitated-volume-growth-stalls
brief: 064_rising-agitated-volume-dry-up-rises
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: a rising, agitated market, where the coin's total volume over the last 30 days has grown against the 30 days before -> kept: the profile is added by code, and the volume growth is the log ratio of the 30-day mean volume to the prior 30-day mean volume, graded
- Comparison: more volume growth against less (or shrinkage) -> kept: the forecast is graded across the size of the volume change
- Outcome: a smaller rise over the next 5 days, the more volume grew -> kept: the coin's 5-bar forward return net of its normal drift should fall as volume growth rises
- Verdict transfer: yes: a graded forecast that leans long on shrinking volume and short on growing volume, read against the 5-day excess return inside the profile, confirms or rejects exactly this relation.
Forecast: Inside the rising-agitated profile, one component, VolumeRatioComponent with period 30, short_period 30, exclude_current 30 and form "log". It gives ln(mean volume of the last 30 days / mean volume of the 30 days before), which is 0 when the two are equal. It is standardised over its own past 60 values (min 20) and negated. The forecast is positive (long) when volume shrank and negative (short) when it grew. Its size grows with the size of the log change, capped at ±20. Outside the profile the code keeps the book flat.
Config: 064-02_rising-agitated-volume-growth-stalls_1d_config.json
Profile: rising agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The slope, and its t, of the coin's 5-bar forward return minus its normal drift (its mean 5-bar return over all windows) on the forecast. It is measured at the bar's close, on the non-overlapping 5-bar grid of each window, over bars with a nonzero forecast. Cases on the same day are summed into one piece of evidence. This is before costs.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2: a larger forecast (more shrinkage) is followed by a larger excess rise, and a negative one (growth) by a smaller one.
- Reject: The slope is negative with t ≤ -2: volume growth is followed by larger excess rises.
- Inconclusive: A t between -2 and 2, or fewer than 100 grid cases (or fewer than 60 distinct days) with a nonzero forecast inside the profile.
