---
idea: 002-04_price-downcross-long-sma-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: Short-only distance below the long moving average. Take the percent distance of the close from its 200-bar simple moving average, (close − SMA200) / SMA200 × 100, which includes the current close. Divide it by the mean absolute value of its previous 200 values (at least 50 required) and multiply by 10, capped at ±20. Clip the result at a maximum of 0. When the close is above its SMA200 the forecast is 0 (flat). When the close is below it, the forecast is negative and grows smoothly with how far price sits below the average: −10 at an average-sized distance, down to −20 at twice that or more. It is never positive.
Config: 002-04_price-downcross-long-sma-drift_1d_config.json
Confirm: The horizon is 10 bars, sampled at non-overlapping 10-bar blocks and pooled over the 6 windows, before costs. On blocks that start with a forecast below 0, BTC's forward 10-bar return minus that window's mean 10-bar return (the buy-and-hold drift) is negative on average, with a t-statistic of −2 or lower, over at least 20 such blocks. Supporting check: more than 55% of those blocks have a negative excess return.
Reject: The mean excess forward 10-bar return on short-active blocks is zero or positive, meaning price after closes below the SMA200 falls no further than at random points, or rebounds.
Inconclusive: The mean excess is negative but its t-statistic lies between −2 and 0. Also inconclusive: fewer than 20 non-overlapping short-active blocks exist across the 6 windows. Also inconclusive: the main measure confirms but the hit rate is 55% or lower.
Deviation: "After price crosses below the long average" becomes "while price is below the long average". The config cannot tell a fresh cross from a long stay below the average. The size also grows with depth below the average, not with how recent the cross is. So the test credits any persistence of moves below the SMA200, not only what follows the crossing bar. The 200-bar SMA is the conventional daily long average; the brief does not name a period.
