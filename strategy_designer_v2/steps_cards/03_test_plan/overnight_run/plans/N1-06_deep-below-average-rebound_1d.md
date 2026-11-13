---
idea: N1-06_deep-below-average-rebound
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close far below its 200-day simple moving average -> adapted: "far below" becomes a graded size of the percent distance below the SMA200, with a strong graded dead zone.
- Comparison: rising rather than continuing down -> kept: the sign of the forward move is judged against the coin's own mean drift.
- Outcome: price rises over the following ten days -> kept: measured as the 10-bar forward return after long positions.
- Verdict transfer: yes: the forecast is long only while the close sits below the SMA200, and it grows with the depth, so the test measures exactly the claimed rebound.
Forecast: The forecast uses one indicator, the percent distance of the close from its 200-bar simple moving average, current close included. - It is standardised over the 200 previous values and then negated, so it is positive when the close is below the SMA200. - It is clipped at 0, so it is zero whenever the close is at or above the average. The idea says nothing about that side. - It then goes through signed_power with exponent 3 and pivot 20, the strongest graded dead zone. A typical depth gives a near-zero position (10 becomes 2.5). The position grows steeply only when the distance below the average is extreme (20 gives 20). - It is never negative, so it never adds to shorts.
Config: N1-06_deep-below-average-rebound_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The 10-bar forward return of the coin after bars where the forecast is at least 5, which are the deep-below-SMA200 cases. From it, subtract the coin's mean 10-bar return pooled over all windows (holding). Pool all coins and windows. Count overlapping returns once, either as non-overlapping 10-bar blocks or with a Newey-West t-statistic with lag 9.
- Supporting check: Across all bars with a forecast above 0, the slope of the 10-bar forward excess return on the forecast should be positive. This means the gain grows with depth.
- Confirm: The mean excess 10-bar return after forecast ≥ 5 is positive, with t ≥ 2.
- Reject: The mean excess 10-bar return after forecast ≥ 5 is negative, with t ≤ -2. That would mean price keeps falling after a deep distance below the SMA200.
- Inconclusive: Any result with -2 < t < 2 is inconclusive, including an estimate near zero. So is any result with fewer than 30 non-overlapping 10-bar cases at forecast ≥ 5, pooled over coins and windows.
