---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's day volume, heavier or lighter -> kept
- Comparison: against its own 30-day average volume -> kept
- Outcome: return over the next 3 days is higher the heavier the volume, so favour a long -> kept
- Verdict transfer: yes: the forecast grows with the volume ratio, and the 3-day forward return is tested against it directly.
Forecast: Take VolumeRatioComponent with period 30, which is today's volume divided by its 30-day average. Standardise it over its 60 past values, so it sits near +10 at a usual ratio, higher on heavy days and up to the cap of 20. Average it with a constant offset of -10 at equal weights. The forecast is then (x − 10)/2, graded between about −5 (very light volume) and +10 (very heavy volume). It is 0 at the usual volume ratio, long when volume is above it, more long the heavier the volume, and mildly short when volume is light. It is active on every bar, with no regime.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Regress the coin's 3-bar forward return, minus that coin's mean 3-bar return over all windows, on the bar's forecast. Use bars at positions 0, 3, 6, ... of each window, pooled over coins and windows. Report the slope's t.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2.
- Reject: The slope is negative with t ≤ −2.
- Inconclusive: Any t between −2 and 2 is inconclusive. The test needs at least 300 non-overlapping cases; with fewer, the result is inconclusive.
