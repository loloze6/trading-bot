---
idea: 002-01_sma-golden-cross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a short moving average of the close has crossed above the long one -> adapted: "after the cross" made "while the 50-day SMA is above the 200-day SMA", graded by their percent spread.
- Comparison: price after random bars -> kept: forward returns on long bars are judged against all bars of the same coin and window, i.e. against holding it.
- Outcome: price keeps rising, more often and further -> kept: the coin's forward return over the next 10 bars, measured both in size and in hit rate.
- Verdict transfer: yes: a positive excess of position-weighted forward returns over holding is what "rises more often and further after up-crosses" predicts, and a significant shortfall is the reversal the brief names as its refutation.
Forecast: The forecast is the percent spread of the 50-day SMA over the 200-day SMA of the close. It is standardised against its own past 200 values (average absolute value about 10, capped at 20) and clipped at 0, so it is long-only, because the idea concerns upward crosses only. It is zero while the 50-day SMA is below the 200-day SMA. It starts near zero at the up-cross and grows smoothly as the short average pulls further above the long one.
Config: 002-01_sma-golden-cross-upward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The forecast-weighted mean 10-bar forward return of the coin, minus the mean 10-bar forward return over all bars of the same coin and window (the excess over holding). It is pooled across coins and windows, using non-overlapping 10-bar blocks, before costs.
- Supporting check: The share of positive-forecast bars whose 10-bar forward return is positive, minus the same share over all bars.
- Confirm: The excess is positive with t >= 2 across the non-overlapping blocks, and the supporting hit-rate difference is positive.
- Reject: The excess is negative with t <= -2, meaning moves after up-crosses underperform holding or reverse.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is any result built on fewer than 30 non-overlapping 10-bar blocks with a positive forecast, pooled across coins and windows.
