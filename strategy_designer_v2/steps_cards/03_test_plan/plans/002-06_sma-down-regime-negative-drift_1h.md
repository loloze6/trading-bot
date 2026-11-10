---
idea: 002-06_sma-down-regime-negative-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
---
Forecast: Short-only, graded by the depth of the short average below the long average. Take the 50-bar and 200-bar simple moving averages of the 1h close, the most common "golden/death cross" pair. Compute the spread (SMA50 - SMA200) / SMA200 x 100. Standardise it against its own past 200 values: the latest value divided by their mean absolute value, times 10, capped at +/-20. Then clip it at a maximum of 0. The forecast is negative (short) on every bar where SMA50 is below SMA200, which is the stretch from a downward cross to the next upward cross. The short grows as SMA50 sinks further below SMA200, up to -20. The forecast is zero whenever SMA50 is at or above SMA200, and never positive.
Config: 002-06_sma-down-regime-negative-drift_1h_config.json
Confirm: Use a 1-bar horizon, so each bar's next-bar log return is counted once with no overlap. Main measure: the mean next-bar return on bars where the forecast is below 0, minus the mean next-bar return over all bars of the same window, before costs. The idea is confirmed if this excess is negative in at least 5 of the 6 windows and the pooled excess has t below -2. Supporting check: across the bars with a forecast below 0, the mean next-bar return in the third with the largest |forecast| is lower than in the third with the smallest |forecast|.
Reject: The idea is rejected if the pooled excess is 0 or positive, or if it is positive in 4 or more of the 6 windows. Positive excess means price during "short below long" stretches does no worse than the coin's own drift, or reverses upward.
Inconclusive: The result is inconclusive if the pooled excess is negative but its t is between -2 and 0. It is also inconclusive if the excess is negative in only 3 or 4 windows, or if the main measure confirms but the supporting tercile check goes the wrong way.
Deviation: The idea gives equal weight to every bar of the stretch from a downward cross to the next upward cross. The config shorts on each bar of that same stretch, which is exactly the bars where SMA50 is below SMA200. But it sizes the short by how far SMA50 sits below SMA200, so bars just after the cross, when the spread is still small, get small positions. The test therefore weights deep, established downtrends more than the onset of the trend. The 50/200 settings are convention; the brief does not give them.
