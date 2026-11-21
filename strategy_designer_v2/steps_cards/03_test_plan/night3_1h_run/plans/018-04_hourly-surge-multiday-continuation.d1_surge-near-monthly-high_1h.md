---
idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: afc0f50f6fe7
---
Fidelity:
- Situation: the 24-hour return first reaches several times the coin's 30-day average absolute daily return, on the upside -> adapted: measured as a graded ratio while it holds, the 24-bar return standardised over 720 bars with a dead zone.
- Comparison: the close stands near its 30-day high, and the closer it is, the larger the rise -> replaced: no component can multiply that ratio by a proximity to the 720-bar high.
- Outcome: over the next 5 days the price rises more than the coin's usual 5-day return -> kept: a 120-bar forward return against the coin's drift.
- Verdict transfer: no: the only proximity-weighted surge, `HighProximityMomentumComponent` standardised on its own history, also divides by the past proximity-weighted moves, which cancels the proximity gate during month-long declines.
Reason: A weighted mean of components cannot form the product "surge ratio × proximity to the 30-day high". `HighProximityMomentumComponent` has no divisor of its own, so `standardise` has to set its scale. That divides it by the mean of its own past proximity-weighted returns, not by the 30-day average absolute daily return. In a decline the denominator shrinks with the numerator, so the rebounds the idea refuses would read as strongly as surges near the high.
