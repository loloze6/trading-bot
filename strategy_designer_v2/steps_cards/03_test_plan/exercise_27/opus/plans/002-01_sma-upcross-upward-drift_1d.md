---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a short moving average has crossed above a long one -> adapted: "after the cross" becomes "while the short SMA is above the long SMA", graded by how far apart they are.
- Comparison: random points -> kept: judged against holding the coin, using its mean return over all windows.
- Outcome: price keeps rising over the following bars, more often and further -> kept: forward return and hit rate after positive forecasts.
- Verdict transfer: yes: both changes are allowed adaptations, and a lasting rise after up-crosses must show as excess forward return while the short average stays above the long one.
Forecast: The forecast is the 50-day SMA minus the 200-day SMA, as a percent of the 200-day SMA (the conventional daily golden-cross pair). It is standardised against its own past 200 values and clipped at 0, so it is long-only, as the idea is about up-crosses. It is zero while the 50-day SMA is below the 200-day SMA. It turns positive from the up-cross and grows smoothly as the short average pulls further above the long one, up to the cap of 20.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Regress each bar's forward 10-bar return, minus the coin's mean 10-bar return over all 24 windows together, on the forecast. Pool all coins, use non-overlapping 10-bar steps (or HAC errors with lag 9), and take the t-stat of the slope.
- Supporting check: Compare the share of positive excess 10-bar returns on bars with forecast > 0 against bars with forecast = 0.
- Confirm: The slope is positive with t >= 2, and the hit rate is higher on forecast > 0 bars.
- Reject: The slope is negative with t <= -2, meaning moves reverse after up-crosses.
- Inconclusive: A t between -2 and 2 is inconclusive, as is any result with fewer than 100 non-overlapping 10-bar cases with forecast > 0 across coins.
