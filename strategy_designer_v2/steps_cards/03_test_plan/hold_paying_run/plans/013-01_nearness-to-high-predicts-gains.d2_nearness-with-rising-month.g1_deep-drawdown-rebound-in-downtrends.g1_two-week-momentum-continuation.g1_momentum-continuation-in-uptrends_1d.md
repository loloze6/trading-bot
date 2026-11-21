---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the coin's 14-day rise, larger meaning stronger -> kept: a graded 14-bar price change, long side only.
- Comparison: only among coins whose 60-day return is positive -> kept: a regime rule on the 60-bar return, with the position flat otherwise.
- Outcome: a higher return over the next 7 days, upward -> kept: the 7-bar forward return compared with the forecast's size.
- Verdict transfer: yes: the test measures, within each coin, whether a larger 14-day rise during a positive 60-day trend is followed by a higher 7-day return.
Forecast: The regime detector computes the 60-bar percent return (PriceEvolutionComponent, period 60). When that return is above 0, the bar is "trending"; every other bar is "unknown", which is flat. In "trending", the forecast is the 14-bar percent return (PriceEvolutionComponent, period 14). It is standardised against its own last 60 values (min_periods 20) and then clipped at 0. The forecast is therefore positive and grows with the 14-day rise, from 0 at no rise to the cap of 20. It is 0 when the coin has fallen over 14 days, and 0 whenever the 60-day return is not positive. It is never short.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: This uses the bars where the regime is "trending", sampled on a non-overlapping 7-bar grid in each window and pooled across coins. On those bars, regress the 7-bar forward return minus the coin's mean 7-bar return over all windows on the forecast. The measure is the slope's t.
- Supporting check: Take the book's mean daily return before costs and remove the part that comes from the market's own rise. What remains is the timing gain, and it must be above 0.
- Confirm: The slope is positive with t of 2 or more, and the timing gain is positive.
- Reject: The slope is negative with t of -2 or less.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a positive t of 2 or more if the timing gain is 0 or below. The test needs at least 100 independent 7-bar cases in the "trending" regime, with at least 30 of them having a forecast above 0; fewer is inconclusive.
