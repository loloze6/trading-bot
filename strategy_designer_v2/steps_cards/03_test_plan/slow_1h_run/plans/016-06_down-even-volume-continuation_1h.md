---
idea: 016-06_down-even-volume-continuation
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: coin has fallen over the past 3 days, with hourly volume spread evenly across those hours -> kept: a 72-bar fall regime, and evenness read as ln(mean / median) of the 72 hourly volumes (0 when even, larger when bursty)
- Comparison: more even volume against less even volume, among falling coins -> kept: the short grows as the volume concentration falls
- Outcome: the coin keeps falling over the next 3 days, more so the more even the volume -> adapted: 72-bar holding period dropped; the short is held while the fall lasts
- Verdict transfer: yes: the forecast is graded only by evenness inside the fallen state, so its link to the next 72 bars' excess return answers the idea both ways.
Forecast: The regime is active only while the 72-bar return is below zero; elsewhere the forecast is 0. Inside the regime there are two parts. The first is the volume concentration c = ln(mean / median) of the last 72 hourly volumes, standardised over 72 bars. It is about +10 at its usual level and capped at 20. The second is a constant standardised to -10 at weight 2. The forecast is (c − 20) / 3. It sits near 0 when volume came in bursts, about -3.3 at usual concentration, and about -6.7 or deeper when volume was even. If mean < median, c is negative and the short goes deeper, to at most -13.3. The short therefore grows smoothly as volume becomes more even.
Config: 016-06_down-even-volume-continuation_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The sample is the bars of a non-overlapping 72-bar grid in each window where the regime is trending. On each, take the coin's 72-bar forward return minus that coin's mean 72-bar return over all windows (the excess over holding). Regress this excess return on the bar's forecast, pooled over coins, and report the slope's t. A positive slope means more-even falls (more negative forecast) are followed by lower excess returns.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2.
- Reject: The slope is negative with t ≤ -2: even-volume falls are followed by higher excess returns than bursty ones.
- Inconclusive: Any slope with -2 < t < 2 is inconclusive. Fewer than 200 grid cases in the fallen regime is also inconclusive.
