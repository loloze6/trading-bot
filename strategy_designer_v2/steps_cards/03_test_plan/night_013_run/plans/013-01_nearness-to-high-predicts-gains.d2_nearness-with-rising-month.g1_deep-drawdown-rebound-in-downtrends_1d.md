---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's 30-day return is negative, and its close sits some distance below its highest close of the past 60 days -> kept: a regime rule on the 30-bar return below 0, and the percent distance below the 60-bar closing high.
- Comparison: the farther below the high, against closer to it -> kept: the position grows with the depth below the high and is near zero at the high.
- Outcome: a higher return over the next 7 days, the deeper the fall -> kept: the 7-bar forward return.
- Verdict transfer: yes: the test measures the stated relation, on the stated condition and horizon, for each coin's own bars.
Forecast: A regime rule checks the 30-bar price change (PriceEvolutionComponent, period 30). When it is below 0, the regime is mean_reversion. On every other bar the regime is unknown, which is set to null, so the forecast is 0. In the mean_reversion regime, the forecast comes from one component, DistanceFromHighComponent with period 60. This is the percent distance of the close below its 60-bar closing high, and it is 0 or negative. It is standardised against its own past 60 values (min_periods 20), which gives a value from -20 to 0. It is then negated, so the forecast runs from 0 to +20. The forecast is 0 at a new 60-day high and grows with the depth below the high, so the position is long only. It is never negative: a coin near its high after a down month is not held, rather than shorted.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: The sample is the bars in the mean_reversion regime, taken on a non-overlapping 7-bar grid in each window and pooled over coins and windows. On these bars, regress the coin's 7-bar forward excess return on the forecast and report the slope's t. The excess return is close[t+7]/close[t]-1 minus that coin's mean 7-bar return over all windows.
- Supporting check: On the same regime bars, the top third by forecast (the deepest below the high) has a mean 7-bar excess return above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less, meaning deeper falls are followed by lower excess returns.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with the supporting check failing is also inconclusive. The test needs at least 100 independent regime grid cases; with fewer, the result is inconclusive.
