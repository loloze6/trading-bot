---
idea: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 3503e22a3698
---
Fidelity:
- Situation: a 24-hour fall whose high-low range is a large multiple of its 30-day average 24-hour range -> adapted: graded by `FallGatedRangeMultipleComponent` (period 6, base_period 180, fall_period 6) instead of a "large" threshold.
- Comparison: only while 7-day volatility is high against 60-day volatility, the excess growing with that ratio -> kept as a measure by `VolatilityRatioToAverageComponent` (vol_period 42, vol_lookback 360), but it cannot multiply the situation.
- Outcome: a higher-than-usual return over the next 14 days (84 bars), rising with the range multiple -> kept.
- Verdict transfer: no: no config can make the position grow with both the range multiple and the volatility ratio while staying zero without a panic.
Reason: The idea needs the panic's range multiple scaled by the 7-day/60-day volatility ratio, so the position is zero without a fall and grows with both. A strategy only takes a weighted mean of its components. Adding the ratio would put on longs in turbulent weeks with no panic, and a regime gate on the ratio would drop "the excess growing with that ratio". No catalogue component computes this product.
