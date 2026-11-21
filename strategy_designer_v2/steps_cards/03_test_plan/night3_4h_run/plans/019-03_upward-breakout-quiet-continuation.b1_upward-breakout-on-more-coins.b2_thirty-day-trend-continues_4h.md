---
idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: ad5059559106
---
Fidelity:
- Situation: a coin's 30-day return, the higher the stronger -> kept
- Comparison: higher past returns against lower ones, with longs refused after a monthly fall -> kept
- Outcome: the coin rises more over the next three days -> kept
- Verdict transfer: yes: the forecast is the coin's own 30-day return, long in proportion and flat after a fall, and it is judged on the 3-day move that follows.
Forecast: The forecast is the coin's percent change over the last 180 bars (30 days of 4h bars). It is standardised against its own last 180 values, so an average-sized move reads about 10. It is then clipped at 0. The forecast is positive and grows in proportion to the size of the past-month rise, up to the cap of 20. It is zero whenever the coin has fallen over the month, and it is never negative.
Config: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b2_thirty-day-trend-continues_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Sample each window on a non-overlapping 18-bar grid, for every coin. Regress the coin's 18-bar forward return, minus its mean 18-bar return over all windows (the drift from holding), on the bar's forecast. Pool all coins and windows and estimate the slope's t.
- Supporting check: none
- Confirm: The slope is positive with t >= 2, over at least 300 grid cases with forecast > 0.
- Reject: The slope is negative with t <= -2, over at least 300 grid cases with forecast > 0.
- Inconclusive: Any t between -2 and 2, including a slope near zero. Also any result with fewer than 300 grid cases with forecast > 0.
