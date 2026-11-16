---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above its 200-day average, with a strong rise toward its 20-day high -> adapted: "above 200-day SMA" is a regime gate, and the rise is graded by where the close sits in its 20-day range (upper half only).
- Comparison: none -> kept
- Outcome: larger rise over the next 5 days -> kept
- Verdict transfer: yes: the test measures whether, above the 200-day SMA, closes nearer the 20-day high are followed by larger 5-day rises, which is the idea as stated.
Forecast: The forecast is active only while the close is at or above its 200-day SMA, measured by MovingAverageDistance(200, sma) ≥ 0. On every other bar it is 0. While active, it is the close's position in its 20-day closing range (Donchian, period 20), standardised over its own past 60 values. The lower half of the range is clipped to 0. So the forecast is 0 when the close is at or below the middle of its 20-day range. It grows steadily to about +10–20 as the close reaches the 20-day high. It is never negative.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Take bars where regime is trending, on the non-overlapping 5-bar grid of each window. Regress each coin's 5-bar forward return, minus that coin's mean 5-bar return over all windows, on the forecast. The measure is the pooled slope and its t-statistic.
- Supporting check: none
- Confirm: the slope is positive with t ≥ 2.
- Reject: the slope is negative with t ≤ -2.
- Inconclusive: any t between -2 and 2 is inconclusive, as is fewer than 100 independent grid cases with regime trending and forecast > 0.
