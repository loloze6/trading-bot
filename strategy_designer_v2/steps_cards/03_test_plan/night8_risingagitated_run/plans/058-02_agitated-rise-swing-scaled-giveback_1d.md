---
idea: 058-02_agitated-rise-swing-scaled-giveback
brief: 058_rising-agitated-overextension-gives-back
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 78914cf300b5
---
Fidelity:
- Situation: rising, agitated market; close above its 20-day average, in units of the 20-day daily swing -> kept: the profile is added by code; the distance is MovingAverageDistanceComponent (SMA 20, "usual_moves", vol_period 20), and below the average it is zero.
- Comparison: the further above, the larger the fall -> kept: the short grows continuously with the distance.
- Outcome: the coin falls over the next 5 days -> kept: short, held 5 daily bars.
- Verdict transfer: yes: the forecast is the idea's own measure, signed and graded as the idea states, judged over its own 5-day horizon.
Forecast: The forecast starts from the distance of the close above its 20-day simple average, divided by the standard deviation of the last 20 daily returns. That distance is standardised against its past 60 values, then negated, then clipped at 0. The result is a short position whose size grows with how far the close stands above the average, in usual daily moves. It is zero when the close is at or below the average, and never long. Code adds the rising-agitated profile, so the book is flat outside that profile.
Config: 058-02_agitated-rise-swing-scaled-giveback_1d_config.json
Profile: rising agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window, on bars where the forecast is below 0. Regress the coin's 5-bar forward return, minus its mean 5-bar return over all windows, on the forecast. Cases on the same day are taken together. The idea predicts a positive slope: a more negative forecast is followed by a lower return.
- Supporting check: On those same cases, the mean drift-removed 5-bar return taken in the signal's direction (the strength) is above 0.
- Confirm: The slope's t is 2 or more, the supporting check's mean is above 0, and there are at least 50 cases.
- Reject: The slope's t is -2 or less, with at least 50 cases. This means a larger stretch above the average is followed by a further rise.
- Inconclusive: Any slope t between -2 and 2. Also a t of 2 or more when the supporting check fails. Also any result from fewer than 50 grid cases with a forecast below 0.
