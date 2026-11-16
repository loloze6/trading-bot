---
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin's one-day rise relative to the standard deviation of its daily returns over the past 20 days -> kept
- Comparison: the larger the scaled rise, the larger the further rise -> kept
- Outcome: further rise over the next 5 days -> adapted: holding period dropped; the forecast is judged against the coin's following 5-bar return.
- Verdict transfer: yes: the forecast is the idea's own quantity, and the test reads the idea's own 5-day outcome.
Forecast: One indicator, VolatilityScaledReturnComponent (period 1, vol_period 20). It is today's return divided by the standard deviation of the last 20 daily returns. It is standardised over its past 60 values and then clipped at 0, so only rises count. The forecast is 0 on a down day. On an up day it is positive and grows in proportion to how many usual moves the rise was, capped at 20. There is no dead zone, because the idea claims a steady relation across all sizes of rise.
Config: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use bars with forecast > 0 on the non-overlapping 5-bar grid of each window, pooled over coins and windows. Regress each bar's excess return on its forecast and take the slope's t. The excess return is the coin's 5-bar forward return minus that coin's mean 5-bar return over all windows.
- Supporting check: Compare the top fifth of positive forecasts with the bottom fifth, on the same grid. Their mean 5-bar excess return difference (top minus bottom) must be > 0.
- Confirm: Slope t >= 2 and the supporting check passes.
- Reject: Slope t <= -2.
- Inconclusive: Either of these: - slope t between -2 and 2; - slope t >= 2 while the supporting check fails. At least 300 independent positive-forecast cases are needed; with fewer, the result is inconclusive.
