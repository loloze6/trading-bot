---
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a sharp falling hour, sized against the coin's usual hourly volatility -> adapted: "sharp" made graded, so the long grows smoothly with the hour's fall in usual moves; "after" made "while", and the bet is held 24 bars.
- Comparison: only while 24-hour volatility is raised against its 30-day average -> kept: a regime rule turns the idea on only when the 24h volatility is above its 720-bar average (ratio of 1 or more).
- Outcome: the coin rises over the next 24 hours, more after larger falls -> kept: a long held 24 bars, sized by the fall.
- Verdict transfer: yes: the test buys exactly the falls the idea names, only in raised volatility, scaled to the fall's size, and holds for its 24-hour horizon.
Forecast: The forecast uses one return measure. It is the last hour's return (close over the previous close, minus 1) divided by the usual hourly volatility. That volatility is the 720-bar (30-day) mean of the 24-hour standard deviation of hourly returns. The measure is standardised over its past 500 values, negated so that a fall reads positive, and clipped at 0, so it is long only. A graded dead zone then applies: signed power with exponent 3 and pivot 10. Small falls give almost nothing, and sharp falls give large longs. The forecast is positive only on falling hours. It is 0 on rising or flat hours. It grows with the cube of the fall's size in usual moves, up to the cap of 20. It is active only on bars where the 24-hour volatility is at or above its 30-day average (the ratio of 24h volatility to its 720-bar mean is 1.0 or more). On every other bar the regime is null and the forecast is 0.
Config: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Each case is a bet: a rise of the forecast of at least 2 points, read once per non-overlapping 24-bar grid cell of each window. For each case, take the coin's return from the close of the signal bar over the next 24 bars, minus the coin's mean 24-bar return over all windows. The measure is the mean of this excess over all cases, pooled across coins, with its t-statistic.
- Supporting check: Split the cases at the median forecast. The mean excess return of the larger-forecast half minus that of the smaller-forecast half should be positive.
- Confirm: The mean excess return is positive with t of 2 or more, and the larger-forecast half beats the smaller-forecast half (difference above 0).
- Reject: The mean excess return is negative with t of -2 or less.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a confirming main measure whose larger-forecast half does not beat the smaller half. At least 100 independent cases are required, pooled over coins and windows; fewer is inconclusive.
