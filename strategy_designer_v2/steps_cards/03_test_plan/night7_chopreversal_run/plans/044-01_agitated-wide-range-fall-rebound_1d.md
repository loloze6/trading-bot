---
idea: 044-01_agitated-wide-range-fall-rebound
brief: 044_agitated-wide-range-fall-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 0e977cd77240
---
Fidelity:
- Situation: a day closing lower, its fall against the 30-day standard deviation of daily returns times its range against the 30-day average range -> replaced: the nearest component, ScaledFallRangeMultipleComponent, divides the fall by the 30-day mean absolute daily return, not the standard deviation.
- Comparison: none -> kept
- Outcome: the next day's rise grows with that product -> kept
- Verdict transfer: no: a result on mean-absolute-scaled falls would not confirm or reject a claim stated on standard-deviation-scaled falls.
Reason: The forecast needs the day's fall in 30-day standard deviations multiplied by the day's range in 30-day average ranges. No catalogue component computes that product with a standard deviation. The config cannot multiply two components, because it only takes weighted sums, and the regime detector's score_product mode is a regime decision, not a forecast.
