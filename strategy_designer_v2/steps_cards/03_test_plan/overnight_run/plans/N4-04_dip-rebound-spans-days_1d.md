---
idea: N4-04_dip-rebound-spans-days
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: 20-day and 60-day returns both positive, and a sharp daily drop -> adapted: the both-positive condition is a regime rule; "sharp" becomes a graded size of the one-day drop.
- Comparison: the 2-3 day rise against the first-day rise alone -> kept: the criterion compares the return over bars 2-3 with zero, which is the same as comparing the 3-day rise with the 1-day rise.
- Outcome: price rises over the next two to three days -> adapted: the holding period is dropped from the position and measured in the criterion as the forward return after the forecast bar.
- Verdict transfer: yes: the record holds the forecast and the price on every bar, so the extra rise on days 2-3 after the largest dip positions can be measured directly, in both directions.
Forecast: A regime rule marks a bar "trending" only when the 20-bar and the 60-bar price change are both above 0. Every other bar is flat. On trending bars, the forecast is the one-bar return (PriceEvolutionComponent, period 1), processed in four steps: - standardised over its past 60 values (min_periods 20); - negated, so a drop is positive; - clipped at 0, so the forecast is long only and nothing is taken on up days; - passed through signed_power with exponent 3 and pivot 10, the strongest graded dead zone. An ordinary dip gives almost no position. A drop of twice the average daily move or more reaches about +80 before the final clip to +20. The forecast is zero on up days and outside the regime, and grows with the cube of the drop's size.
Config: N4-04_dip-rebound-spans-days_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Take the bars whose forecast is in the top decile of positive forecasts, pooled over all coins and windows. For each, measure the coin's return from close t+1 to close t+3, minus the coin's mean 2-bar return over all test windows together. Report the mean of this excess and its t-statistic. Cases on the same coin within 3 bars of each other are merged into one case, so overlapping returns are counted once.
- Supporting check: The mean 3-bar excess return (close t to close t+3) after the same cases, against the coin's mean 3-bar return over all windows, should be positive.
- Confirm: The mean excess return over days 2-3 is above 0, with t ≥ 2.
- Reject: The mean excess return over days 2-3 is below 0, with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a result from fewer than 30 non-overlapping cases.
