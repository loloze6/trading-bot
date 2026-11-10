---
idea: 002-04_price-downcross-long-sma-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Forecast: Short only, graded. The indicator is the percent distance of the close from its 200-bar simple moving average, (close − SMA200) / SMA200 × 100, which is a common convention for "the long average". It is standardised against its own previous 200 values (at least 50 needed): the latest value is divided by the mean absolute value of those past values, times 10, capped at ±20. The result is then clipped at a maximum of 0. While the close is below its SMA200, the forecast is negative, and the short grows larger the further price sits below the average relative to its usual distance. It is about −10 at a typical distance and reaches −20 at twice that distance or more. While the close is at or above the SMA200, the forecast is 0 and the position is flat.
Config: 002-04_price-downcross-long-sma-drift_1h_config.json
Confirm: The horizon is 24 bars. Sample BTC's forward 24-bar log return every 24 bars, so returns do not overlap, and pool the samples across the 6 windows. On sampled bars where the forecast is below 0, the mean forward return minus the unconditional mean of all sampled bars in the same windows is negative with t ≤ −2. Supporting check: the strategy's before-cost equity, which is short-only and so shows the difference from simply holding, ends above its start in at least 4 of the 6 windows.
Reject: The pooled difference is ≥ 0, meaning BTC falls no more after it goes below its SMA200 than at random points. A positive difference with t ≥ +2 would mean reversal: the cross marks exhaustion, not the start of a trend.
Inconclusive: The pooled difference is negative but with t between −2 and 0. The difference is also inconclusive if it meets t ≤ −2 while the supporting check holds in fewer than 4 of the 6 windows.
Deviation: The idea is "after the close crosses below the long average" and refers to the fresh cross event. The config tests "while the close is below the SMA200", sized by how far below it is. It holds the short for the whole time price stays below the average, not only in the bars after the cross. Its size is largest when price is deep below the average, which is usually well after the cross, not at the cross itself.
