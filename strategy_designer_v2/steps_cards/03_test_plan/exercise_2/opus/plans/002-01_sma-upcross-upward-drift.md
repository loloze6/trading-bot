---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 002-01_sma-upcross-upward-drift_config.json
Confirm: Horizon is 20 bars. Look at bars where the forecast is above 0, that is, where SMA50 is above SMA200. On those bars, the mean 20-bar forward return of BTC and the share of positive 20-bar forward returns must both exceed the same figures over all bars (random points). The gap in mean return must be at least 2 standard errors, counted on non-overlapping 20-bar blocks. Before costs, the portfolio must also beat exposure-matched holding, that is, the average allocation times buy-and-hold, over the same 20-bar blocks.
Reject: The theory is rejected if any of these holds: - The 20-bar forward return on bars with a positive forecast is at or below the all-bar mean. - Its hit rate is no higher than the all-bar hit rate. - The 20-bar forward return after the first bars of each positive episode (the fresh upward crosses) is below the all-bar mean, meaning moves reverse after the cross. - The portfolio trails exposure-matched holding before costs.
Inconclusive: These results neither confirm nor reject the idea: - Positive-forecast bars beat random points, but by less than 2 standard errors. - Mean and hit rate disagree. - The excess comes from only one or two of the roughly ten 50/200 upward crosses in the BTC daily history, too few episodes to separate trend persistence from a few large bull runs.
Deviation: The idea says "after the short average crosses above the long one, for the following bars". The config tests something different: "while SMA50 is above SMA200, long in proportion to the gap between them". Three things change: - The position is largest well into a mature trend, not right after the cross. - The position stays on for the whole time the averages stay crossed, not for a fixed number of bars. - The short side of the brief (the downward cross) is left out, because the idea names only the upward cross.
