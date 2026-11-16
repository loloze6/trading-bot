---
idea: 002-04_price-cross-below-long-sma
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin's close has crossed below its long moving average -> adapted: "after the cross" becomes "while the close is below the 200-day SMA", graded by how far below it sits.
- Comparison: compared with random bars -> kept: measured against holding the coin, using its mean return over all windows.
- Outcome: price keeps falling, more often and further -> kept: measured as the coin's forward return while the position is short.
- Verdict transfer: yes: short gains beyond holding while the close is below the long average confirm downward persistence; reliable losses reject it.
Forecast: The indicator is the percent distance of the close from its 200-day simple moving average. It is standardised over its own past 200 values, then clipped at 0 from above, so the forecast is short only. It is zero while the close is at or above the SMA200. It turns negative once the close is below the average and grows more negative the deeper the close sits under it, down to -20 (twice the usual distance).
Config: 002-04_price-cross-below-long-sma_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Split each coin's record into non-overlapping 10-bar blocks, so overlapping returns count once. For each block, take the allocation at the block's start and multiply it by the coin's 10-bar return minus 10 times the coin's mean daily return over all 24 windows together. Pool these products across coins and blocks, then compute their mean and its t-statistic, before costs.
- Supporting check: Within blocks with a nonzero position, regress the excess 10-bar return on the allocation. A positive slope (deeper short followed by further excess fall) supports the idea.
- Confirm: The mean excess gain of the short positions is positive with t >= 2.
- Reject: The mean excess gain is negative with t <= -2, meaning the coin rose beyond holding after closes below the SMA200 (a reversal).
- Inconclusive: Any t between -2 and 2 is inconclusive, including results near zero. The test also needs at least 30 non-overlapping 10-bar blocks with a nonzero position, pooled across coins; with fewer, the result is inconclusive.
