---
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the last hour's move times the coin's 24-hour volatility over its 30-day average -> kept
- Comparison: the 24-hour volatility against its 30-day average -> kept
- Outcome: over the next 4 hours the coin moves against the last hour's move, more as the product grows -> kept
- Verdict transfer: yes: the forecast is the idea's product with its sign flipped, so a graded fade either earns over 4 hours or it does not.
Forecast: The forecast starts from one input, `RecentToPriorVolatilityWeightedReturnComponent` with period 1, vol_period 24, base_period 720 and base_lag 0. Its raw value is the last hour's return in percent times the ratio of two volatilities: the standard deviation of the last 24 hourly returns over the standard deviation of the last 720 hourly returns. It is standardised over its past 500 values (min_periods 120), then negated. The forecast is positive (long) after a down hour and negative (short) after an up hour. It is near 0 after a flat hour. Its size grows linearly with the move and with the volatility ratio, capped at ±20. No regime is used, so it applies on every bar.
Config: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d3_four-hour-fade-of-extreme-hours_1h_config.json
Criterion:
- Horizon: 4 bars
- Main measure: Sample the bars at positions 0, 4, 8, ... of each window, on every coin. At each sampled bar, compute the coin's 4-bar forward return close[t+4]/close[t]-1. Subtract the coin's mean 4-bar return over all its windows, so the market's own rise is not credited. Regress this excess return on the bar's `forecast`, pooled over coins and windows, and read the slope and its t.
- Supporting check: Take the sampled bars in the top fifth of |forecast|. The mean of sign(forecast) x excess 4-bar return over them must be above 0.
- Confirm: The slope is positive with t ≥ 2 and the supporting check passes.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any other result is inconclusive: a t between -2 and 2, or a slope with t ≥ 2 whose top-fifth mean is not above 0. The test needs at least 1000 non-overlapping sampled bars with a non-zero forecast; with fewer, the result is inconclusive.
