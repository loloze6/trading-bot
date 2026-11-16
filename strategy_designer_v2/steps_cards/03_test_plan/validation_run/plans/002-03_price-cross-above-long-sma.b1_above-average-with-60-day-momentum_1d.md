---
idea: 002-03_price-cross-above-long-sma.b1_above-average-with-60-day-momentum
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above its 200-day average, with a positive 60-day return -> adapted: the 200-day condition is a regime, and the 60-day return is graded from 0 (clip at 0) instead of an on/off filter.
- Comparison: more than the coin's usual drift -> kept: judged against the coin's mean 20-day return over all windows.
- Outcome: the coin rises over the next 20 days, and rises more when the 60-day return is larger -> kept: the 20-bar forward return, graded by the position size.
- Verdict transfer: yes: the forecast is long only above the 200-day SMA, scaled by the positive 60-day return, and flat elsewhere, which is exactly the idea's claim.
Forecast: A regime rule uses the percent distance of the close from its 200-day SMA. When the close is above the SMA the regime is "trending"; otherwise the regime is "unknown" and the forecast is 0 (flat). In "trending", the forecast is the 60-bar price change. It is standardised against its own past 60 values (average size about 10, cap 20) and clipped at 0. So the forecast is 0 when the 60-day return is flat or falling. It is positive and grows in proportion to the 60-day rise when that return is up, reaching at most 20, which is 200 percent long. It is never negative.
Config: 002-03_price-cross-above-long-sma.b1_above-average-with-60-day-momentum_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The sample is the bars of each window's non-overlapping 20-bar grid where the forecast is above 0. For each such case, the value is (forecast / 10) x (the coin's 20-bar forward return minus that coin's mean 20-bar return over all windows). The measure is the mean of these values and its ordinary t-statistic.
- Supporting check: Across the same cases, the OLS slope of the excess 20-bar forward return on the forecast must be above 0. This tests that a larger 60-day rise gives a larger rise.
- Confirm: The main measure has t ≥ 2.0 over at least 30 active cases, and the supporting slope is above 0.
- Reject: The main measure has t ≤ -2.0 over at least 30 active cases.
- Inconclusive: Any of the following is inconclusive: - t is between -2.0 and 2.0; - t ≥ 2.0 but the slope is ≤ 0; - there are fewer than 30 active non-overlapping cases across all coins and windows.
