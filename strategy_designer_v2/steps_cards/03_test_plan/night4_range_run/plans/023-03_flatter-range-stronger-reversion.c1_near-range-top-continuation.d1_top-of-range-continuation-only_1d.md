---
idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 10d8cbead801
---
Fidelity:
- Situation: daily close sits in the upper half of its 30-day closing range, closer to the top -> adapted: the on/off "only in the upper half" condition is made graded, with the close's position in the 30-day closing range clipped at 0 below the middle.
- Comparison: the rise grows fastest just below the 30-day high, judged against lower positions in the range -> kept: a convex (squared) grading of the range position.
- Outcome: the coin rises over the next 10 days -> kept: held 10 daily bars, long only, judged against the coin's normal drift.
- Verdict transfer: yes: the forecast is the idea's own range position, graded convexly over its own 30-day range and 10-day horizon, so a confirm or a reject carries over to the idea.
Forecast: The forecast uses DonchianBreakoutComponent with period 30 on closes, which is the close's position in its 30-day closing range, from bottom to top. It is standardised over the 60 past values (min_periods 20). It is then clipped at 0, so it is zero at or below the range's middle and never short. Finally, signed_power with exponent 2 is applied, so the size grows convexly as the close nears the 30-day high. The forecast is positive only in the upper half of the range and largest at the top. It is never negative.
Config: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use the non-overlapping 10-bar grid of each window, on the cells where the forecast is above 0. Regress the coin's 10-day return minus its normal drift (its mean 10-day return over all windows) on the forecast at the grid bar. The measure is the slope's t, with the number of cases stated.
- Supporting check: The mean excess 10-day return, weighted by the forecast, over the same cells must be above 0.
- Confirm: The slope's t is 2 or more and the weighted mean excess return is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: The slope's t lies between -2 and 2, or the t is 2 or more but the weighted mean excess return is 0 or below. Any result from fewer than 100 grid cells with a forecast above 0, across all coins and windows, is also inconclusive.
