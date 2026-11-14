---
idea: N1-01_trend-with-rising-month
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above its 200-day average and above its close of 20 bars earlier -> adapted: both conditions kept as a regime rule, and the size is graded by how far each is above zero.
- Comparison: rise beyond the coin's average 20-bar return -> kept: forward 20-bar return judged against the coin's mean 20-bar return over all windows.
- Outcome: the coin keeps rising over the next 20 bars -> adapted: the 20-bar hold is dropped; the long is held while the situation lasts, and is judged at a 20-bar horizon.
- Verdict transfer: yes: the regime is exactly the idea's two conditions, and the forward 20-bar excess return is exactly its outcome.
Forecast: Two regime measures are computed on every bar: - the percent distance of the close from its 200-day SMA (current close included); - the 20-bar percent return. When both are at or above 0, the bar is in "trending" and the forecast is the equal-weight mean of two parts: - the 20-bar return, standardised over 60 bars (min 20), clipped at 0; - the SMA-200 distance, standardised over 200 bars (min 50), clipped at 0. The forecast is never negative. It grows as the momentum and the height above the long average grow. On every other bar the regime is null and the forecast is 0: flat when the price is below the average, or above it but sliding.
Config: N1-01_trend-with-rising-month_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The forward 20-bar return after bars with a forecast above 0, minus the coin's mean 20-bar return over all test windows together. Cases are pooled across coins, with non-overlapping 20-bar blocks counted once. The test statistic is a t-stat.
- Supporting check: Within active bars, the slope of the forward 20-bar excess return on forecast size, using non-overlapping blocks. A positive slope is expected.
- Confirm: Mean excess forward 20-bar return is above 0 with t ≥ 2.
- Reject: Mean excess forward 20-bar return is below 0 with t ≤ -2. This means moves above the rising long average reverse, or lag the coin's average.
- Inconclusive: Any t between -2 and 2, including estimates near zero, is inconclusive. Fewer than 30 non-overlapping active 20-bar cases pooled is also inconclusive.
