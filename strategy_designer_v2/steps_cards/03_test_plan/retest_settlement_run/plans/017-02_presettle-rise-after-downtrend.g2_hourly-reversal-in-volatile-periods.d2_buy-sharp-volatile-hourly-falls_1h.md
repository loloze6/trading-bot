---
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a sharp falling hour -> adapted: a threshold made graded; the position grows with the size of the hour's fall, held while it shows, zero on rising hours.
- Comparison: the fall against usual hourly volatility, and 24h volatility against its 30-day average -> kept: the fall in 24-hour hourly volatility units, times that volatility over its 720-bar mean.
- Outcome: the coin rises over the next 24 hours, more after larger scaled falls; no short after rises -> kept: long only, held 24 bars.
- Verdict transfer: yes: the forecast is the idea's scaled fall times its volatility ratio, long only and held for its 24-hour horizon.
Forecast: The forecast is built from VolatilityScaledReturnComponent with period 1, vol_period 24 and vol_lookback 720. Its raw value is the last hour's return divided by the 24-hour standard deviation of hourly returns. That is multiplied by the ratio of that standard deviation to its mean over the last 720 bars (30 days). This equals the hour's return divided by the mean of the 24-hour volatility over 30 days. The value is standardised over its past 500 values. It is then negated, so falls read positive, and clipped at 0, so the forecast is long only and zero on rising or flat hours. Last, a graded dead zone (signed_power, exponent 3, pivot 20) keeps ordinary falls near zero. The position grows steeply with sharp falls during raised volatility. The forecast is never negative.
Config: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Each case is a bet: a rise of the forecast of at least 2 points, read once per 24-bar grid cell of each window. For each case, take the coin's 24-bar return from the signal bar's close and subtract the coin's normal 24-bar drift (its mean over all windows). The measure is the mean of these excess returns across all coins and windows, with the t of that mean.
- Supporting check: Split the cases at the median entry forecast. The mean excess return of the cases above the median, minus that of the cases below, must be above 0.
- Confirm: The idea is confirmed when the main measure's t is 2 or more with at least 30 cases, and the supporting check is above 0.
- Reject: The idea is rejected when the main measure's t is -2 or less with at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main t of 2 or more with the supporting check at or below 0 is also inconclusive. So is any result with fewer than 30 cases.
