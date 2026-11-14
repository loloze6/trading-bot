---
idea: 002-04_price-downcross-long-sma-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close crosses below the long average after being above it -> adapted: "after the cross" made "while below", graded by the percent distance under the 200-day SMA (zero at the cross, growing as the close sits further below).
- Comparison: versus random points -> kept: forward returns on short bars are compared with forward returns over all tested bars.
- Outcome: price keeps falling, more often and further -> kept: forward 10-bar return, downward, plus the hit rate of declines.
- Verdict transfer: yes: the short-only position exists exactly while the close is below its long average after crossing it, so its forward returns against all bars answer the idea both ways.
Forecast: The 200-day SMA distance, (close - SMA200) / SMA200 x 100, divided by its own mean absolute value over the prior 200 bars, times 10 and capped at ±20. It is then clipped at a maximum of 0, so it is short only. It is zero while the close is at or above the SMA. It turns negative as soon as the close drops below the SMA and grows more negative the further the close falls below it, down to -20 (200 percent short).
Config: 002-04_price-downcross-long-sma-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On bars with forecast < 0, take the forward 10-bar BTC log return minus the mean forward 10-bar return over all tested bars (buy-and-hold baseline). Regress this excess return on the forecast before costs, using non-overlapping 10-bar blocks only so overlapping returns count once. A positive slope means that deeper short positions are followed by larger excess falls.
- Supporting check: Compare two shares on non-overlapping blocks: the share of short-bar blocks with a negative forward 10-bar return, and the same share over all blocks.
- Confirm: Slope t-statistic ≥ +2 and mean excess forward return on short bars below 0, with the supporting share of declines higher than on all bars.
- Reject: Slope t-statistic ≤ -2, meaning price rebounds after the close goes below the average, more strongly the deeper it is below.
- Inconclusive: Any t-statistic between -2 and +2 is inconclusive. So is a run with fewer than 15 non-overlapping 10-bar blocks with forecast < 0 across the 6 windows, whatever the t-statistic.
