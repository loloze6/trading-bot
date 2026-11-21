---
idea: 021-01_above-rising-cloud-continues-up
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a31b77de3651
---
Fidelity:
- Situation: the coin closes above its Ichimoku cloud and the cloud is rising -> kept: a regime rule requires the close above the cloud top (9/26/52 spans, displaced 26) and a positive 26-bar slope of the cloud's mid level.
- Comparison: larger the faster the cloud has risen over the past 26 days -> kept: inside the regime, the position grows with the cloud's 26-bar rise.
- Outcome: the return over the next 26 days is positive -> kept: each bet is held 26 daily bars and judged on the 26-bar forward return.
- Verdict transfer: yes: the test measures the idea's own condition, its graded strength and its 26-day horizon, so a confirmation or a rejection carries over to the idea.
Forecast: The regime detector marks a bar "trending" when two things hold. First, `IchimokuCloudPositionComponent` (9/26/52, displacement 26, edge top) is above 0, so the close is above the cloud top. Second, `IchimokuCloudSlopeComponent` (same spans, lookback 26) is above 0, so the cloud's mid level has risen over 26 bars. On every other bar the regime is null and the forecast is 0 (flat). On trending bars the forecast is the cloud's 26-bar slope, standardised against its own last 60 values (about 10 for a usual rise, capped at 20) and clipped at 0. It is therefore always long and grows with how fast the cloud has risen.
Config: 021-01_above-rising-cloud-continues-up_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: The coin's 26-bar forward return minus its normal drift (its mean 26-bar return over all windows), on the non-overlapping 26-bar grid of each window. It is taken on the grid bars where the forecast is above 0. The test is the t of the mean of this excess return.
- Supporting check: Across those same cases, regress the excess 26-bar return on the forecast; the slope must be positive with t ≥ 2.
- Confirm: The mean excess return is positive with t ≥ 2, and the supporting slope is positive with t ≥ 2.
- Reject: The mean excess return is negative with t ≤ -2, or the supporting slope is negative with t ≤ -2.
- Inconclusive: Anything else (either t between -2 and 2, or the main measure confirming without the check passing). The test also needs at least 30 non-overlapping cases across coins and windows; with fewer it is inconclusive.
