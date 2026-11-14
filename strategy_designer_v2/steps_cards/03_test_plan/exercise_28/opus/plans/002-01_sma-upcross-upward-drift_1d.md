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
- Situation: the short average has crossed above the long average -> adapted: "after the cross" becomes "while SMA50 is above SMA200", graded by the size of their spread.
- Comparison: compared with random points -> kept: measured against simply holding the coin, using its mean return over all windows together.
- Outcome: price keeps rising over the next bars, more often and further -> kept: the forward return and the share of rising periods while long.
- Verdict transfer: yes: both changes are allowed adaptations (on/off made graded, "after" made "while"), and the direction and the comparison are measured as the idea states them.
Forecast: The forecast is the percent spread of SMA50 over SMA200 on daily closes. It is divided by the mean absolute spread of the previous 200 bars, times 10, capped at 20. It is then clipped at 0, because the idea is only about upward crosses. It is zero while SMA50 is below SMA200. Above SMA200 it is positive and grows as the short average pulls further above the long one. It is close to zero just after a cross and reaches its largest values in a well-established uptrend.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The 20-bar forward return of the coin, weighted by the position (forecast/10), minus the same position times the coin's mean 20-bar return over all 24 windows pooled. Pool across coins, use non-overlapping 20-bar blocks, and compute a t-statistic.
- Supporting check: Compare the share of 20-bar blocks with a positive return while the forecast is above 0 against the share over all blocks pooled. Use a two-proportion z-test.
- Confirm: The mean excess position-weighted 20-bar return is positive with t ≥ 2.
- Reject: The mean excess is negative with t ≤ -2, meaning moves after upward crosses reverse.
- Inconclusive: Any t strictly between -2 and 2 is inconclusive. So is a sample of fewer than 30 non-overlapping 20-bar blocks with a forecast above 0, pooled across coins.
