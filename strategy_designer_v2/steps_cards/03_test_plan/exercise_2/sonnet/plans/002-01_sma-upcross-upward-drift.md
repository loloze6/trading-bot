---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 002-01_sma-upcross-upward-drift_config.json
Confirm: Over a 20-bar (20-day) horizon, the forecast at each bar's close times the next 20-bar BTC return is positive, and the gain grows with position size: bars in the top tercile of forecast (long) earn a higher mean 20-bar forward return than bars in the bottom tercile (short), and the strategy's pre-cost return beats buy-and-hold BTC, or its excess over a 0.5-beta-adjusted hold is positive.
Reject: Mean 20-bar forward return after bars with the largest positive forecasts is no higher than the unconditional mean 20-bar BTC return, or the forecast-times-forward-return relation is zero or negative (moves reverse after the cross). Pre-cost portfolio return does not beat buy-and-hold on a beta-adjusted basis.
Inconclusive: The forecast-return relation is positive but the sample of independent 20-day windows is too small to separate from zero, or the strategy beats buy-and-hold only through the long-side drift while the short side loses (the edge is just market beta).
Deviation: The idea is about the event of an upward cross (short SMA over long SMA). The config instead holds a position proportional to the spread of the 50-bar SMA over the 200-bar SMA on every bar, so it is long while the short average is above the long one (growing with the gap, not only just after the cross) and short when below. It tests persistence of the cross regime, not the return right after the crossing event, and it also takes shorts after downward crosses.
