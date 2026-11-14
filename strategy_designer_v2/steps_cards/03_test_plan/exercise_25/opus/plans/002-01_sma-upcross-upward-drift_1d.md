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
- Situation: short moving average has crossed above long moving average -> adapted: "after the cross" made "while short SMA is above long SMA", graded by the spread.
- Comparison: rise more often and further than after random points -> kept: forward returns while long are compared with the coin's unconditional forward returns.
- Outcome: price keeps rising over the following bars -> kept: the coin's forward return over the horizon while the forecast is positive.
- Verdict transfer: yes: the spread is positive exactly on the bars that follow an upward cross until the reverse cross, so the persistence after crosses is what is measured.
Forecast: The forecast is the percent spread of the 50-day SMA over the 200-day SMA (the conventional daily golden-cross pair). It is standardised against its own past 200 values and clipped at 0, so the strategy is long only, as the idea concerns the upward cross. It is 0 when the 50-day is below the 200-day. It turns positive from the upward cross and grows as the short average pulls further above the long one, capped at 20.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Take non-overlapping 10-bar blocks, pooled over the 6 windows. Compare the mean forward 10-bar log return of BTC in blocks starting with forecast > 0 against the mean over all blocks (random points). Use a t-statistic on the difference.
- Supporting check: The slope of the forward 10-bar return on the forecast size at block starts should be positive.
- Confirm: Long-block mean return exceeds the all-block mean with t >= 2, and the share of positive long blocks exceeds the all-block share.
- Reject: Long-block mean return is below the all-block mean with t <= -2, which means moves after crosses reverse.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is fewer than 20 non-overlapping blocks with forecast > 0 across the windows.
