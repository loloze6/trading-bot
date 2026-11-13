---
idea: N3-03_calm-uptrend-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: 20-day volatility low against its own recent history, and 20-day return positive -> adapted: low volatility is kept as an on/off condition in the regime, and "return positive" is made graded by the size of the positive 20-day return.
- Comparison: volatility against its own recent history -> kept: the regime ranks 20-day volatility within its last 100 values.
- Outcome: price drifts up over the next five days -> kept: the long position is measured on the 5-bar forward return, against holding the coin.
- Verdict transfer: yes: the test is long only in calm, rising bars and flat in calm, falling ones, so a drift up confirms the idea and a drift down rejects it.
Forecast: The regime uses VolatilityPercentileRegimeComponent (vol_period 20, lookback_period 100, smooth_period 1, so the rank is not smoothed). This is the rank of today's 20-day volatility among its last 100 values. When the rank is at or below 0.5 (volatility in the lower half of its recent history), the bar is "trending" and the idea is active. Every other bar is flat. In the active regime, the forecast is the 20-day percent return (PriceEvolutionComponent, period 20), divided by its own recent mean absolute value (standardise, window 60, min_periods 20), then clipped at 0. It is zero when the 20-day return is zero or negative. It is positive when the return is positive, and it grows with the size of the return, capped at +20. It is never short.
Config: N3-03_calm-uptrend-drift_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On bars with a forecast above 0, take the coin's 5-bar forward return minus its mean 5-bar return over all windows together. Pool these across coins and use non-overlapping 5-bar blocks for the t-statistic. Judge before costs.
- Supporting check: Regress the same excess 5-bar forward return on the forecast size across long bars. The slope should be positive.
- Confirm: The mean excess 5-bar return on long bars is above 0, with t ≥ 2 on non-overlapping blocks.
- Reject: The mean excess 5-bar return on long bars is below 0, with t ≤ -2 on non-overlapping blocks.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is any result with fewer than 30 non-overlapping 5-bar long cases pooled across coins.
