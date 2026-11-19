---
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: 14-day RSI level, higher is stronger, while the 60-day return is positive -> kept: a regime on the 1440-bar return, with the 336-bar RSI graded around 50.
- Comparison: more than the coin's usual 10-day move -> kept: the forward return is measured against the coin's mean 240-bar return.
- Outcome: the coin rises more over the next 10 days as RSI is higher -> kept: 240-bar forward return.
- Verdict transfer: yes: the test measures this RSI, in this uptrend condition, against this horizon and this baseline.
Forecast: On every hourly bar, the regime is "trending" when the 1440-bar (60-day) percent return is above 0. On all other bars the forecast is 0. On trending bars the forecast is RSI(336) minus 50: the component outputs 50 minus RSI, and `negate` flips it. It is standardised against the mean absolute value of its previous 336 values. It is positive and grows as RSI rises above 50, negative and grows as RSI falls below 50, and is capped at ±20.
Config: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1h_config.json
Criterion:
- Horizon: 240 bars
- Main measure: The cases are bars on a non-overlapping 240-bar grid in each window where the regime is trending, pooled over coins. Regress the coin's 240-bar forward return minus its mean 240-bar return (over all windows) on the forecast. The measure is the t of the slope.
- Supporting check: The trending cases in the top third of forecast must have a mean excess 240-bar return, as above, greater than 0.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: The idea is neither confirmed nor rejected when the slope t lies between -2 and 2, or when t ≥ 2 but the top-third check fails. At least 100 independent trending cases are required; with fewer, the result is inconclusive.
