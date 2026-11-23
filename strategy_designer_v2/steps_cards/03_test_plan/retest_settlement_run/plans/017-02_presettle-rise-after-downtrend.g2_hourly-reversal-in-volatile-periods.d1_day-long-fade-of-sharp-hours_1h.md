---
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the last hour's move, measured in the coin's usual hourly volatility -> kept: the 1-bar return over the 24-hour std of hourly returns.
- Comparison: the coin's 24-hour volatility against its 30-day average -> kept: s(24h) over its 720-bar mean, multiplying the scaled move.
- Outcome: over the next 24 hours, price moves against the last hour's move -> kept: the sign is flipped and held for 24 bars.
- Verdict transfer: yes: the product measures exactly the stated move, its scale and its volatility amplifier, and is judged on the stated 24-hour reversal.
Forecast: The forecast is built from one indicator, VolatilityScaledReturnComponent with period 1, vol_period 24 and vol_lookback 720. It equals the last hour's return divided by the 30-day mean of the 24-hour std of hourly returns. This is the same as two factors multiplied together: - the move counted in current usual hourly moves; - the ratio of the 24-hour volatility to its 30-day average. The value is standardised over its past 500 values and then negated. It is negative after an up hour (short) and positive after a down hour (long). It is near zero after a small move. Its size grows with the size of the move and with how high current volatility stands against its 30-day average. It is signed and graded, and active on every bar.
Config: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Use the non-overlapping 24-bar grid of each window, with all coins and windows pooled. For each case (a grid bar with a non-zero forecast), compute forecast/10 x (the coin's 24-bar forward return minus its normal 24-bar drift over all its windows). The measure is the t of the mean of this product, before costs.
- Supporting check: On the same cases, compare the third with the largest |forecast| against the third with the smallest. The mean of sign(forecast) x excess return must be higher in the largest third (difference larger minus smaller > 0).
- Confirm: The mean product is positive with t >= 2, and the supporting check passes.
- Reject: The mean product is negative with t <= -2.
- Inconclusive: The idea is inconclusive in two cases. The first is a t between -2 and 2. The second is t >= 2 with the supporting check failing. At least 500 cases with a non-zero forecast are required; with fewer, the result is inconclusive.
