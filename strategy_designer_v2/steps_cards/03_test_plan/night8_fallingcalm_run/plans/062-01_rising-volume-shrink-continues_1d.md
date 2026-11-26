---
idea: 062-01_rising-volume-shrink-continues
brief: 062_rising-market-volume-dry-up-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: ca7c09a81ba4
---
Fidelity:
- Situation: in a rising market, volume over the past 30 days shrunk against the 30 days before -> kept: the profile code keeps the rising market, and the shrink is ln(mean volume of days t-29..t / mean volume of days t-59..t-30).
- Comparison: shrinking volume against volume that held up or grew -> kept: the forecast is 0 when volume did not shrink, and those in-profile bars are the comparison group.
- Outcome: a larger rise over the next 5 days, growing with the shrink -> kept: a long position sized by the shrink, held 5 bars.
- Verdict transfer: yes: the forecast and the 5-day return measure exactly the stated relation inside rising markets.
Forecast: One indicator: the log ratio of the mean daily volume over the last 30 days to the mean over the 30 days before them (`VolumeRatioComponent`, short_period 30, period 30, exclude_current 30, form "log"). It is standardised over its past 60 values, negated so that a shrink reads positive, and clipped at 0. The forecast is therefore 0 when volume held up or grew. It is positive when volume shrank, and grows continuously with the depth of the shrink, up to +20. It is long only. The profile code keeps the book flat outside rising markets.
Config: 062-01_rising-volume-shrink-continues_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: On the non-overlapping 5-bar grid of each window, take only the bars inside the rising profile (component recorded), all coins pooled. Measure the slope of the coin's 5-bar forward return, minus its normal 5-bar drift (holding the coin over all windows), on the bar's forecast, with its t.
- Supporting check: On the same grid bars, the mean excess 5-bar return of bars with forecast > 0 minus that of bars with forecast = 0 must be above 0 (Welch).
- Confirm: The slope is positive with t >= 2, and the supporting check's difference is above 0.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any slope t between -2 and 2, or a confirming slope whose supporting difference is not above 0. The test needs at least 100 in-profile grid cases, of which at least 30 have forecast > 0 and at least 30 have forecast = 0; fewer cases is inconclusive.
