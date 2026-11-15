---
idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the coin's 50-day SMA is above its 200-day SMA, with its own 20-day return -> kept: a regime rule on the SMA50/SMA200 spread above 0, and a graded 20-bar return.
- Comparison: higher versus lower 20-day return inside the uptrend -> kept: the position grows with the 20-bar return.
- Outcome: a larger return over the next 10 days -> kept: 10-bar forward return, long only as the consequence says (no long when the 20 days fell).
- Verdict transfer: yes: the test measures within-uptrend 10-bar returns against 20-bar momentum, exactly as the idea states.
Forecast: The regime detector computes the SMA50 minus SMA200 spread (EMASpreadComponent, average "sma", fast 50, slow 200). When the spread is above 0, the bar is "trending". Otherwise it is "unknown", which is flat. In "trending", the forecast is the 20-bar price change (PriceEvolutionComponent, period 20), standardised against its own past 60 values (target 10, cap 20), then clipped at 0. It is positive and grows with the 20-day rise. It is zero when the last 20 days fell. It is never short.
Config: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use the non-overlapping 10-bar grid of each window and keep only the bars where the SMA spread is above 0. Regress the coin's 10-bar forward return, minus that coin's mean 10-bar return over all windows, on the recorded 20-bar return. Report the t of the OLS slope.
- Supporting check: On the same cases, the mean excess 10-bar return of the bars with a positive forecast, minus that of the bars with a zero forecast, is above 0.
- Confirm: The slope t is 2 or more and the supporting difference is positive.
- Reject: The slope t is -2 or less.
- Inconclusive: A slope t between -2 and 2, or a t of 2 or more with a supporting difference of 0 or less. At least 50 independent in-regime cases are needed; with fewer, the test is inconclusive.
