---
idea: 074-01_agitated-stretch-below-rebounds
brief: 074_agitated-stretch-below-average-rebounds
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in an agitated market, the close sits below its 20-day average, in units of the 20-day standard deviation of daily returns -> kept: the agitated profile is added by code, and the depth is read by `MovingAverageDistanceComponent` (sma 20, usual_moves, vol_period 20), clipped to the below side.
- Comparison: none -> kept
- Outcome: the coin rises more over the next 10 days the deeper the stretch -> kept: each bet is held 10 bars, and the long position grows with the depth.
- Verdict transfer: yes: the forecast is exactly the depth below the average in usual moves, inside the agitated profile, held for the idea's 10 days.
Forecast: The forecast is the distance of the close from its 20-day simple average, divided by the standard deviation of the last 20 daily returns. It is standardised over its past 60 values (min 20), then negated and clipped at 0. So it is 0 when the close is at or above the average. It is positive and grows linearly as the close sits more usual moves below the average, capped at 20. It is never negative (long only). Outside the agitated profile, code keeps the book flat.
Config: 074-01_agitated-stretch-below-rebounds_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 10 bars
- Main measure: The slope of the coin's 10-bar forward return, minus its normal drift (its mean 10-bar return over all windows), on the bar's forecast. It is measured over the non-overlapping 10-bar grid bars where the forecast is above 0. The t is computed with cases on the same day pooled.
- Supporting check: The mean unusual 10-bar move over those same grid bars is above 0.
- Confirm: The slope has t >= 2 and the mean unusual move is above 0.
- Reject: The slope has t <= -2 (deeper stretches are followed by smaller or more negative 10-day moves than shallow ones).
- Inconclusive: The slope has t between -2 and 2. A slope with t >= 2 together with a mean unusual move at or below 0 is also inconclusive. Fewer than 30 non-overlapping grid cases with a forecast above 0, pooled over coins and windows, is inconclusive whatever the result.
