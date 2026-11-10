---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: The percent spread between the 50-day and the 200-day simple moving averages of the close, (SMA50 − SMA200) / SMA200 × 100, computed at each daily close. It is divided by the mean absolute spread of the 200 bars before it and multiplied by 10, then capped at +20. It is then floored at 0, because the idea concerns only the upward cross. The forecast is zero while SMA50 is at or below SMA200. It turns positive as soon as SMA50 crosses above SMA200. It grows continuously as the short average pulls further above the long one: about 10 at a typical gap, up to 20 at twice that gap. It never goes short.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Confirm: Use one horizon of 20 bars, sampled on non-overlapping 20-bar blocks inside each window, about 36 blocks pooled over the 6 windows. Regress the coin's 20-bar forward return on the forecast at the block's first bar. The idea is confirmed if the slope is positive with t ≥ 2. The supporting check: blocks that start with a positive forecast close up at least 5 percentage points more often than all blocks. Because the comparison is with all blocks, the coin's own drift is not credited to the idea.
Reject: The idea is rejected if the slope is zero or negative. A slope ≤ 0 with t ≤ −2 also means that moves after upward crosses tend to reverse.
Inconclusive: A positive slope with t between 0 and 2. Or fewer than 8 of the blocks start with a positive forecast, so too few cross states are observed to judge.
Deviation: "After an upward cross" becomes "while SMA50 is above SMA200, sized by how far above". The test measures persistence over the whole time the short average stays above the long one, not only on the bars just after the cross. The price-crosses-the-long-average variant and the short side, which the brief mentions, are not tested.
