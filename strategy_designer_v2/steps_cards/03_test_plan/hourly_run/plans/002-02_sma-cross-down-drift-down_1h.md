---
idea: 002-02_sma-cross-down-drift-down
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA has crossed below long SMA -> adapted: "after the cross" becomes "while short SMA is below long SMA", graded by the size of the gap.
- Comparison: price moves after random points -> kept: compared against the coin's own average move over all bars.
- Outcome: price keeps falling over the following bars -> kept: forward return measured on the short side.
- Verdict transfer: yes: the post-cross bars are exactly the bars where the short average sits below the long one, so persistent falls there confirm the idea and their absence rejects it.
Forecast: The config computes the SMA50 minus SMA200 spread as a percent of SMA200 on hourly closes. It standardises that spread against its own past 200 values and clips it at a maximum of 0. The forecast is negative (short) only while the 50-bar SMA is below the 200-bar SMA. The short position grows smoothly with how far the short average sits under the long one, up to -20. The forecast is 0 whenever the short average is at or above the long one. 50/200 is the standard SMA cross convention, since the brief gives no periods.
Config: 002-02_sma-cross-down-drift-down_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The record is split into non-overlapping 24-bar blocks, pooled over the 6 windows. - For each block, take the forecast/10 at its first bar and multiply it by the block's forward 24-bar BTC return minus that window's mean 24-bar return. This is the excess over the market's own drift. - The measure is the t-stat of the mean of these products, before costs.
- Supporting check: For active blocks (forecast < 0), compare the share whose forward 24-bar excess return is negative against 50%.
- Confirm: The main-measure t-stat is ≥ 2, meaning short positions gain beyond the coin's drift and gain more when the gap is larger.
- Reject: The t-stat is ≤ -2, meaning moves after down-crosses reverse relative to drift (the exhaustion reading).
- Inconclusive: A t-stat strictly between -2 and 2 neither confirms nor rejects. Any result is also inconclusive if there are fewer than 100 non-overlapping active blocks (forecast < 0) across the 6 windows.
