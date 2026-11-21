---
idea: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin with a strong 3-day run down -> adapted: the "strong" threshold is made graded as the depth of the 72-bar fall, with a graded dead zone.
- Comparison: closes away from the funding settlement times -> kept: a regime keeps only closes whose next 2 hours neither reach nor just follow 00/08/16 UTC (hours-to-settlement 3 to 6).
- Outcome: the return over the next 2 hours is positive, and larger the deeper the fall -> kept: the 2-bar forward return is measured against the fall's depth.
- Verdict transfer: yes: the off-settlement filter, the 72-bar fall depth and the 2-bar rebound are all measured as stated, and only the threshold is graded.
Forecast: The forecast is zero at closes where the coming 2 hours touch or just follow a settlement. That means hours-to-settlement of the coming bar is 1, 2, 7 or 8. At the other closes, take the 72-bar percent price change and standardise it over window 72 with min_periods 20. Then negate it, so a fall reads positive, and clip it at 0, so it is long only. Then apply signed_power with exponent 2 and pivot 10. The forecast is positive after a 72-bar fall and grows with the square of the fall's standardised depth. A fall of usual size gives about 10, half that gives 2.5, and a deep fall gives up to 20. The forecast is zero after a 72-bar rise.
Config: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The sample is non-overlapping grid bars (every 2 bars from each window's first row) in regime mean_reversion with forecast > 0. On each, compute (forecast / 10) x (the 2-bar return minus the coin's mean 2-bar return over all windows). Take the ordinary t of the mean of these values, pooled over coins and windows.
- Supporting check: Split the same cases into forecast quintiles. The mean excess 2-bar return of the top quintile, minus that of the bottom quintile, must be above 0.
- Confirm: The main t is 2 or more, with at least 200 cases, and the top-minus-bottom quintile difference is above 0.
- Reject: The main t is -2 or less, with at least 200 cases.
- Inconclusive: Any main t between -2 and 2 is inconclusive. A main t of 2 or more with a quintile difference of 0 or less is inconclusive. Fewer than 200 cases is inconclusive.
