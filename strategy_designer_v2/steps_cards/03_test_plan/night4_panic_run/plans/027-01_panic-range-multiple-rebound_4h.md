---
idea: 027-01_panic-range-multiple-rebound
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a 24-hour fall whose high-low range is a large multiple of the 30-day average 24-hour range -> replaced: no component or combination computes a 24h range over its 30-day mean 24h range.
- Comparison: the coin's usual return over 14 days -> kept: measured against holding the coin.
- Outcome: a higher return over the next 14 days, larger as the range multiple grows -> kept: an 84-bar forward return, graded by the multiple.
- Verdict transfer: no: the nearest stand-in measures a different quantity, so neither a confirm nor a reject would carry over to the idea.
Reason: The 24h fall is available (`PriceEvolutionComponent`, period 6). No component measures the 6-bar high-low range against the mean of 6-bar ranges over 180 bars. `RangeCompressionRatioComponent` divides by the 180-bar total range or the mean single-bar range. `MeanAbsReturnComponent` averages returns, not ranges. The config cannot divide one component by another, so no combination gives the multiple.
