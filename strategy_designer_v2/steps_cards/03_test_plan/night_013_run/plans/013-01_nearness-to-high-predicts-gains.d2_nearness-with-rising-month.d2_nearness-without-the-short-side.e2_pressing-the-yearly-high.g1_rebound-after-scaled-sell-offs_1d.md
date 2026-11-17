---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin's one-day fall -> kept: the one-bar return, negated, with rises clipped to zero.
- Comparison: the fall in units of its own 30-day daily volatility -> kept: the return over the standard deviation of the last 30 daily returns.
- Outcome: a larger rebound (rise) over the next 3 days -> adapted: the 3-day holding is dropped from the position but kept as the criterion's 3-bar horizon.
- Verdict transfer: yes: the forecast grows with the volatility-scaled fall, and the criterion tests whether the following 3-bar rise grows with it.
Forecast: One indicator, `VolatilityScaledReturnComponent` (period 1, vol_period 30). It is the latest daily return divided by the coin's 30-day daily volatility. It is standardised against its own past 60 values, then negated, then clipped at 0. The forecast is zero on up days. It is positive after a down day and grows in proportion to the size of the fall in usual moves, up to the cap of 20. It is long only, as the idea buys sell-offs. There is no dead zone, because the idea states a graded relation over all falls.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The slope of a regression of the coin's excess 3-bar forward return on the bar's forecast. - The excess return is close[t+3]/close[t]-1 minus that coin's mean 3-bar return over all windows. - The sample is the non-overlapping grid of bars 0, 3, 6, ... of each window, pooled over coins and windows.
- Supporting check: On grid bars with forecast > 0, the mean excess 3-bar return is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less, meaning larger volatility-scaled falls are followed by smaller excess 3-bar returns.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. A positive slope whose supporting check fails is also inconclusive. The test needs at least 200 grid bars with forecast > 0; with fewer, the result is inconclusive.
