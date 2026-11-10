---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Forecast: The 50-bar simple moving average of the close minus the 200-bar simple moving average, divided by the 200-bar SMA, in percent. This is the graded form of "the short average is above the long average". The spread is standardised against its own past 200 values: it is divided by the mean absolute value of those values and multiplied by 10, capped at ±20. Negative values are clipped to 0, because the idea concerns only the upward cross. The forecast is 0 while the 50-SMA is at or below the 200-SMA. It turns positive from the bar the 50-SMA crosses above the 200-SMA. It grows in proportion to how far the 50-SMA sits above the 200-SMA, relative to the spread's usual size. It returns to 0 when the 50-SMA crosses back below. No regime is used; the forecast is active on every bar.
Config: 002-01_sma-upcross-upward-drift_1h_config.json
Confirm: The horizon is 24 bars. Take non-overlapping 24-bar blocks, one sampled every 24 bars, and pool them across the 6 windows. Main measure: the mean 24-bar forward return of the coin, before costs, on blocks that start with forecast > 0, minus the mean 24-bar forward return over all blocks. Confirm the idea if this excess is positive with t ≥ 2 and positive in at least 4 of the 6 windows. Supporting check: the Spearman rank correlation between the forecast and the forward 24-bar return, on blocks with forecast > 0, is above 0.
Reject: Reject the idea if the excess forward return on forecast > 0 blocks is ≤ 0 (pooled point estimate), or negative in at least 4 of the 6 windows. Either result means price after the up-cross does no better than at random points, or reverses.
Inconclusive: The pooled excess is positive but t < 2. Or the pooled excess is significant but positive in only 3 or fewer windows. Or the main measure confirms while the supporting rank correlation is ≤ 0. In that last case the gain does not grow with the size of the spread.
Deviation: "After an upward cross" becomes "while the 50-SMA is above the 200-SMA, sized by the spread". The position is smallest right at the cross, when the spread is near 0. It is largest once the averages have separated. So the test weights the persistence of an established trend more than the bars immediately after the cross. The 50/200 settings come from convention, since the brief gives none. The downward cross is not traded, because the idea is stated for the upward cross only.
