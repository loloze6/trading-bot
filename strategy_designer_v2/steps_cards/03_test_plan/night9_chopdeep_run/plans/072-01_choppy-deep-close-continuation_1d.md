---
idea: 072-01_choppy-deep-close-continuation
brief: 072_choppy-deep-below-high-falls
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a choppy market, the close's depth below its 20-day high, in 20-day daily-return standard deviations -> kept
- Comparison: deeper closes against closes nearer the high -> adapted: graded, so the short grows with depth and nears 0 at the high
- Outcome: a larger fall over the next day -> kept
- Verdict transfer: yes: the forecast is exactly the depth in usual moves, and the test asks whether the next day's fall grows with it, on up and down days alike.
Forecast: `VolatilityScaledDistanceFromHighComponent` with `period` 20, `vol_period` 20, `source` "high", `exclude_current` 0 and `base` "level". It computes (close − 20-day highest high, bar t included) / that high / std of the last 20 daily returns. This is never positive. It is 0 with the close at the 20-day high and more negative the deeper the close sits below it, counted in usual daily moves. `standardise` (60/20) puts it on the forecast scale, about −10 at an average depth and down to −20 at twice that. The forecast is short only and graded by depth, and it is never long. Step 3's code adds the choppy profile, so the book is flat outside it.
Config: 072-01_choppy-deep-close-continuation_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the next-day return, minus the coin's mean daily return over all windows, on the depth (abs of `depth` post_pipeline_value). It is measured on bars with a non-zero forecast, with standard errors clustered by day.
- Supporting check: The same slope is below 0 separately on bars where the day closed up and on bars where it closed down.
- Confirm: The slope is negative with t ≤ −2, and the check passes.
- Reject: The slope is positive with t ≥ 2, so deeper closes are followed by relatively larger rises.
- Inconclusive: A slope with |t| < 2, or a confirming slope whose check fails in one subset. At least 300 in-profile bars on at least 150 distinct days are needed; fewer is inconclusive.
