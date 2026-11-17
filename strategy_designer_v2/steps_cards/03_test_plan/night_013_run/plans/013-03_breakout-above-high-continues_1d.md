---
idea: 013-03_breakout-above-high-continues
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 70a362722b07
---
Fidelity:
- Situation: a coin closes above its prior 52-week high -> adapted: the on/off break becomes graded, as the percent distance of the close above the prior 365-bar high, 0 when the close is below it.
- Comparison: the further above that high, the larger the return -> kept: the size of the forecast grows with the distance above the high.
- Outcome: a larger return over the next 30 days -> kept: the 30-bar forward return from break bars, measured against that distance.
- Verdict transfer: yes: the test measures the same break, distance and 30-day return, with only the break made graded.
Forecast: The forecast uses one indicator, DistanceFromHighComponent with period 365, source "high", exclude_current 1 and form "percent". It measures the percent distance of the close from the highest high of the prior 365 bars, with bar t excluded. Standardise rescales it by the mean absolute distance over its past 365 values, and a clip at min 0 then keeps only closes above that high. The forecast is 0 whenever the close is at or below the prior 52-week high. Above that high it is positive, and it grows in proportion to how far the close has cleared the high. It is long only and never negative. min_allocation_change is lowered to 0.05 so that small breaks still trade.
Config: 013-03_breakout-above-high-continues_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: The sample is the bars on each window's non-overlapping 30-bar grid where the forecast is above 0. On those bars, take the coin's 30-bar forward return minus its mean 30-bar return over all windows. The measure is the OLS slope of that excess return on the forecast, with its t and the number of cases.
- Supporting check: On the same bars, the mean excess 30-bar return (break bars minus holding the coin) is above 0.
- Confirm: The slope t is 2 or more and the mean excess return on break bars is above 0, with at least 30 cases.
- Reject: The slope t is -2 or less, with at least 30 cases.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A slope t of 2 or more with a mean excess return of 0 or less is also inconclusive. Any result with fewer than 30 grid bars where the forecast is above 0 is inconclusive.
