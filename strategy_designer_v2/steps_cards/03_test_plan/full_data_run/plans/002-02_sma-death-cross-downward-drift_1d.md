---
idea: 002-02_sma-death-cross-downward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the short moving average of the close has crossed below the long one -> adapted: "after the cross" becomes "while the short SMA is below the long SMA", graded by how far below it is.
- Comparison: falls more often and further than after random bars -> kept: forward returns on short-signal bars are compared with the coin's own returns on all bars.
- Outcome: price keeps falling over the following bars -> kept: the next-bar returns of the short position, measured against holding the coin.
- Verdict transfer: yes: the graded spread is the "while below" form of the downward cross, so its forward returns stand or fall with the idea.
Forecast: The forecast is the percent spread between the 50-day and 200-day simple moving averages of the close. It is standardised against its own past 200 values and then clipped at a maximum of 0, so it only ever goes short. It is zero while the 50-day SMA is above the 200-day SMA. It is negative while the 50-day is below, and the short grows as the spread widens, up to -20. It is never positive.
Config: 002-02_sma-death-cross-downward-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Split each window into non-overlapping 20-bar blocks, pooled over coins and windows. In each block, take the coin's forward 20-bar log return minus that coin-window's mean 20-bar return, so the market's own drift is removed. Regress this excess return on the forecast at the start of the block. A positive slope means more negative forecasts are followed by lower excess returns.
- Supporting check: Compare two shares: the share of blocks with a negative excess return when the forecast is below 0, and the same share across all blocks.
- Confirm: The slope is positive with t >= 2, using non-overlapping blocks with standard errors clustered by coin.
- Reject: The slope is negative with t <= -2: deeper shorts are followed by rebounds, which reads as exhaustion rather than persistence.
- Inconclusive: Any t between -2 and 2, including slopes near zero. At least 100 non-overlapping blocks with a forecast below 0 are required; fewer is inconclusive.
