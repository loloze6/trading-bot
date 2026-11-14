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
- Situation: short SMA has crossed above long SMA -> adapted: "after the cross" becomes "while the 50-day SMA is above the 200-day SMA", graded by the percent spread between them.
- Comparison: drift after random points -> kept: forward returns on active bars are compared with all bars and with holding the coin.
- Outcome: price keeps rising over the following bars -> kept: forward return on the long side.
- Verdict transfer: yes: the up-cross regime holding and its spread growing is the persistence the idea claims, measured long-only against random bars.
Forecast: The indicator is the percent spread between the 50-day and 200-day simple moving averages. These are the conventional golden-cross settings on daily bars. The spread is standardised against its own past 200 values, so an average spread gives about 10, capped at 20. It is then clipped at 0. The forecast is positive while the 50-day SMA is above the 200-day SMA. It grows as the short average pulls further above the long one. It is zero when the short average is below the long one. It is never negative, because the idea concerns only up-crosses.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The coin's forward 10-bar return, taken on non-overlapping 10-bar blocks and pooled over the 6 windows. Blocks that start with forecast > 0 are compared with all blocks, which stand for random points or simply holding the coin. Before costs.
- Supporting check: Regress the forward 10-bar return on the forecast at the block start, over the active blocks. A positive slope means returns grow with the size of the spread.
- Confirm: The mean forward return of active blocks exceeds the all-block mean, with Welch t ≥ 2. The share of rising blocks among active blocks also exceeds the share among all blocks. The supporting slope is ≥ 0.
- Reject: The active-block mean forward return is ≤ the all-block mean. Or the active blocks show reversal, with the difference negative and t ≤ -1.
- Inconclusive: A positive difference with t between 0 and 2 neither confirms nor rejects. So do mixed signs between the mean and the hit rate. The test is also inconclusive if there are fewer than 20 non-overlapping active blocks, or fewer than 20 inactive blocks.
