---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Forecast: One graded, long-only trend reading on daily bars, using the classic 50/200 "golden cross" pair. The raw value is the spread between the two simple averages: (SMA50 − SMA200) / SMA200 × 100. It is standardised against its own past 200 values (min_periods 50): the latest spread is divided by the mean absolute spread of the previous 200 bars and multiplied by 10, with a cap of ±20. It is then clipped at 0. The forecast is positive while SMA50 is above SMA200, which is the state that follows an upward cross. It grows as the short average pulls further above the long one. It is zero while SMA50 is at or below SMA200, so a downward cross closes the position.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Confirm: Horizon: 20 bars. Each window is cut into non-overlapping 20-bar blocks, so overlapping returns are counted once. For each block, record BTC's forward return from the forecast at the block's first bar, pooled over all 6 windows. The idea is confirmed if two things hold. First, the mean forward return of blocks that start with a forecast above 0 exceeds that of blocks that start flat by at least 2 percentage points, with a Welch t-stat of at least 2 and at least 8 blocks on each side. Second, as a supporting check, the share of positive long blocks is higher than the share of positive flat blocks.
Reject: The idea is rejected if long blocks average no more than flat blocks (difference ≤ 0), or if long blocks are positive less often than flat blocks. The second case means that moves after an upward cross reverse and the cross marks exhaustion.
Inconclusive: Either side has fewer than 8 blocks. Or the difference is positive but below 2 points, or has a t-stat below 2.
Deviation: The idea says "after an upward cross". The config tests "while SMA50 is above SMA200", sized by how far apart the averages are. The largest positions therefore come well into an established trend, not at the cross itself. Only the long side is tested; the brief's downward cross is used only as the exit. Settings are the 50/200 convention, so with 122-bar windows there are few crosses and most evidence comes from states inherited from the warm-up.
