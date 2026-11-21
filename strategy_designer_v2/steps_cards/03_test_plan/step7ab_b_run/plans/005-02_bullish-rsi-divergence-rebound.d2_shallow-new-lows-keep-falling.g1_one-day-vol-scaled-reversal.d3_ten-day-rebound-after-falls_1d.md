---
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d3_ten-day-rebound-after-falls
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin's 1-day fall, the larger the stronger -> kept
- Comparison: the fall against the coin's own 20-day daily volatility -> kept
- Outcome: the coin rises over the next 10 days, more after larger falls -> kept
- Verdict transfer: yes: the forecast is the volatility-scaled 1-day fall, held 10 days, so its gains test exactly this claim.
Forecast: The forecast comes from VolatilityScaledReturnComponent with period 1, vol_period 20, lag 0 and vol_lookback 1. Its raw value is today's 1-day return divided by the standard deviation of the last 20 daily returns. That value is standardised against its own last 60 values (min_periods 20), then negated, so a fall reads positive. It is then clipped at 0, so the book is long only and only on down days. The forecast is zero on up or flat days and positive on down days. It grows linearly with the size of the fall in usual moves, up to the cap of 20. It is ungated, with no regime condition.
Config: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d3_ten-day-rebound-after-falls_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Take non-overlapping 10-bar grid cells in each window and keep the cells where the forecast is above 0 at the cell's first bar. For each kept cell, compute the coin's 10-bar forward return minus its normal 10-bar drift (its mean over all windows). Regress that excess return on the forecast and report the t of the slope.
- Supporting check: Over the same cells, the mean excess 10-bar return is above 0.
- Confirm: The slope's t is 2 or more and the mean excess return over the cells is positive, with at least 100 cells.
- Reject: The slope's t is -2 or less, with at least 100 cells.
- Inconclusive: These results are inconclusive: - a slope t between -2 and 2; - a slope t of 2 or more with a mean excess return of 0 or below; - fewer than 100 cells with a positive forecast (about 400 are expected over 3 coins × 24 windows).
