---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA has crossed above the long SMA -> adapted: "after the up-cross" made "while the short SMA is above the long one", sized by their percent gap.
- Comparison: random points -> kept: judged against the coin's unconditional forward return, which is the same as simply holding the coin.
- Outcome: price keeps rising, more often and further -> kept: the forward return of the coin while the forecast is long.
- Verdict transfer: yes: the trend persists after an up-cross exactly when it persists while the short average stays above the long one, so both verdicts carry over to the idea.
Forecast: The forecast uses one indicator, the percent spread of the 50-day SMA over the 200-day SMA. This is the golden-cross convention on daily bars. The spread is standardised against its own past 200 values and clipped at 0. The forecast is positive while the 50-day SMA is above the 200-day SMA and grows with the gap between them, up to a cap of +20. It is zero when the 50-day SMA is at or below the 200-day SMA, because a down-cross ends the trend and the idea is about up-crosses only. It is never negative.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The coin's 10-bar forward return from the starts of non-overlapping 10-bar blocks where the forecast is > 0, minus the mean 10-bar forward return over all blocks (random points). It is measured before costs, pooled over the 6 windows.
- Supporting check: The share of long blocks with a positive 10-bar return, against the share over all blocks. As a second view, the slope of the 10-bar forward return on the forecast size at the block start should be positive.
- Confirm: The mean excess 10-bar return in long blocks is > 0 with t >= 2 on the non-overlapping blocks. The hit rate in long blocks is above the unconditional hit rate. The excess is positive in at least 4 of the windows that contain long blocks.
- Reject: The mean excess 10-bar return in long blocks is <= 0. A negative excess with t <= -2 means reversal: the cross marks exhaustion, not a trend.
- Inconclusive: An excess > 0 with t between 0 and 2, or confirming numbers carried by a single window. The test is also inconclusive with fewer than 20 non-overlapping 10-bar long blocks, or with fewer than 2 windows containing long blocks.
