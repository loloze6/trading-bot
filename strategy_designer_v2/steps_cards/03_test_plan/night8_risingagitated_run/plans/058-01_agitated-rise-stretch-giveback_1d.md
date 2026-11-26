---
idea: 058-01_agitated-rise-stretch-giveback
brief: 058_rising-agitated-overextension-gives-back
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: close standing above its 20-day average price, in a rising agitated market -> adapted: the profile is added by code, and the distance above the 20-day SMA is graded and zero at or below the average.
- Comparison: the further above the average, the larger the fall -> kept: the short grows with the percent distance above the SMA.
- Outcome: the coin falls over the next 5 days -> kept: short, held 5 bars.
- Verdict transfer: yes: the forecast is the idea's distance itself, inside its profile, over its 5-day horizon.
Forecast: The forecast uses one indicator, the percent distance of the close from its 20-day simple moving average, with the current close included. It is standardised over its own past 60 values (min_periods 20), clipped at 0 so that only distances above the average count, then negated. So the forecast is zero when the close is at or below its 20-day average. It is negative (short) when the close is above the average, and the short grows continuously with the distance above it, up to -20. Code adds the rising agitated profile, so the book is flat outside it.
Config: 058-01_agitated-rise-stretch-giveback_1d_config.json
Profile: rising agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The sample is grid bars with forecast below 0, on a non-overlapping 5-bar grid per window, all coins pooled. On those bars, regress the coin's 5-bar forward return minus its normal 5-bar drift (holding the coin) on abs(forecast). The measure is the slope's t, before costs.
- Supporting check: On the same cases, the mean unusual move in the short direction (minus the excess return) must be above 0.
- Confirm: Confirmed when the slope is negative with t <= -2 (a larger distance is followed by a larger fall versus drift) and the mean unusual move in the short direction is positive.
- Reject: Rejected when the slope is positive with t >= +2: a larger distance is followed by a further rise versus drift.
- Inconclusive: Any slope with |t| < 2 is inconclusive, as is t <= -2 with a mean unusual move at or below 0. Fewer than 30 independent short cases is also inconclusive.
