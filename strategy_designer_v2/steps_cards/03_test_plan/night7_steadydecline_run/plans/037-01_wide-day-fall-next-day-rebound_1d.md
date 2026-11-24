---
idea: 037-01_wide-day-fall-next-day-rebound
brief: 037_wide-range-separates-forced-falls
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a one-day fall, larger together with a wider day's range -> replaced: the only fall-times-range-multiple component (`ScaledFallRangeMultipleComponent`) counts the fall in usual 14-day moves, not as the day's fall.
- Comparison: the day's high-to-low range against its own average daily range over the past 14 days -> kept: a range multiple over 14 bars exists (`FallGatedRangeMultipleComponent`, period 1, base_period 14).
- Outcome: a rise over the next day, larger the larger the joint reading -> kept: horizon 1 bar, long only.
- Verdict transfer: no: no existing component grades on the day's fall times its range multiple, so a result would be about a volatility-scaled fall, not the idea.
Reason: The idea needs the day's fall multiplied by the day's range against its 14-day average. The config cannot multiply two components. A weighted sum would give a rebound forecast to a large fall on a narrow day, which the idea says does not rebound. A fall regime with a graded range multiple drops the grading by fall size. `ScaledFallRangeMultipleComponent` replaces the fall with a fall in usual moves, and `RiseTimesRangeMultipleComponent` reads rises only.
